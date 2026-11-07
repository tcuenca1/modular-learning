"""Servicio de aplicación de guías de estudio offline y su confirmación al volver."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from modular_learning.core.application.repaso import RepasoService
from modular_learning.core.domain.guia_offline import (
    CON_DUDAS,
    ENTENDIDA,
    EXTENSIONES,
    MARCADOR_RESPUESTAS,
    MAXIMO_CLASES,
    RESULTADOS,
    ClaseGuia,
    GuiaOffline,
    elegir_extension,
    separar_respuestas,
)
from modular_learning.core.domain.materias import slug_materia
from modular_learning.core.ports.documentos import LectorDocumentosPort
from modular_learning.core.ports.guias import ExportadorPdfPort, GuiasRepo
from modular_learning.core.ports.llm import LLMPort
from modular_learning.core.ports.repositorios import CronogramaRepo


def _ahora() -> str:
    return datetime.now().isoformat(timespec="seconds")


def _texto_lista(valor: Any) -> str:
    if isinstance(valor, list):
        return ", ".join(str(v) for v in valor if v) or "ninguno"
    return str(valor or "").strip() or "no indicado"


class GuiaOfflineService:
    """Caso de uso: arma guías de lectura sin conexión y aplica lo que el estudiante revisó."""

    def __init__(
        self,
        llm: LLMPort,
        cronograma_repo: CronogramaRepo,
        lector_docs: LectorDocumentosPort,
        guias_repo: GuiasRepo,
        repaso: RepasoService | None = None,
        exportador_pdf: ExportadorPdfPort | None = None,
    ):
        self.llm = llm
        self.cronograma_repo = cronograma_repo
        self.lector_docs = lector_docs
        self.guias_repo = guias_repo
        self.repaso = repaso
        self.exportador_pdf = exportador_pdf

    # ------------------------------------------------------------------ creación
    def crear(
        self, materia: str, temas: list[str], tiempo_minutos: int | None = None
    ) -> GuiaOffline:
        """
        Registra la guía con las clases elegidas (por id o por tema), en el orden del cronograma,
        sin generar aún. Si se indica `tiempo_minutos`, la extensión se adapta a ese presupuesto.
        """
        if not temas:
            raise ValueError("Elige al menos una clase para la guía.")
        if len(temas) > MAXIMO_CLASES:
            raise ValueError(f"Una guía admite como máximo {MAXIMO_CLASES} clases.")

        cronograma = self.cronograma_repo.obtener_cronograma(materia)
        if not cronograma:
            raise ValueError(f"La asignatura {materia} no tiene cronograma.")

        buscados_ids = {str(t).strip() for t in temas}
        buscados_temas = {str(t).strip().lower() for t in temas}

        clases: list[ClaseGuia] = []
        encontrados_ids: set[str] = set()
        encontrados_temas: set[str] = set()

        for c in cronograma:
            c_id = str(c.get("id") or "").strip()
            c_tema = str(c.get("tema") or "").strip()
            c_tema_l = c_tema.lower()

            if (c_id and c_id in buscados_ids) or c_tema_l in buscados_temas:
                clases.append(
                    ClaseGuia(
                        tema=c_tema,
                        fecha=str(c.get("fecha", "")),
                        clase_id=c_id,
                    )
                )
                if c_id:
                    encontrados_ids.add(c_id)
                encontrados_temas.add(c_tema_l)

        if not clases:
            faltan = sorted(buscados_temas - encontrados_temas)
            raise ValueError(f"Estas clases no están en el cronograma: {', '.join(faltan)}")

        guia = GuiaOffline(
            id=uuid.uuid4().hex[:12],
            materia=materia,
            extension=elegir_extension(len(clases), tiempo_minutos),
            creada=_ahora(),
            clases=clases,
            tiempo_minutos=tiempo_minutos,
        )
        self.guias_repo.guardar(guia)
        return guia

    def generar_clase(self, guia_id: str, indice: int) -> ClaseGuia:
        """Genera (o regenera) el contenido de una clase de la guía con el LLM."""
        guia = self.obtener(guia_id)
        if not 0 <= indice < len(guia.clases):
            raise ValueError(f"La guía no tiene la clase {indice}.")
        clase = guia.clases[indice]
        detalle = self.cronograma_repo.obtener_detalle_clase(
            guia.materia, tema=clase.tema, clase_id=clase.clase_id
        )

        plantilla = self.lector_docs.leer_prompt("06_guia_offline.md")
        prompt = plantilla.format(
            materia=guia.materia,
            tema=clase.tema,
            objetivo=_texto_lista(detalle.get("objetivo")),
            contenido=_texto_lista(detalle.get("contenido")),
            subtemas=_texto_lista(detalle.get("subtemas_adicionales")),
            extension=EXTENSIONES.get(guia.extension, EXTENSIONES["estandar"]),
            marcador=MARCADOR_RESPUESTAS,
        )
        clase.contenido, clase.respuestas = separar_respuestas(self.llm.generar_texto(prompt))
        self.guias_repo.guardar(guia)
        return clase

    # ------------------------------------------------------------------ consultas
    def obtener(self, guia_id: str) -> GuiaOffline:
        guia = self.guias_repo.obtener(guia_id)
        if guia is None:
            raise LookupError("Guía no encontrada.")
        return guia

    def listar(self) -> list[GuiaOffline]:
        return self.guias_repo.listar()

    def pendientes_de_confirmar(self) -> list[GuiaOffline]:
        return [g for g in self.guias_repo.listar() if g.pendiente_de_confirmar]

    # ------------------------------------------------------------------ revisión
    def registrar_revision(
        self, guia_id: str, resultados: dict[int, tuple[str, str]]
    ) -> dict[str, Any]:
        """
        Aplica lo que el estudiante dice de cada clase: entendida (con o sin dudas) la marca
        como completada; pendiente la deja como estaba. Registra cada clase en el historial.
        """
        guia = self.obtener(guia_id)
        if guia.revisada:
            raise ValueError("Esta guía ya se confirmó.")
        if not guia.completa:
            raise ValueError("La guía todavía no está generada por completo.")
        if set(resultados) != set(range(len(guia.clases))):
            raise ValueError("Indica cómo te fue con cada clase de la guía.")

        completadas: list[str] = []
        pendientes: list[str] = []
        dudas: list[dict[str, str]] = []
        for indice, (resultado, texto_dudas) in sorted(resultados.items()):
            if resultado not in RESULTADOS:
                raise ValueError(f"Resultado no válido: {resultado}")
            clase = guia.clases[indice]
            clase.resultado = resultado
            clase.dudas = texto_dudas.strip() if resultado == CON_DUDAS else ""

            detalle = self.cronograma_repo.obtener_detalle_clase(
                guia.materia, tema=clase.tema, clase_id=clase.clase_id or None
            )
            clase.estado_previo = detalle.get("estado") if detalle else None

            if resultado in (ENTENDIDA, CON_DUDAS):
                self.cronograma_repo.marcar_clase_completada(
                    guia.materia, tema_exacto=clase.tema, clase_id=clase.clase_id
                )
                completadas.append(clase.tema)
                if clase.dudas:
                    dudas.append({"tema": clase.tema, "dudas": clase.dudas})
            else:
                pendientes.append(clase.tema)
            if self.repaso:
                self.repaso.registrar_estudio_offline(
                    guia.materia,
                    clase.tema,
                    resultado,
                    clase.dudas,
                    guia_id=guia.id,
                )

        guia.revisada = _ahora()
        self.guias_repo.guardar(guia)
        return {
            "materia": guia.materia,
            "completadas": completadas,
            "pendientes": pendientes,
            "dudas": dudas,
        }

    def deshacer_revision(self, guia_id: str) -> dict[str, Any]:
        """
        Deshace la confirmación de la guía:
        - Revierte el estado de las clases en el cronograma a 'pendiente'
        - Limpia el resultado y dudas de la guía
        - Quita del historial los eventos registrados por esta guía
        """
        guia = self.obtener(guia_id)
        if not guia.revisada:
            raise ValueError("Esta guía no ha sido confirmada todavía.")

        revertidas: list[str] = []
        for clase in guia.clases:
            if clase.resultado in (ENTENDIDA, CON_DUDAS):
                self.cronograma_repo.marcar_clase(
                    guia.materia,
                    clase_id=clase.clase_id or None,
                    tema=clase.tema,
                    estado=clase.estado_previo or "pendiente",
                )
                revertidas.append(clase.tema)
            clase.resultado = None
            clase.dudas = ""
            clase.estado_previo = None

        if self.repaso:
            self.repaso.historial_repo.eliminar(
                lambda e: e.get("tipo") == "guia" and e.get("guia_id") == guia.id
            )

        guia.revisada = None
        self.guias_repo.guardar(guia)
        return {
            "guia_id": guia.id,
            "materia": guia.materia,
            "revertidas": revertidas,
        }

    def eliminar_guia(self, guia_id: str) -> bool:
        """Elimina una guía guardada."""
        return self.guias_repo.eliminar([guia_id]) > 0

    def exportar_pdf(self, guia_id: str) -> tuple[bytes, str]:
        """Genera un archivo PDF vectorizado en A5 para la guía indicada."""
        guia = self.guias_repo.obtener(guia_id)
        if not guia:
            raise LookupError(f"Guía {guia_id} no encontrada.")
        if not self.exportador_pdf:
            raise ValueError("No hay exportador de PDF configurado.")
        pdf_bytes = self.exportador_pdf.exportar_guia(guia)
        slug = slug_materia(guia.materia)
        nombre_archivo = f"Guia_{slug}_{guia.id}.pdf"
        return pdf_bytes, nombre_archivo


__all__ = ["GuiaOfflineService"]
