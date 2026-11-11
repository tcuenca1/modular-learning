"""Adaptadores falsos y repositorios en memoria para pruebas unitarias de la capa application."""

from __future__ import annotations

from collections.abc import Callable, Iterator
from typing import Any

from modular_learning.core.domain.cronograma import asignar_ids, buscar_clase
from modular_learning.core.domain.guia_offline import GuiaOffline
from modular_learning.core.domain.materias import Materia, slug_materia
from modular_learning.core.domain.proyectos import HuellaProyecto, Proyecto, TipoProyecto
from modular_learning.core.domain.repaso_espaciado import Tarjeta
from modular_learning.core.ports.boveda import BovedaNotasPort
from modular_learning.core.ports.config import AjustesPort
from modular_learning.core.ports.conversor_pdf import ConversorPdfPort
from modular_learning.core.ports.documentos import LectorDocumentosPort
from modular_learning.core.ports.guias import ExportadorPdfPort, GuiasRepo
from modular_learning.core.ports.llm import LLMPort
from modular_learning.core.ports.plugin_practico import (
    PluginConfigRepoPort,
    PluginMetadatos,
    PluginPracticoBase,
)
from modular_learning.core.ports.proyectos import InspectorProyectosPort, ProyectosRepo
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
        self.cronogramas: dict[str, list[dict[str, Any]]] = {}
        for m, clases in (datos_iniciales or {}).items():
            copia = [dict(c) for c in clases]
            asignar_ids(copia)
            self.cronogramas[m] = copia
        self.transversal: dict[str, list[dict[str, Any]]] = {}
        self.parciales: dict[str, list[dict[str, Any]]] = {}

    def _resolver_clave(self, materia: str) -> str | None:
        slug = slug_materia(materia)
        for k in self.cronogramas:
            if slug_materia(k) == slug:
                return k
        return None

    def obtener_cronograma(self, materia: str) -> list[dict[str, Any]] | None:
        clave = self._resolver_clave(materia)
        if clave is not None:
            return self.cronogramas.get(clave)
        return None

    def guardar_cronograma(self, materia: str, clases: list[dict[str, Any]]) -> str:
        asignar_ids(clases)
        clave = self._resolver_clave(materia) or materia
        self.cronogramas[clave] = list(clases)
        return f"memoria://{clave.replace(' ', '_')}_cronograma.json"

    def actualizar_cronograma(
        self,
        materia: str,
        transformar: Callable[[list[dict[str, Any]]], list[dict[str, Any]] | None],
    ) -> list[dict[str, Any]]:
        clases = self.obtener_cronograma(materia) or []
        resultado = transformar(clases)
        nuevas = clases if resultado is None else resultado
        self.guardar_cronograma(materia, nuevas)
        return nuevas

    def eliminar_cronograma(self, materia: str) -> bool:
        clave = self._resolver_clave(materia)
        if clave and clave in self.cronogramas:
            del self.cronogramas[clave]
            self.parciales.pop(clave, None)
            return True
        return False

    def listar_cronogramas(self) -> dict[str, list[dict[str, Any]]]:
        return {slug_materia(k): v for k, v in self.cronogramas.items()}

    def obtener_proximas_clases(self, materia: str) -> list[dict[str, Any]]:
        clases = self.obtener_cronograma(materia) or []
        pendientes = [c for c in clases if c.get("estado", "").lower() != "completado"]
        for c in pendientes:
            c.setdefault("subtemas_adicionales", [])
            c.setdefault("materiales_asociados", [])
        return pendientes[:5]

    def obtener_detalle_clase(
        self, materia: str, tema: str | None = None, clase_id: str | None = None
    ) -> dict[str, Any]:
        clases = self.obtener_cronograma(materia) or []
        clase = buscar_clase(clases, clase_id=clase_id, tema=tema)
        if clase is not None:
            clase.setdefault("subtemas_adicionales", [])
            clase.setdefault("materiales_asociados", [])
            return clase
        return {"subtemas_adicionales": [], "materiales_asociados": []}

    def marcar_clase(
        self,
        materia: str,
        clase_id: str | None = None,
        tema: str | None = None,
        estado: str = "completado",
    ) -> bool:
        clases = self.obtener_cronograma(materia) or []
        clase = buscar_clase(clases, clase_id=clase_id, tema=tema)
        if clase is not None:
            clase["estado"] = estado
            return True
        return False

    def marcar_clase_completada(
        self, materia: str, tema_exacto: str, clase_id: str | None = None
    ) -> bool:
        return self.marcar_clase(materia, clase_id=clase_id, tema=tema_exacto, estado="completado")

    def agregar_material_transversal(self, materia: str, item: dict[str, Any]) -> None:
        clave = self._resolver_clave(materia) or materia
        self.transversal.setdefault(clave, []).append(item)

    def quitar_material_transversal(self, materia: str, nombre_archivo: str) -> bool:
        clave = self._resolver_clave(materia) or materia
        items = self.transversal.get(clave, [])
        restantes = [i for i in items if i.get("archivo") != nombre_archivo]
        if len(restantes) == len(items):
            return False
        self.transversal[clave] = restantes
        return True

    def limpiar_material_transversal(self, materia: str) -> None:
        clave = self._resolver_clave(materia) or materia
        self.transversal[clave] = []

    def obtener_parciales(self, materia: str) -> list[dict[str, Any]]:
        clave = self._resolver_clave(materia) or materia
        return list(self.parciales.get(clave, []))

    def guardar_parciales(self, materia: str, parciales: list[dict[str, Any]]) -> None:
        clave = self._resolver_clave(materia) or materia
        self.parciales[clave] = list(parciales)


class InMemoryMateriaRepo(MateriaRepo):
    """Repositorio de asignaturas en memoria."""

    def __init__(self, materias_iniciales: list[str | Materia] | None = None) -> None:
        self.materias: list[Materia] = []
        for m in materias_iniciales or []:
            if isinstance(m, Materia):
                self.guardar(m)
            else:
                self.guardar(Materia.desde_nombre(str(m)))

    def listar(self) -> list[Materia]:
        return list(self.materias)

    def guardar(self, materia: Materia) -> None:
        for i, m in enumerate(self.materias):
            if m.slug == materia.slug:
                self.materias[i] = materia
                return
        self.materias.append(materia)

    def eliminar(self, slug: str) -> bool:
        buscado = slug_materia(slug)
        restantes = [m for m in self.materias if m.slug != buscado]
        if len(restantes) == len(self.materias):
            return False
        self.materias = restantes
        return True

    def cargar_materias(self) -> list[str]:
        return [m.nombre for m in self.materias]

    def agregar_materia(self, nueva_materia: str) -> None:
        if nueva_materia and nueva_materia.strip():
            materia = Materia.desde_nombre(nueva_materia.strip())
            if any(m.slug == materia.slug for m in self.materias):
                return
            self.materias.append(materia)


class InMemoryRegistroMaterialesRepo(RegistroMaterialesRepo):
    """Repositorio de registro de materiales en memoria."""

    def __init__(self) -> None:
        self.registros: list[dict[str, Any]] = []

    def verificar_material_ingestado(self, nombre_archivo: str) -> bool:
        buscado = nombre_archivo.lower()
        return any(r.get("nombre", "").lower() == buscado for r in self.registros)

    def registrar_material(
        self, nombre_archivo: str, materia: str, nota: str | None = None
    ) -> None:
        buscado = nombre_archivo.lower()
        self.registros = [r for r in self.registros if r.get("nombre", "").lower() != buscado]
        entrada = {"nombre": nombre_archivo, "materia": materia}
        if nota:
            entrada["nota"] = nota
        self.registros.append(entrada)

    def listar_materiales(self) -> list[dict[str, Any]]:
        return list(self.registros)

    def eliminar_material(self, nombre_archivo: str) -> dict[str, Any] | None:
        buscado = nombre_archivo.lower()
        for i, r in enumerate(self.registros):
            if r.get("nombre", "").lower() == buscado:
                return self.registros.pop(i)
        return None

    def eliminar_de_materia(self, materia: str) -> int:
        slug = slug_materia(materia)
        restantes = [r for r in self.registros if slug_materia(r.get("materia", "")) != slug]
        quitados = len(self.registros) - len(restantes)
        self.registros = restantes
        return quitados

    def vaciar(self) -> int:
        total = len(self.registros)
        self.registros.clear()
        return total


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

    def eliminar_nota(self, ruta: str, ruta_boveda: str | None = None) -> bool:
        if ruta in self.notas:
            del self.notas[ruta]
            return True
        return False


class InMemoryLectorDocumentosPort(LectorDocumentosPort):
    """Adaptador de lectura de documentos y plantillas en memoria."""

    def __init__(self, plantillas: dict[str, str] | None = None) -> None:
        self.plantillas: dict[str, str] = {
            "01_roadmap_aprendizaje.md": "Genera roadmap para {tema}. Objetivo: {objetivo}",
            "02_explicacion_tema.md": "Explica tema: {tema}. Nivel: {nivel_profundidad}. Contexto: {contexto_roadmap}",
            "03_resumen_evaluacion.md": "Resume {materia}. Contenido: {contenido_apuntes}",
            "04_extraccion_silabo.md": "Extrae cronograma para {materia}:\n{contenido_texto}",
            "06_guia_offline.md": (
                "Guía de {tema} ({materia}). Objetivo: {objetivo}. Contenido: {contenido}. "
                "Subtemas: {subtemas}. Extensión: {extension}. Marcador: {marcador}"
            ),
            **(plantillas or {}),
        }
        self.materiales: dict[str, str] = {}
        # Carpetas que existen aunque no tengan archivos en `materiales`
        self.carpetas: set[str] = set()

    def leer_prompt(self, nombre_archivo: str) -> str:
        return self.plantillas.get(nombre_archivo, f"Prompt simulado para {nombre_archivo}")

    def leer_material_estudio(self, ruta_archivo: str) -> str:
        return self.materiales.get(ruta_archivo, "Contenido simulado de material.")

    def extraer_texto(self, ruta_archivo: str) -> str:
        return self.materiales.get(ruta_archivo, "Contenido simulado de material.")

    def listar_archivos(self, carpeta: str, recursivo: bool = True) -> list[str] | None:
        c_norm = carpeta.replace("\\", "/").rstrip("/") + "/"
        encontrados = [r for r in self.materiales if r.replace("\\", "/").startswith(c_norm)]
        if not recursivo:
            encontrados = [r for r in encontrados if "/" not in r.replace("\\", "/")[len(c_norm) :]]
        if not encontrados and c_norm.rstrip("/") not in {
            c.replace("\\", "/").rstrip("/") for c in self.carpetas
        }:
            return None
        return sorted(encontrados)


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

    def eliminar(self, ids: list[str]) -> int:
        quitadas = [i for i in ids if self.tarjetas.pop(i, None) is not None]
        return len(quitadas)


class InMemoryHistorialRepo(HistorialRepo):
    """Historial de estudio en memoria."""

    def __init__(self) -> None:
        self.eventos: list[dict[str, Any]] = []

    def registrar(self, evento: dict[str, Any]) -> None:
        self.eventos.append(evento)

    def listar(self, materia: str | None = None, tema: str | None = None) -> list[dict[str, Any]]:
        m_slug = slug_materia(materia) if materia else None
        return [
            e
            for e in reversed(self.eventos)
            if (m_slug is None or slug_materia(e.get("materia", "")) == m_slug)
            and (tema is None or e.get("tema") == tema)
        ]

    def eliminar(self, criterio: Callable[[dict[str, Any]], bool]) -> int:
        restantes = [e for e in self.eventos if not criterio(e)]
        quitados = len(self.eventos) - len(restantes)
        self.eventos = restantes
        return quitados


class InMemoryGuiasRepo(GuiasRepo):
    """Guías de estudio offline en memoria."""

    def __init__(self) -> None:
        self.guias: dict[str, GuiaOffline] = {}

    def listar(self) -> list[GuiaOffline]:
        return sorted(self.guias.values(), key=lambda g: g.creada, reverse=True)

    def obtener(self, guia_id: str) -> GuiaOffline | None:
        return self.guias.get(guia_id)

    def guardar(self, guia: GuiaOffline) -> None:
        self.guias[guia.id] = guia

    def eliminar(self, ids: list[str]) -> int:
        quitadas = [i for i in ids if self.guias.pop(i, None) is not None]
        return len(quitadas)


class InMemoryExportadorPdfPort(ExportadorPdfPort):
    """Generador simulado de PDF para pruebas."""

    def __init__(self, salida_bytes: bytes = b"%PDF-1.4 mock pdf content") -> None:
        self.salida_bytes = salida_bytes
        self.guias_exportadas: list[GuiaOffline] = []

    def exportar_guia(self, guia: GuiaOffline) -> bytes:
        self.guias_exportadas.append(guia)
        return self.salida_bytes


class FakePluginPractico(PluginPracticoBase):
    """Plugin práctico falso: registra lo que el servicio le pide y no toca el disco."""

    def __init__(
        self,
        metadatos: PluginMetadatos,
        contexto: str = "",
        analiza_archivos: bool = True,
    ) -> None:
        self._metadatos = metadatos
        self.contexto = contexto
        self.analiza_archivos = analiza_archivos
        self.carpetas_analizadas: list[str] = []
        self.archivos_analizados: list[str] = []

    @property
    def metadatos(self) -> PluginMetadatos:
        return self._metadatos

    def obtener_instrucciones_ia(self) -> str:
        return f"[INSTRUCCIONES {self._metadatos.id}]"

    def generar_ejercicio_base(self, tema: str) -> str:
        return f"[EJERCICIO {self._metadatos.id}: {tema}]"

    def guardar_contexto_extraido(self, metadatos: str) -> None:
        self.contexto = metadatos

    def cargar_contexto_reciente(self) -> str:
        return self.contexto

    def analizar_carpeta(self, ruta_carpeta: str) -> str:
        self.carpetas_analizadas.append(ruta_carpeta)
        return f"Carpeta {ruta_carpeta} analizada por {self._metadatos.id}"

    def analizar_archivo(self, ruta_archivo: str) -> str | None:
        if not self.analiza_archivos:
            return None
        self.archivos_analizados.append(ruta_archivo)
        return f"Archivo {ruta_archivo} analizado por {self._metadatos.id}"


class InMemoryPluginConfigRepo(PluginConfigRepoPort):
    """Configuraciones de plugins en memoria para pruebas unitarias."""

    def __init__(self, configs: dict[str, dict[str, Any]] | None = None) -> None:
        self.configs: dict[str, dict[str, Any]] = dict(configs or {})

    def obtener_configuraciones(self) -> dict[str, dict[str, Any]]:
        return dict(self.configs)

    def guardar_configuracion(
        self, clave: str, carpeta: str | None = None, materia: str | None = None
    ) -> dict[str, Any]:
        clave_norm = clave.lower().strip()
        actual = dict(self.configs.get(clave_norm, {}))
        if carpeta is not None:
            actual["carpeta"] = carpeta.strip()
        if materia is not None:
            actual["materia"] = materia.strip()
        self.configs[clave_norm] = actual
        return actual


class InMemoryProyectosRepo(ProyectosRepo):
    """Repositorio en memoria de proyectos para pruebas unitarias."""

    def __init__(self, proyectos: list[Proyecto] | None = None) -> None:
        self.proyectos: dict[str, Proyecto] = {p.id: p for p in (proyectos or [])}

    def guardar(self, proyecto: Proyecto) -> None:
        self.proyectos[proyecto.id] = proyecto

    def obtener(self, id_proyecto: str) -> Proyecto | None:
        return self.proyectos.get(id_proyecto)

    def listar(self, materia: str | None = None) -> list[Proyecto]:
        lista = list(self.proyectos.values())
        if materia:
            buscado = slug_materia(materia)
            lista = [p for p in lista if slug_materia(p.materia) == buscado]
        return sorted(lista, key=lambda p: (p.materia, p.parcial, p.nombre))

    def eliminar(self, id_proyecto: str) -> bool:
        return self.proyectos.pop(id_proyecto, None) is not None

    def vaciar(self) -> int:
        total = len(self.proyectos)
        self.proyectos.clear()
        return total


class InMemoryInspectorProyectos(InspectorProyectosPort):
    """Proyectos en disco simulados: {ruta: (tipo, huella)} y candidatos por carpeta."""

    def __init__(self) -> None:
        self.proyectos: dict[str, tuple[TipoProyecto, HuellaProyecto]] = {}
        self.candidatos: dict[str, list[dict[str, Any]]] = {}

    def escanear(self, carpeta_materia: str) -> list[dict[str, Any]]:
        return [dict(c) for c in self.candidatos.get(carpeta_materia, [])]

    def huella(self, ruta: str) -> HuellaProyecto | None:
        datos = self.proyectos.get(ruta)
        return datos[1] if datos else None

    def detectar_tipo(self, ruta: str) -> TipoProyecto:
        datos = self.proyectos.get(ruta)
        return datos[0] if datos else "documento_rector"

    def extraer_contexto(self, ruta: str) -> str:
        return f"Contexto simulado de {ruta}"


class FakeConversorPdfPort(ConversorPdfPort):
    """Conversor a PDF simulado para pruebas unitarias."""

    def __init__(self, ruta_retorno: str | None = None) -> None:
        self.ruta_retorno = ruta_retorno
        self.archivos_convertidos: list[str] = []
        self.temporales_borrados: list[str] = []

    def convertir_a_pdf(self, ruta_archivo: str) -> str | None:
        self.archivos_convertidos.append(ruta_archivo)
        return self.ruta_retorno

    def borrar_temporal(self, ruta_pdf: str) -> None:
        self.temporales_borrados.append(ruta_pdf)
