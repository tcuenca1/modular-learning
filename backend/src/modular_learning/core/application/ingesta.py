"""Servicio de aplicación para ingesta y anonimización de material de estudio (`ml im`)."""

from __future__ import annotations

import logging
import mimetypes
import os
import re
import time
from collections.abc import Iterator
from typing import Any

from modular_learning.core.application.plugins import PluginsService
from modular_learning.core.application.proyectos import ProyectosService
from modular_learning.core.domain import alineador_curricular
from modular_learning.core.domain.materias import resolver_materia
from modular_learning.core.domain.rutas import unir_dentro
from modular_learning.core.ports.boveda import BovedaNotasPort
from modular_learning.core.ports.config import AjustesPort
from modular_learning.core.ports.conversor_pdf import ConversorPdfPort
from modular_learning.core.ports.documentos import LectorDocumentosPort
from modular_learning.core.ports.llm import LLMPort
from modular_learning.core.ports.repositorios import (
    CronogramaRepo,
    MateriaRepo,
    RegistroMaterialesRepo,
)

logger = logging.getLogger(__name__)

EXTENSIONES_MATERIAL = (".pdf", ".docx", ".txt", ".md", ".pptx")
EXTENSIONES_NO_SOPORTADAS_WEB: tuple[str, ...] = ()
TIPOS_MATERIAL = ("actividad", "diapositiva", "lectura", "material_complementario")

REGLA_PRIVACIDAD = (
    "\n\n[REGLA ESTRICTA DE PRIVACIDAD Y ANONIMIZACIÓN]:\n"
    "Oculta o anonimiza cualquier nombre de estudiante, profesor, número de identificación institucional, "
    "correos electrónicos o datos personales que aparezcan en el documento. Reemplázalos por etiquetas "
    "genéricas como [ESTUDIANTE], [DOCENTE] o [ID_OMITIDO]."
)


class IngestaService:
    """Caso de uso para la ingesta multimodal, extracción con IA, alineación y archivo en Obsidian."""

    def __init__(
        self,
        llm: LLMPort,
        registro_repo: RegistroMaterialesRepo,
        boveda_port: BovedaNotasPort,
        lector_docs: LectorDocumentosPort,
        ajustes_port: AjustesPort,
        plugins_service: PluginsService | None = None,
        cronograma_repo: CronogramaRepo | None = None,
        proyectos_service: ProyectosService | None = None,
        materia_repo: MateriaRepo | None = None,
        conversor_pdf: ConversorPdfPort | None = None,
    ):
        self.llm = llm
        self.registro_repo = registro_repo
        self.boveda_port = boveda_port
        self.lector_docs = lector_docs
        self.ajustes_port = ajustes_port
        self.plugins_service = plugins_service
        self.cronograma_repo = cronograma_repo
        self.proyectos_service = proyectos_service
        self.materia_repo = materia_repo
        self.conversor_pdf = conversor_pdf

    def clasificar_tipo_material(self, ruta_archivo: str, ruta_raiz_lote: str) -> str:
        """Clasifica el material según su ubicación en la carpeta de la asignatura."""
        rel_path = os.path.relpath(ruta_archivo, ruta_raiz_lote)
        partes_upper = [p.upper() for p in rel_path.split(os.sep)]
        if "PROYECTO" in partes_upper or "PROYECTOS" in partes_upper:
            return "proyecto"
        if len(rel_path.split(os.sep)) == 1:
            return "actividad"
        ruta_upper = rel_path.upper()
        if "ACTIVIDADES" in partes_upper or "ACTIVIDAD" in partes_upper:
            return "actividad"
        if "MATERIAL DE ESTUDIO" in ruta_upper:
            return "diapositiva"
        if "MATERIAL ADICIONAL" in ruta_upper:
            return "lectura"
        return "material_complementario"

    def _generar_contenido(self, ruta: str, prompt: str) -> tuple[str, str | None]:
        ext = os.path.splitext(ruta)[1].lower()
        if ext in (".docx", ".txt", ".md"):
            texto = self.lector_docs.extraer_texto(ruta)
            return (
                self.llm.generar_texto(f"{prompt}\n\nCONTENIDO DEL DOCUMENTO:\n{texto}"),
                None,
            )

        if ext == ".pptx":
            pdf_temporal = None
            if self.conversor_pdf:
                pdf_temporal = self.conversor_pdf.convertir_a_pdf(ruta)

            if pdf_temporal:
                try:
                    contenido = self.llm.generar_texto_con_archivo(
                        {"mime_type": "application/pdf", "path": pdf_temporal}, prompt
                    )
                    return contenido, None
                finally:
                    if self.conversor_pdf:
                        self.conversor_pdf.borrar_temporal(pdf_temporal)
            else:
                texto = self.lector_docs.extraer_texto(ruta)
                texto_util = re.sub(
                    r"---\s*Diapositiva\s*\d+\s*---", "", texto, flags=re.IGNORECASE
                ).strip()
                if len(texto_util) < 200:
                    raise ValueError(
                        "La presentación es solo imágenes: instala LibreOffice para procesarla"
                    )

                aviso = (
                    "Se extrajo únicamente el texto de la presentación (plan B con python-pptx). "
                    "Las imágenes y diagramas visuales no se pudieron procesar (LibreOffice no disponible)."
                )
                contenido = self.llm.generar_texto(f"{prompt}\n\nCONTENIDO DEL DOCUMENTO:\n{texto}")
                return contenido, aviso

        mime = (
            "application/pdf" if ext == ".pdf" else (mimetypes.guess_type(ruta)[0] or "text/plain")
        )
        return (
            self.llm.generar_texto_con_archivo({"mime_type": mime, "path": ruta}, prompt),
            None,
        )

    def _alinear_con_cronograma(
        self, materia: str, contenido_md: str, nombre_archivo: str
    ) -> dict[str, Any]:
        """Asigna el material a la clase más afín y persiste el cronograma actualizado."""
        if not self.cronograma_repo:
            return {}
        clases = self.cronograma_repo.obtener_cronograma(materia) or []
        resultado = alineador_curricular.asignar_material_a_clase(
            clases, contenido_md, nombre_archivo, llm=self.llm
        )
        if resultado.get("asignado") is True:
            self.cronograma_repo.guardar_cronograma(materia, clases)
        elif resultado.get("asignado") is False:
            self.cronograma_repo.agregar_material_transversal(
                materia, alineador_curricular.item_material_transversal(nombre_archivo, resultado)
            )
        return resultado

    def _nombre_materia(self, materia: str) -> str:
        if self.materia_repo:
            m_obj = resolver_materia(self.materia_repo.listar(), materia)
            if m_obj:
                return m_obj.nombre
        return materia

    def ingestar_archivo(
        self,
        ruta_archivo: str,
        nombre_original: str,
        materia: str,
        tipo: str = "material_complementario",
    ) -> dict[str, Any]:
        """Ingesta un archivo individual, extrae contenido anonimizado y lo sincroniza."""
        materia = self._nombre_materia(materia)
        if tipo not in TIPOS_MATERIAL:
            tipo = "material_complementario"

        ruta_boveda = self.ajustes_port.ruta_boveda()
        try:
            plantilla = self.lector_docs.leer_prompt("05_ingesta_material.md")
        except Exception:
            plantilla = "Actúa como un extractor de conocimiento experto y transcribe este documento en Markdown."

        prompt = (
            plantilla.replace("{materia}", materia)
            .replace("{tipo}", tipo)
            .replace("{fecha}", time.strftime("%Y-%m-%d"))
            .replace("{materia_slug}", materia.lower().replace(" ", "_"))
            + REGLA_PRIVACIDAD
        )

        contenido_md, aviso = self._generar_contenido(ruta_archivo, prompt)

        base = os.path.splitext(nombre_original)[0].replace(" ", "_")
        ruta_salida = self.boveda_port.guardar_nota(
            materia, tipo.capitalize(), f"{base}_Notas", contenido_md, ruta_boveda
        )

        self.registro_repo.registrar_material(nombre_original, materia, nota=ruta_salida)

        alineacion: dict[str, Any] = {}
        try:
            alineacion = self._alinear_con_cronograma(materia, contenido_md, nombre_original)
        except Exception as e:
            logger.warning("No se pudo alinear '%s' con el cronograma: %s", nombre_original, e)
            alineacion = {"error": str(e)}

        plugin_actualizado = False
        if self.plugins_service:
            plugin = self.plugins_service.obtener_plugin(materia)
            if plugin:
                try:
                    tecnico = self.llm.generar_texto(
                        "Extrae únicamente un listado técnico de los comandos, nodos, topologías o "
                        "configuraciones exactas que aparecen en este documento. Devuelve solo la lista, "
                        f"sin introducciones.\n\nDOCUMENTO:\n{contenido_md[:8000]}"
                    ).strip()
                    if tecnico:
                        plugin.guardar_contexto_extraido(tecnico)
                        plugin_actualizado = True
                except Exception as e:
                    logger.warning("No se pudo actualizar la memoria del plugin: %s", e)

        resultado_final: dict[str, Any] = {
            "archivo": nombre_original,
            "materia": materia,
            "tipo": tipo,
            "ruta_salida": ruta_salida,
            "contenido_md": contenido_md,
            "alineacion": alineacion,
            "plugin_actualizado": plugin_actualizado,
        }
        if aviso:
            resultado_final["aviso"] = aviso
        return resultado_final

    def listar_materiales_ingestados(self) -> list[dict[str, Any]]:
        """Retorna todos los archivos registrados en la auditoría de ingesta."""
        return self.registro_repo.listar_materiales()

    def eliminar_material(
        self, nombre_archivo: str, borrar_nota: bool = True
    ) -> dict[str, Any] | None:
        """
        Elimina el archivo del registro. Si borrar_nota es True y existe la nota en Obsidian,
        la borra de la bóveda. También desvincula el archivo del cronograma de la asignatura.
        """
        eliminado = self.registro_repo.eliminar_material(nombre_archivo)
        if not eliminado:
            return None

        if borrar_nota and eliminado.get("nota"):
            self.boveda_port.eliminar_nota(eliminado["nota"])

        materia = eliminado.get("materia", "")
        if materia and self.cronograma_repo:
            self.cronograma_repo.quitar_material_transversal(materia, nombre_archivo)
            clases = self.cronograma_repo.obtener_cronograma(materia)
            if clases:
                cambio = False
                for c in clases:
                    asoc = c.get("materiales_asociados", [])
                    if nombre_archivo in asoc:
                        c["materiales_asociados"] = [x for x in asoc if x != nombre_archivo]
                        cambio = True
                if cambio:
                    self.cronograma_repo.guardar_cronograma(materia, clases)

        return eliminado

    def escanear_materia(self, materia: str) -> dict[str, Any]:
        """Detecta los archivos nuevos (no ingestados) de la carpeta de la asignatura."""
        # La asignatura nunca puede salirse de la carpeta de material (p. ej. "../..")
        carpeta = unir_dentro(self.ajustes_port.carpeta_material(), materia)
        archivos = self.lector_docs.listar_archivos(carpeta) if carpeta else None
        resultado: dict[str, Any] = {
            "materia": materia,
            "carpeta": carpeta or "",
            "existe": archivos is not None,
            "total": 0,
            "omitidos": 0,
            "no_soportados": 0,
            "pendientes": [],
        }
        if not resultado["existe"]:
            return resultado

        for ruta in archivos or []:
            nombre = os.path.basename(ruta)
            ext = os.path.splitext(nombre)[1].lower()
            if ext in EXTENSIONES_NO_SOPORTADAS_WEB:
                resultado["no_soportados"] += 1
                continue
            if ext not in EXTENSIONES_MATERIAL:
                continue

            tipo = self.clasificar_tipo_material(ruta, carpeta)
            if tipo == "proyecto":
                continue

            resultado["total"] += 1
            if self.registro_repo.verificar_material_ingestado(nombre):
                resultado["omitidos"] += 1
                continue
            resultado["pendientes"].append(
                {
                    "nombre": nombre,
                    "ruta": ruta,
                    "tipo": tipo,
                }
            )

        if self.proyectos_service:
            resultado["proyectos"] = self.proyectos_service.escanear_proyectos_en_carpeta(
                materia, carpeta
            )
        else:
            resultado["proyectos"] = []

        return resultado

    def vaciar_materiales(self, borrar_notas_obsidian: bool = True) -> dict[str, Any]:
        """
        Vacía el registro de materiales y de proyectos. Con `borrar_notas_obsidian`, borra
        también las notas que generó cada ingesta (las que figuran en el registro), nunca otras
        notas de la bóveda.
        """
        notas_borradas = 0
        if borrar_notas_obsidian:
            for material in self.registro_repo.listar_materiales():
                nota = material.get("nota")
                if nota and self.boveda_port.eliminar_nota(nota):
                    notas_borradas += 1
        total_materiales = self.registro_repo.vaciar()

        total_proyectos = 0
        if self.proyectos_service:
            total_proyectos = self.proyectos_service.vaciar_proyectos(borrar_notas_obsidian)

        if self.cronograma_repo:
            cronogramas = self.cronograma_repo.listar_cronogramas()
            for materia, clases in cronogramas.items():
                if clases:
                    hubo_cambio = False
                    for c in clases:
                        if c.get("materiales_asociados"):
                            c["materiales_asociados"] = []
                            hubo_cambio = True
                    if hubo_cambio:
                        self.cronograma_repo.guardar_cronograma(materia, clases)
                self.cronograma_repo.limpiar_material_transversal(materia)

        return {
            "total_materiales_eliminados": total_materiales,
            "total_proyectos_eliminados": total_proyectos,
            "notas_obsidian_borradas": notas_borradas,
        }

    def escanear(self, materias: list[str]) -> list[dict[str, Any]]:
        return [self.escanear_materia(m) for m in materias]

    def ingestar_pendientes_stream(self, materias: list[str]) -> Iterator[dict[str, Any]]:
        """Procesa los archivos nuevos de las asignaturas indicadas emitiendo eventos de progreso."""
        escaneos = self.escanear(materias)
        total = sum(len(e["pendientes"]) for e in escaneos)
        yield {"evento": "inicio", "total": total, "materias": materias}

        exitosos = fallidos = 0
        hecho = 0
        for escaneo in escaneos:
            for item in escaneo["pendientes"]:
                hecho += 1
                base = {
                    "evento": "archivo",
                    "indice": hecho,
                    "total": total,
                    "materia": escaneo["materia"],
                    "archivo": item["nombre"],
                    "tipo": item["tipo"],
                }
                try:
                    r = self.ingestar_archivo(
                        item["ruta"], item["nombre"], escaneo["materia"], item["tipo"]
                    )
                    exitosos += 1
                    al = r.get("alineacion") or {}
                    evento: dict[str, Any] = {
                        **base,
                        "ok": True,
                        "clase_asignada": al.get("clase_asignada"),
                        "afinidad": al.get("peso_afinidad"),
                        "ruta_salida": r["ruta_salida"],
                    }
                    if r.get("aviso"):
                        evento["aviso"] = r["aviso"]
                    yield evento
                except Exception as e:
                    fallidos += 1
                    yield {**base, "ok": False, "error": str(e)}

        yield {
            "evento": "fin",
            "exitosos": exitosos,
            "fallidos": fallidos,
            "omitidos": sum(e["omitidos"] for e in escaneos),
        }


__all__ = [
    "EXTENSIONES_MATERIAL",
    "EXTENSIONES_NO_SOPORTADAS_WEB",
    "REGLA_PRIVACIDAD",
    "TIPOS_MATERIAL",
    "IngestaService",
]
