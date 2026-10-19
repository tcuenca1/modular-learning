"""Servicio de aplicación para ingesta y anonimización de material de estudio (`ml im`)."""

from __future__ import annotations

import mimetypes
import os
import time
from collections.abc import Iterator
from typing import Any

from modular_learning.core.domain import alineador_curricular
from modular_learning.core.ports.boveda import BovedaNotasPort
from modular_learning.core.ports.config import AjustesPort
from modular_learning.core.ports.documentos import LectorDocumentosPort
from modular_learning.core.ports.llm import LLMPort
from modular_learning.core.ports.repositorios import CronogramaRepo, RegistroMaterialesRepo

EXTENSIONES_MATERIAL = (".pdf", ".docx", ".txt", ".md")
EXTENSIONES_NO_SOPORTADAS_WEB = (".pptx",)
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
        plugins_service: Any | None = None,
        cronograma_repo: CronogramaRepo | None = None,
    ):
        self.llm = llm
        self.registro_repo = registro_repo
        self.boveda_port = boveda_port
        self.lector_docs = lector_docs
        self.ajustes_port = ajustes_port
        self.plugins_service = plugins_service
        self.cronograma_repo = cronograma_repo

    def clasificar_tipo_material(self, ruta_archivo: str, ruta_raiz_lote: str) -> str:
        """Clasifica el material según su ubicación en la carpeta de la asignatura."""
        rel_path = os.path.relpath(ruta_archivo, ruta_raiz_lote)
        if len(rel_path.split(os.sep)) == 1:
            return "actividad"
        ruta_upper = rel_path.upper()
        if "MATERIAL DE ESTUDIO" in ruta_upper:
            return "diapositiva"
        if "MATERIAL ADICIONAL" in ruta_upper:
            return "lectura"
        return "material_complementario"

    def _leer_docx(self, ruta: str) -> str:
        import docx

        documento = docx.Document(ruta)
        return "\n".join(p.text for p in documento.paragraphs)

    def _generar_contenido(self, ruta: str, prompt: str) -> str:
        ext = os.path.splitext(ruta)[1].lower()
        if ext == ".docx":
            texto = self._leer_docx(ruta)
            return self.llm.generar_texto(f"{prompt}\n\nCONTENIDO DEL DOCUMENTO:\n{texto}")
        if ext in (".txt", ".md"):
            with open(ruta, encoding="utf-8", errors="replace") as f:
                return self.llm.generar_texto(f"{prompt}\n\nCONTENIDO DEL DOCUMENTO:\n{f.read()}")

        mime = "application/pdf" if ext == ".pdf" else (mimetypes.guess_type(ruta)[0] or "text/plain")
        with open(ruta, "rb") as f:
            datos = f.read()
        return self.llm.generar_texto_con_archivo({"mime_type": mime, "data": datos, "path": ruta}, prompt)

    def ingestar_archivo(
        self,
        ruta_archivo: str,
        nombre_original: str,
        materia: str,
        tipo: str = "material_complementario",
    ) -> dict[str, Any]:
        """Ingesta un archivo individual, extrae contenido anonimizado y lo sincroniza."""
        if tipo not in TIPOS_MATERIAL:
            tipo = "material_complementario"

        if self.ajustes_port:
            ruta_boveda = self.ajustes_port.ruta_boveda()
        else:
            from modular_learning.core.application import configuracion as servicio_config

            ruta_boveda = servicio_config.ruta_boveda()
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

        contenido_md = self._generar_contenido(ruta_archivo, prompt)

        carpeta_salida = os.path.join(ruta_boveda, materia, tipo.capitalize())
        os.makedirs(carpeta_salida, exist_ok=True)
        base = os.path.splitext(nombre_original)[0].replace(" ", "_")
        ruta_salida = os.path.join(carpeta_salida, f"{base}_Notas.md")
        with open(ruta_salida, "w", encoding="utf-8") as f:
            f.write(contenido_md)

        self.registro_repo.registrar_material(nombre_original, materia)

        alineacion: dict[str, Any] = {}
        try:
            alineacion = alineador_curricular.asignar_material_a_clase(
                materia, contenido_md, nombre_original, llm=self.llm
            )
        except Exception as e:
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
                except Exception:
                    pass

        return {
            "archivo": nombre_original,
            "materia": materia,
            "tipo": tipo,
            "ruta_salida": os.path.abspath(ruta_salida),
            "contenido_md": contenido_md,
            "alineacion": alineacion,
            "plugin_actualizado": plugin_actualizado,
        }

    def escanear_materia(self, materia: str) -> dict[str, Any]:
        from modular_learning.core.application import configuracion as servicio_config
        from modular_learning.core.application.configuracion import _orig_carpeta_material

        if getattr(servicio_config, "carpeta_material", None) is not _orig_carpeta_material:
            base_carpeta = servicio_config.carpeta_material()
        elif self.ajustes_port:
            base_carpeta = self.ajustes_port.carpeta_material()
        else:
            base_carpeta = servicio_config.carpeta_material()
        carpeta = os.path.join(base_carpeta, materia)
        resultado: dict[str, Any] = {
            "materia": materia,
            "carpeta": carpeta,
            "existe": os.path.isdir(carpeta),
            "total": 0,
            "omitidos": 0,
            "no_soportados": 0,
            "pendientes": [],
        }
        if not resultado["existe"]:
            return resultado

        for raiz, _, archivos in os.walk(carpeta):
            for nombre in sorted(archivos):
                ext = os.path.splitext(nombre)[1].lower()
                if ext in EXTENSIONES_NO_SOPORTADAS_WEB:
                    resultado["no_soportados"] += 1
                    continue
                if ext not in EXTENSIONES_MATERIAL:
                    continue
                resultado["total"] += 1
                if self.registro_repo.verificar_material_ingestado(nombre):
                    resultado["omitidos"] += 1
                    continue
                ruta = os.path.join(raiz, nombre)
                resultado["pendientes"].append(
                    {"nombre": nombre, "ruta": ruta, "tipo": self.clasificar_tipo_material(ruta, carpeta)}
                )
        return resultado

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
                    r = self.ingestar_archivo(item["ruta"], item["nombre"], escaneo["materia"], item["tipo"])
                    exitosos += 1
                    al = r.get("alineacion") or {}
                    yield {
                        **base,
                        "ok": True,
                        "clase_asignada": al.get("clase_asignada"),
                        "afinidad": al.get("peso_afinidad"),
                        "ruta_salida": r["ruta_salida"],
                    }
                except Exception as e:
                    fallidos += 1
                    yield {**base, "ok": False, "error": str(e)}

        yield {
            "evento": "fin",
            "exitosos": exitosos,
            "fallidos": fallidos,
            "omitidos": sum(e["omitidos"] for e in escaneos),
        }


_instancia_por_defecto: IngestaService | None = None


def configurar_servicio_defecto(servicio: IngestaService) -> None:
    global _instancia_por_defecto
    _instancia_por_defecto = servicio


def ingestar_archivo(
    ruta_archivo: str, nombre_original: str, materia: str, tipo: str = "material_complementario"
) -> dict[str, Any]:
    if _instancia_por_defecto is None:
        raise RuntimeError("IngestaService no inicializado en el contenedor.")
    return _instancia_por_defecto.ingestar_archivo(ruta_archivo, nombre_original, materia, tipo)


def escanear(materias: list[str]) -> list[dict[str, Any]]:
    if _instancia_por_defecto is None:
        raise RuntimeError("IngestaService no inicializado en el contenedor.")
    return _instancia_por_defecto.escanear(materias)


def ingestar_pendientes_stream(materias: list[str]) -> Iterator[dict[str, Any]]:
    if _instancia_por_defecto is None:
        raise RuntimeError("IngestaService no inicializado en el contenedor.")
    return _instancia_por_defecto.ingestar_pendientes_stream(materias)


__all__ = [
    "EXTENSIONES_MATERIAL",
    "EXTENSIONES_NO_SOPORTADAS_WEB",
    "REGLA_PRIVACIDAD",
    "TIPOS_MATERIAL",
    "IngestaService",
    "configurar_servicio_defecto",
    "escanear",
    "ingestar_archivo",
    "ingestar_pendientes_stream",
]
