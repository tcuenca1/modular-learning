"""Adaptadores falsos y repositorios en memoria para pruebas unitarias de la capa application."""

from __future__ import annotations

import os
from collections.abc import Iterator
from typing import Any

from modular_learning.core.domain.repaso_espaciado import Tarjeta
from modular_learning.core.ports.boveda import BovedaNotasPort
from modular_learning.core.ports.config import AjustesPort
from modular_learning.core.ports.documentos import LectorDocumentosPort
from modular_learning.core.ports.llm import LLMPort
from modular_learning.core.ports.repaso import HistorialRepo, TarjetasRepo
from modular_learning.core.ports.repositorios import (
    CronogramaRepo,
    MateriaRepo,
    RegistroMaterialesRepo,
)


class FakeLLM(LLMPort):
    """Implementación de LLMPort en memoria controlable para pruebas."""

    def __init__(
        self,
        texto_default: str = "Respuesta simulada del LLM.",
        json_default: dict[str, Any] | list[Any] | None = None,
        stream_chunks: list[str] | None = None,
    ) -> None:
        self.texto_default = texto_default
        self.json_default = json_default or {
            "pasos": [{"titulo": "Paso 1", "descripcion": "Desc 1"}]
        }
        self.stream_chunks = stream_chunks or ["Chunk 1 ", "Chunk 2"]
        self.llamadas_texto: list[dict[str, Any]] = []
        self.llamadas_json: list[str] = []
        self.llamadas_stream: list[dict[str, Any]] = []

    def generar_texto(self, prompt: str, contexto_previo: list[dict] | None = None) -> str:
        self.llamadas_texto.append({"prompt": prompt, "contexto": contexto_previo})
        return self.texto_default

    def generar_texto_con_archivo(self, archivo_inline: dict, prompt: str) -> str:
        self.llamadas_texto.append({"archivo": archivo_inline, "prompt": prompt})
        return self.texto_default

    def generar_json_estructurado(self, prompt: str) -> dict[str, Any] | list[Any]:
        self.llamadas_json.append(prompt)
        return self.json_default

    def generar_respuesta_stream(
        self, prompt: str, contexto_previo: list[dict] | None = None
    ) -> Iterator[str]:
        self.llamadas_stream.append({"prompt": prompt, "contexto": contexto_previo})
        yield from self.stream_chunks


class InMemoryCronogramaRepo(CronogramaRepo):
    """Repositorio de cronogramas en memoria."""

    def __init__(self, datos_iniciales: dict[str, list[dict[str, Any]]] | None = None) -> None:
        self.cronogramas: dict[str, list[dict[str, Any]]] = dict(datos_iniciales or {})
        self.transversal: dict[str, list[dict[str, Any]]] = {}

    def obtener_proximas_clases(self, materia: str) -> list[dict[str, Any]]:
        clases = self.cronogramas.get(materia, [])
        return [c for c in clases if c.get("estado", "").lower() != "completado"]

    def obtener_detalle_clase(self, materia: str, tema: str) -> dict[str, Any]:
        clases = self.cronogramas.get(materia, [])
        for c in clases:
            if c.get("tema", "").strip().lower() == tema.strip().lower():
                return c
        return {}

    def marcar_clase_completada(self, materia: str, tema_exacto: str) -> bool:
        clases = self.cronogramas.get(materia, [])
        for c in clases:
            if c.get("tema", "").strip().lower() == tema_exacto.strip().lower():
                c["estado"] = "completado"
                return True
        return False

    def obtener_cronograma(self, materia: str) -> list[dict[str, Any]] | None:
        return self.cronogramas.get(materia)

    def guardar_cronograma(self, materia: str, clases: list[dict[str, Any]]) -> str:
        self.cronogramas[materia] = list(clases)
        return f"memoria://{materia.replace(' ', '_')}_cronograma.json"

    def listar_cronogramas(self) -> dict[str, list[dict[str, Any]]]:
        return dict(self.cronogramas)

    def agregar_material_transversal(self, materia: str, item: dict[str, Any]) -> None:
        self.transversal.setdefault(materia, []).append(item)


class InMemoryMateriaRepo(MateriaRepo):
    """Repositorio de asignaturas en memoria."""

    def __init__(self, materias_iniciales: list[str] | None = None) -> None:
        self.materias: list[str] = list(materias_iniciales or [])

    def cargar_materias(self) -> list[str]:
        return list(self.materias)

    def agregar_materia(self, nueva_materia: str) -> None:
        if nueva_materia and nueva_materia not in self.materias:
            self.materias.append(nueva_materia)


class InMemoryRegistroMaterialesRepo(RegistroMaterialesRepo):
    """Repositorio de registro de materiales en memoria."""

    def __init__(self) -> None:
        self.ingestados: set[str] = set()

    def verificar_material_ingestado(self, nombre_archivo: str) -> bool:
        return nombre_archivo in self.ingestados

    def registrar_material(self, nombre_archivo: str, materia: str) -> None:
        self.ingestados.add(nombre_archivo)


class InMemoryBovedaPort(BovedaNotasPort):
    """Adaptador de Boveda de Obsidian en memoria."""

    def __init__(self) -> None:
        self.resumenes: dict[tuple[str, str], str] = {}
        self.notas: dict[str, str] = {}
        self.indices_actualizados: list[tuple[str, str]] = []

    def guardar_resumen(
        self, materia: str, tema: str, contenido: str, ruta_boveda: str | None = None
    ) -> bool:
        self.resumenes[(materia, tema)] = contenido
        return True

    def guardar_nota(
        self,
        materia: str,
        subcarpeta: str,
        nombre_base: str,
        contenido: str,
        ruta_boveda: str | None = None,
    ) -> str:
        ruta = f"{ruta_boveda or 'memoria://boveda'}/{materia}/{subcarpeta}/{nombre_base}.md"
        self.notas[ruta] = contenido
        return ruta

    def actualizar_indice_materia(
        self, materia: str, tema_sanitizado: str, ruta_boveda: str | None = None
    ) -> bool:
        self.indices_actualizados.append((materia, tema_sanitizado))
        return True


class InMemoryLectorDocumentosPort(LectorDocumentosPort):
    """Adaptador de lectura de documentos y plantillas en memoria."""

    def __init__(self, plantillas: dict[str, str] | None = None) -> None:
        self.plantillas: dict[str, str] = {
            "01_roadmap_aprendizaje.md": "Genera roadmap para {tema}. Objetivo: {objetivo}",
            "02_explicacion_tema.md": "Explica tema: {tema}. Nivel: {nivel_profundidad}. Contexto: {contexto_roadmap}",
            "03_resumen_evaluacion.md": "Resume {materia}. Contenido: {contenido_apuntes}",
            "04_extraccion_silabo.md": "Extrae cronograma para {materia}:\n{contenido_texto}",
            **(plantillas or {}),
        }
        self.materiales: dict[str, str] = {}

    def leer_prompt(self, nombre_archivo: str) -> str:
        return self.plantillas.get(nombre_archivo, f"Prompt simulado para {nombre_archivo}")

    def leer_material_estudio(self, ruta_archivo: str) -> str:
        return self.materiales.get(ruta_archivo, "Contenido simulado de material.")

    def extraer_texto(self, ruta_archivo: str) -> str:
        return self.materiales.get(ruta_archivo, "Contenido simulado de material.")

    def listar_archivos(self, carpeta: str, recursivo: bool = True) -> list[str] | None:
        prefijo = carpeta.rstrip("/\\") + os.sep
        encontrados = [r for r in self.materiales if r.startswith(prefijo)]
        if not recursivo:
            encontrados = [r for r in encontrados if os.sep not in r[len(prefijo) :]]
        return sorted(encontrados) if encontrados else None


class InMemoryAjustesPort(AjustesPort):
    """Adaptador de ajustes en memoria."""

    def __init__(
        self,
        carpeta_mat: str = "/simulado/material",
        ruta_bov: str = "/simulado/boveda",
        configurado: bool = True,
    ) -> None:
        self._carpeta_mat = carpeta_mat
        self._ruta_bov = ruta_bov
        self._configurado = configurado

    def esta_configurado(self) -> bool:
        return self._configurado

    def carpeta_material(self) -> str:
        return self._carpeta_mat

    def ruta_boveda(self) -> str:
        return self._ruta_bov

    def obtener_ajustes(self) -> dict[str, Any]:
        return {
            "configurado": self._configurado,
            "carpeta_material": self._carpeta_mat,
            "ruta_obsidian": self._ruta_bov,
            "existe_carpeta_material": True,
            "existe_ruta_obsidian": True,
        }

    def guardar_ajustes(
        self, carpeta_material_nueva: str, ruta_obsidian_nueva: str
    ) -> dict[str, Any]:
        self._carpeta_mat = carpeta_material_nueva
        self._ruta_bov = ruta_obsidian_nueva
        self._configurado = True
        return self.obtener_ajustes()


class InMemoryTarjetasRepo(TarjetasRepo):
    """Tarjetas de repaso espaciado en memoria."""

    def __init__(self) -> None:
        self.tarjetas: dict[str, Tarjeta] = {}

    def listar(self) -> list[Tarjeta]:
        return list(self.tarjetas.values())

    def obtener(self, tarjeta_id: str) -> Tarjeta | None:
        return self.tarjetas.get(tarjeta_id)

    def guardar(self, tarjeta: Tarjeta) -> None:
        self.tarjetas[tarjeta.id] = tarjeta


class InMemoryHistorialRepo(HistorialRepo):
    """Historial de estudio en memoria."""

    def __init__(self) -> None:
        self.eventos: list[dict[str, Any]] = []

    def registrar(self, evento: dict[str, Any]) -> None:
        self.eventos.append(evento)

    def listar(self, materia: str | None = None, tema: str | None = None) -> list[dict[str, Any]]:
        return [
            e
            for e in reversed(self.eventos)
            if (materia is None or e.get("materia") == materia)
            and (tema is None or e.get("tema") == tema)
        ]
