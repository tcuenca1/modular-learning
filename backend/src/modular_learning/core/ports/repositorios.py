"""Contratos de persistencia y repositorios para el dominio académico."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any

from modular_learning.core.domain.materias import Materia


class CronogramaRepo(ABC):
    """
    Puerto de repositorio de los cronogramas, uno por asignatura e identificado por su slug.
    Garantiza que cada clase guardada tenga un `id` estable (ver `domain.cronograma`).
    """

    @abstractmethod
    def obtener_cronograma(self, materia: str) -> list[dict[str, Any]] | None:
        """Retorna la lista completa de clases del cronograma de la materia."""

    @abstractmethod
    def guardar_cronograma(self, materia: str, clases: list[dict[str, Any]]) -> str:
        """Guarda o actualiza la lista completa de clases y retorna la ubicación persistida."""

    @abstractmethod
    def actualizar_cronograma(
        self,
        materia: str,
        transformar: Callable[[list[dict[str, Any]]], list[dict[str, Any]] | None],
    ) -> list[dict[str, Any]]:
        """
        Lee las clases (lista vacía si no hay cronograma), aplica `transformar` y guarda el
        resultado como una sola operación atómica respecto a otras escrituras del mismo
        cronograma. `transformar` modifica la lista en sitio o retorna una lista nueva; si
        lanza una excepción no se guarda nada y la excepción se propaga. Retorna las clases
        guardadas.
        """

    @abstractmethod
    def eliminar_cronograma(self, materia: str) -> bool:
        """Elimina el cronograma de la materia; retorna False si no existía."""

    @abstractmethod
    def listar_cronogramas(self) -> dict[str, list[dict[str, Any]]]:
        """Retorna todos los cronogramas registrados como {slug_o_nombre: clases}."""

    @abstractmethod
    def obtener_proximas_clases(self, materia: str) -> list[dict[str, Any]]:
        """Retorna las próximas clases pendientes del cronograma de la materia."""

    @abstractmethod
    def obtener_detalle_clase(
        self, materia: str, tema: str | None = None, clase_id: str | None = None
    ) -> dict[str, Any]:
        """Obtiene la información detallada de una clase por su id o por su tema."""

    @abstractmethod
    def marcar_clase_completada(
        self, materia: str, tema_exacto: str, clase_id: str | None = None
    ) -> bool:
        """Marca una clase específica como completada en el cronograma."""

    @abstractmethod
    def marcar_clase(
        self,
        materia: str,
        clase_id: str | None = None,
        tema: str | None = None,
        estado: str = "completado",
    ) -> bool:
        """Actualiza el estado de una clase específica por su id o tema."""

    @abstractmethod
    def agregar_material_transversal(self, materia: str, item: dict[str, Any]) -> None:
        """Registra un material sin clase afín en la sección transversal del cronograma."""

    @abstractmethod
    def quitar_material_transversal(self, materia: str, nombre_archivo: str) -> bool:
        """Quita un material de la sección transversal; retorna False si no estaba."""

    @abstractmethod
    def limpiar_material_transversal(self, materia: str) -> None:
        """Elimina todos los materiales de la sección transversal del cronograma."""

    @abstractmethod
    def obtener_parciales(self, materia: str) -> list[dict[str, Any]]:
        """Cortes de parcial de la materia: [{nombre, hasta}] con `hasta` = id de la clase."""

    @abstractmethod
    def guardar_parciales(self, materia: str, parciales: list[dict[str, Any]]) -> None:
        """Reemplaza los cortes de parcial de la materia."""


class MateriaRepo(ABC):
    """Puerto de repositorio para el catálogo de asignaturas del estudiante."""

    @abstractmethod
    def listar(self) -> list[Materia]:
        """Retorna las asignaturas registradas, en el orden en que se añadieron."""

    @abstractmethod
    def guardar(self, materia: Materia) -> None:
        """Añade la asignatura o, si su slug ya existe, actualiza su nombre."""

    @abstractmethod
    def eliminar(self, slug: str) -> bool:
        """Quita la asignatura del catálogo; retorna False si no existía."""

    @abstractmethod
    def cargar_materias(self) -> list[str]:
        """Compatibilidad: retorna los nombres de las asignaturas registradas."""

    @abstractmethod
    def agregar_materia(self, nueva_materia: str) -> None:
        """Compatibilidad: añade una asignatura al catálogo a partir de su nombre."""


class RegistroMaterialesRepo(ABC):
    """Puerto de repositorio para la auditoría y control de materiales ingestados."""

    @abstractmethod
    def verificar_material_ingestado(self, nombre_archivo: str) -> bool:
        """Indica si un archivo ya ha sido procesado previamente."""

    @abstractmethod
    def registrar_material(
        self, nombre_archivo: str, materia: str, nota: str | None = None
    ) -> None:
        """Registra un archivo procesado con su fecha, asignatura (slug) y nota generada."""

    @abstractmethod
    def listar_materiales(self) -> list[dict[str, Any]]:
        """Archivos registrados: [{nombre, materia, fecha, nota}]."""

    @abstractmethod
    def eliminar_material(self, nombre_archivo: str) -> dict[str, Any] | None:
        """Quita el archivo del registro y retorna su entrada, o None si no estaba."""

    @abstractmethod
    def eliminar_de_materia(self, materia: str) -> int:
        """Quita del registro todos los archivos de la materia; retorna cuántos."""

    @abstractmethod
    def vaciar(self) -> int:
        """Elimina todos los materiales registrados y retorna cuántos se borraron."""


__all__ = [
    "CronogramaRepo",
    "MateriaRepo",
    "RegistroMaterialesRepo",
]
