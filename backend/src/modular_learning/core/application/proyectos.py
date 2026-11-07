"""Servicio de aplicación para el análisis, ingesta y trazabilidad de proyectos integrales."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from modular_learning.core.domain.materias import slug_materia
from modular_learning.core.domain.proyectos import (
    TOLERANCIA_MTIME_SEGUNDOS,
    HuellaProyecto,
    ParcialProyecto,
    Proyecto,
    TipoProyecto,
    etiqueta_parcial,
    slug_proyecto,
)
from modular_learning.core.ports.boveda import BovedaNotasPort
from modular_learning.core.ports.documentos import LectorDocumentosPort
from modular_learning.core.ports.llm import LLMPort
from modular_learning.core.ports.proyectos import InspectorProyectosPort, ProyectosRepo
from modular_learning.core.ports.repositorios import RegistroMaterialesRepo


def _iso(momento: datetime) -> str:
    return momento.isoformat(timespec="seconds")


class ProyectosService:
    """Caso de uso para escanear, analizar y dar seguimiento a proyectos académicos."""

    def __init__(
        self,
        proyectos_repo: ProyectosRepo,
        registro_repo: RegistroMaterialesRepo,
        boveda_port: BovedaNotasPort,
        lector_docs: LectorDocumentosPort,
        llm: LLMPort,
        inspector: InspectorProyectosPort,
    ):
        self.proyectos_repo = proyectos_repo
        self.registro_repo = registro_repo
        self.boveda_port = boveda_port
        self.lector_docs = lector_docs
        self.llm = llm
        self.inspector = inspector

    def listar_proyectos(self, materia: str | None = None) -> list[Proyecto]:
        """Retorna todos los proyectos registrados."""
        return self.proyectos_repo.listar(materia)

    def obtener_proyecto(self, id_proyecto: str) -> Proyecto | None:
        return self.proyectos_repo.obtener(id_proyecto)

    def eliminar_proyecto(self, id_proyecto: str) -> bool:
        return self.proyectos_repo.eliminar(id_proyecto)

    def escanear_proyectos_en_carpeta(
        self, materia: str, carpeta_materia: str
    ) -> list[dict[str, Any]]:
        """
        Detecta los proyectos de la asignatura:
        - En 'PROYECTO': subcarpetas o archivos directos (parcial general).
        - En 'PROYECTOS': subcarpetas 'PRIMER PARCIAL' y 'SEGUNDO PARCIAL'.
        """
        return [{"materia": materia, **p} for p in self.inspector.escanear(carpeta_materia)]

    def generar_ficha_markdown(
        self,
        materia: str,
        nombre_proyecto: str,
        parcial: ParcialProyecto,
        tipo: TipoProyecto,
        ruta_origen: str,
        huella: HuellaProyecto,
    ) -> str:
        """Construye la ficha técnica en Markdown con Frontmatter YAML y análisis con IA."""
        fecha_analisis = _iso(datetime.now(timezone.utc))
        fecha_cambio = (
            _iso(datetime.fromtimestamp(huella.mtime, tz=timezone.utc))
            if huella.mtime > 0
            else fecha_analisis
        )
        contexto = self.inspector.extraer_contexto(ruta_origen)
        prompt = self.lector_docs.leer_prompt("07_ficha_proyecto.md").format(
            materia=materia, nombre_proyecto=nombre_proyecto, contexto=contexto
        )
        try:
            analisis = self.llm.generar_texto(prompt).strip()
        except Exception:
            analisis = (
                f"## 📌 Resumen del Proyecto\nProyecto de tipo `{tipo}`.\n\n"
                f"## 🗂️ Componentes Detectados\nTotal de archivos: {huella.total_archivos}\n\n"
                f"```text\n{contexto[:1500]}\n```"
            )

        ruta_yaml = ruta_origen.replace("\\", "/")
        return (
            f"---\n"
            f"tipo: proyecto\n"
            f"materia: {materia}\n"
            f"parcial: {parcial}\n"
            f"tipo_proyecto: {tipo}\n"
            f"ruta_origen: {ruta_yaml}\n"
            f"fecha_analisis: {fecha_analisis}\n"
            f"fecha_ultimo_cambio_archivos: {fecha_cambio}\n"
            f"hash_estado: {huella.hash_estado}\n"
            f"total_archivos: {huella.total_archivos}\n"
            f"---\n\n"
            f"# Proyecto: {nombre_proyecto} ({etiqueta_parcial(parcial)})\n\n"
            f"- **Asignatura:** {materia}\n"
            f"- **Ubicación local:** `{ruta_origen}`\n"
            f"- **Naturaleza técnica:** `{tipo}` ({huella.total_archivos} archivos)\n"
            f"- **Última modificación detectada en disco:** {fecha_cambio}\n\n"
            f"{analisis}\n"
        )

    def analizar_e_ingestar_proyecto(
        self,
        materia: str,
        nombre_proyecto: str,
        parcial: ParcialProyecto,
        ruta_origen: str,
        tipo_forzado: TipoProyecto | None = None,
    ) -> Proyecto:
        """Analiza un proyecto, guarda su ficha en Obsidian y lo registra con trazabilidad."""
        huella = self.inspector.huella(ruta_origen)
        if huella is None:
            raise ValueError(f"No existe el proyecto en {ruta_origen}.")
        tipo = tipo_forzado or self.inspector.detectar_tipo(ruta_origen)

        ficha_md = self.generar_ficha_markdown(
            materia, nombre_proyecto, parcial, tipo, ruta_origen, huella
        )
        nombre_base = slug_materia(nombre_proyecto)
        if parcial != "general":
            nombre_base = f"{parcial.upper()}_{nombre_base}"
        ruta_salida = self.boveda_port.guardar_nota(materia, "Proyectos", nombre_base, ficha_md)

        proyecto = Proyecto(
            id=slug_proyecto(materia, nombre_proyecto, parcial),
            nombre=nombre_proyecto,
            materia=materia,
            parcial=parcial,
            tipo=tipo,
            ruta_origen=ruta_origen,
            ruta_nota_obsidian=ruta_salida,
            fecha_analisis=_iso(datetime.now()),
            mtime_archivos=huella.mtime,
            total_archivos=huella.total_archivos,
            hash_estado=huella.hash_estado,
        )
        self.proyectos_repo.guardar(proyecto)
        self.registro_repo.registrar_material(
            nombre_archivo=f"[PROYECTO] {nombre_proyecto} ({parcial})",
            materia=materia,
            nota=ruta_salida,
        )
        return proyecto

    def verificar_estado_proyecto(self, proyecto_id: str) -> dict[str, Any]:
        """Compara el estado actual en disco con el del último análisis para detectar cambios."""
        proyecto = self.proyectos_repo.obtener(proyecto_id)
        if not proyecto:
            return {"existe": False, "estado": "no_encontrado"}

        huella = self.inspector.huella(proyecto.ruta_origen)
        if huella is None:
            return {
                "existe": False,
                "proyecto": proyecto.a_dict(),
                "estado": "carpeta_eliminada",
                "mensaje": f"La carpeta u origen en {proyecto.ruta_origen} ya no existe.",
            }

        modificado = huella.mtime > proyecto.mtime_archivos + TOLERANCIA_MTIME_SEGUNDOS
        return {
            "existe": True,
            "proyecto": proyecto.a_dict(),
            "estado": "cambios_detectados" if modificado else "al_dia",
            "modificado": modificado,
            "mtime_registrado": proyecto.mtime_archivos,
            "mtime_actual": huella.mtime,
            "total_archivos_actual": huella.total_archivos,
            "hash_actual": huella.hash_estado,
        }

    def actualizar_proyecto(self, proyecto_id: str) -> Proyecto:
        """Re-escanea y actualiza la ficha del proyecto en Obsidian y el repositorio."""
        proyecto = self.proyectos_repo.obtener(proyecto_id)
        if not proyecto:
            raise ValueError(f"Proyecto con ID '{proyecto_id}' no encontrado.")
        return self.analizar_e_ingestar_proyecto(
            materia=proyecto.materia,
            nombre_proyecto=proyecto.nombre,
            parcial=proyecto.parcial,
            ruta_origen=proyecto.ruta_origen,
            tipo_forzado=proyecto.tipo,
        )

    def vaciar_proyectos(self, borrar_notas_obsidian: bool = True) -> int:
        """Elimina todos los proyectos registrados y, si se pide, sus fichas en Obsidian."""
        if borrar_notas_obsidian:
            for p in self.proyectos_repo.listar():
                if p.ruta_nota_obsidian:
                    self.boveda_port.eliminar_nota(p.ruta_nota_obsidian)
        return self.proyectos_repo.vaciar()


__all__ = ["ProyectosService"]
