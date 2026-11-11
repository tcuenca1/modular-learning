from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class PluginMetadatos:
    """
    Lo que el servicio necesita saber de un plugin sin conocerlo: cómo se presenta, con qué
    asignaturas se asocia y cómo se sincroniza. Cada plugin declara el suyo; el núcleo no
    contiene nombres de asignaturas.
    """

    id: str
    nombre: str
    opcion_key: str
    categoria: str
    descripcion: str
    # Slug de la asignatura a la que se asocia si el usuario no configuró otra
    materia_defecto: str
    # Fragmentos que, dentro de la selección del usuario, activan este plugin
    claves_seleccion: tuple[str, ...] = ()
    # Valores de `tipo_plugin` que procesan archivos sueltos con `analizar_archivo`
    tipos_archivo: tuple[str, ...] = ()
    # Palabras que, dentro del nombre de una asignatura, la asocian a este plugin
    palabras_clave: tuple[str, ...] = ()
    # Carpeta (bajo el material y la bóveda) donde se busca si no hay carpeta configurada
    carpeta_convencional: str = ""
    # Si se indica, la sincronización busca archivos con esta extensión y los analiza uno a uno
    extension_archivos: str | None = None
    # Presentación del resultado de la sincronización
    etiqueta: str = ""
    titulo_carpeta_asignada: str = "Carpeta Asignada"
    titulo_carpeta_convencional: str = "Carpeta de Materia"
    titulo_sincronizacion: str = "Sincronización"
    texto_sin_contexto: str = "Sin contexto registrado."
    limite_contexto: int | None = None
    # Orden en que aparece al sincronizar varios plugins a la vez
    orden_sincronizacion: int = 0


class PluginPracticoBase(ABC):
    """
    Puerto base (Abstract Base Class) para la arquitectura hexagonal de plugins prácticos.
    Define la interfaz estándar que todos los adaptadores de materias prácticas deben implementar.
    El servicio solo invoca lo declarado aquí: no distingue entre plugins concretos.
    """

    @property
    @abstractmethod
    def metadatos(self) -> PluginMetadatos:
        """Identidad, asociación con asignaturas y forma de sincronizarse del plugin."""

    @abstractmethod
    def analizar_carpeta(self, ruta_carpeta: str) -> str:
        """Analiza una carpeta de trabajo del estudiante y devuelve un resumen en Markdown."""

    def analizar_archivo(self, ruta_archivo: str) -> str | None:
        """Analiza un archivo suelto; devuelve None si el plugin no analiza archivos sueltos."""
        return None

    @abstractmethod
    def obtener_instrucciones_ia(self) -> str:
        """Devuelve las directivas y restricciones de system prompt específicas de la herramienta práctica."""

    @abstractmethod
    def generar_ejercicio_base(self, tema: str) -> str:
        """Devuelve el contexto técnico inicial, plantilla o boilerplate práctico para el tema indicado."""

    @abstractmethod
    def guardar_contexto_extraido(self, metadatos: str) -> None:
        """Guarda y acumula contexto técnico extraído de materiales ingestados (historial máx. 5)."""

    @abstractmethod
    def cargar_contexto_reciente(self) -> str:
        """Carga el contexto técnico reciente guardado para inyectarlo al system prompt de la IA."""


class PluginConfigRepoPort(ABC):
    """Puerto para persistir la configuración de carpetas y materias de los plugins prácticos."""

    @abstractmethod
    def obtener_configuraciones(self) -> dict[str, dict[str, Any]]:
        """Retorna todas las configuraciones almacenadas por clave de plugin."""

    @abstractmethod
    def guardar_configuracion(
        self, clave: str, carpeta: str | None = None, materia: str | None = None
    ) -> dict[str, Any]:
        """Guarda o actualiza la configuración para el plugin indicado."""


__all__ = ["PluginConfigRepoPort", "PluginMetadatos", "PluginPracticoBase"]
