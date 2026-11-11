"""Servicio de aplicación para la gestión de asignaturas académicas y sus clases."""

from __future__ import annotations

from typing import Any

from modular_learning.core.domain.cronograma import buscar_clase, nuevo_id_clase
from modular_learning.core.domain.materias import (
    Materia,
    MateriaDuplicada,
    MateriaNoEncontrada,
    resolver_materia,
    slug_materia,
    validar_nombre_materia,
)
from modular_learning.core.ports.proyectos import ProyectosRepo
from modular_learning.core.ports.repositorios import (
    CronogramaRepo,
    MateriaRepo,
    RegistroMaterialesRepo,
)


class MateriasService:
    """Caso de uso y operaciones para catálogo de asignaturas, cronogramas y reversibilidad."""

    def __init__(
        self,
        materia_repo: MateriaRepo,
        cronograma_repo: CronogramaRepo | None = None,
        registro_repo: RegistroMaterialesRepo | None = None,
        proyectos_repo: ProyectosRepo | None = None,
        proyectos_service: Any = None,
    ):
        self.materia_repo = materia_repo
        self.cronograma_repo = cronograma_repo
        self.registro_repo = registro_repo
        self.proyectos_repo = proyectos_repo
        self.proyectos_service = proyectos_service

    # ------------------------------------------------------------------ Catálogo de materias
    def listar_materias(self) -> list[str]:
        """Retorna los nombres de las asignaturas registradas (compatibilidad)."""
        return self.materia_repo.cargar_materias()

    def listar_catalogo(self) -> list[dict[str, str]]:
        """Retorna las materias como [{slug, nombre}] ordenadas por nombre."""
        return [m.a_dict() for m in self.materia_repo.listar()]

    def obtener_materia(self, slug_o_nombre: str) -> Materia | None:
        """Busca una asignatura por su slug o por su nombre."""
        return resolver_materia(self.materia_repo.listar(), slug_o_nombre)

    def agregar_materia(self, nueva_materia: str) -> list[str]:
        """
        Añade una asignatura al catálogo y retorna la lista de nombres actualizada. Es
        idempotente (una repetida se ignora) y no valida: la usan flujos que "aseguran" que
        la asignatura exista. Para altas del usuario usar `crear_materia`.
        """
        self.materia_repo.agregar_materia(nueva_materia)
        return self.materia_repo.cargar_materias()

    def crear_materia(self, nombre: str) -> Materia:
        """Crea una asignatura nueva: valida el nombre y rechaza duplicados."""
        materia = Materia.desde_nombre(validar_nombre_materia(nombre))
        if any(m.slug == materia.slug for m in self.materia_repo.listar()):
            raise MateriaDuplicada(f"Ya existe una asignatura llamada «{materia.nombre}».")
        self.materia_repo.guardar(materia)
        return materia

    def validar_materia_recibida(self, texto: str) -> None:
        """
        Comprueba una asignatura recibida del cliente que puede ser nueva: si ya está en el
        catálogo vale tal cual; si no, su nombre debe ser válido (ver `validar_nombre_materia`).
        """
        if self.obtener_materia(texto) is None:
            validar_nombre_materia(texto)

    def _exigir_materia(self, materia: str) -> Materia:
        encontrada = self.obtener_materia(materia)
        if encontrada is None:
            raise MateriaNoEncontrada("Asignatura no encontrada.")
        return encontrada

    def renombrar_materia(self, slug: str, nuevo_nombre: str) -> Materia:
        """Cambia el nombre para mostrar de una asignatura conservando su slug."""
        nuevo_nombre = validar_nombre_materia(nuevo_nombre)
        existente = self._exigir_materia(slug)
        nuevo_slug = slug_materia(nuevo_nombre)
        if nuevo_slug != existente.slug and any(
            m.slug == nuevo_slug for m in self.materia_repo.listar()
        ):
            raise MateriaDuplicada(f"Ya existe una asignatura llamada «{nuevo_nombre}».")
        materia = Materia(slug=existente.slug, nombre=nuevo_nombre)
        self.materia_repo.guardar(materia)
        return materia

    def eliminar_materia(self, slug_o_nombre: str, borrar_cronograma: bool = True) -> bool:
        """
        Elimina la materia del catálogo. Si borrar_cronograma es True, también elimina
        su cronograma y desvincula sus materiales registrados. Además elimina los proyectos
        asociados a esa asignatura.
        """
        slug = slug_materia(slug_o_nombre)
        eliminada = self.materia_repo.eliminar(slug)
        if borrar_cronograma and self.cronograma_repo:
            self.cronograma_repo.eliminar_cronograma(slug)
        if self.registro_repo:
            self.registro_repo.eliminar_de_materia(slug)
        if self.proyectos_service:
            for p in self.proyectos_service.listar_proyectos(slug):
                self.proyectos_service.eliminar_proyecto(p.id)
        elif self.proyectos_repo:
            for p in self.proyectos_repo.listar(slug):
                self.proyectos_repo.eliminar(p.id)
        return eliminada

    # ------------------------------------------------------------------ Cronogramas y clases
    def obtener_cronograma(self, materia: str) -> list[dict[str, Any]] | None:
        if not self.cronograma_repo:
            return None
        return self.cronograma_repo.obtener_cronograma(materia)

    def obtener_proximas_clases(self, materia: str) -> list[dict[str, Any]]:
        """Retorna las clases pendientes del cronograma de la asignatura."""
        if not self.cronograma_repo:
            return []
        return self.cronograma_repo.obtener_proximas_clases(materia)

    def listar_cronogramas(self) -> dict[str, list[dict[str, Any]]]:
        """Todas las clases de todos los cronogramas, para el calendario."""
        if not self.cronograma_repo:
            return {}
        return self.cronograma_repo.listar_cronogramas()

    def eliminar_cronograma(self, materia: str, borrar_materia: bool = True) -> bool:
        """Elimina el cronograma de una asignatura y opcionalmente la materia del catálogo."""
        if not self.cronograma_repo:
            return False
        ok = self.cronograma_repo.eliminar_cronograma(materia)
        if borrar_materia:
            self.eliminar_materia(materia, borrar_cronograma=False)
        return ok

    def agregar_clase(self, materia: str, datos_clase: dict[str, Any]) -> dict[str, Any]:
        """Añade manualmente una clase al cronograma de una asignatura del catálogo."""
        if not self.cronograma_repo:
            raise ValueError("No hay repositorio de cronogramas configurado.")
        self._exigir_materia(materia)
        nueva = dict(datos_clase)
        if not nueva.get("id"):
            nueva["id"] = nuevo_id_clase()
        if not nueva.get("estado"):
            nueva["estado"] = "pendiente"
        self.cronograma_repo.actualizar_cronograma(materia, lambda clases: clases.append(nueva))
        return nueva

    def editar_clase(self, materia: str, clase_id: str, campos: dict[str, Any]) -> dict[str, Any]:
        """Actualiza los campos de una clase específica dentro del cronograma."""
        if not self.cronograma_repo:
            raise ValueError("No hay repositorio de cronogramas configurado.")
        editada: dict[str, Any] = {}

        def aplicar(clases: list[dict[str, Any]]) -> None:
            if not clases:
                raise LookupError(f"No hay cronograma para la asignatura {materia}.")
            clase = buscar_clase(clases, clase_id=clase_id)
            if clase is None:
                raise LookupError(f"Clase {clase_id} no encontrada en el cronograma.")
            for k, v in campos.items():
                if k != "id":  # El id nunca cambia
                    clase[k] = v
            editada.update(clase)

        self.cronograma_repo.actualizar_cronograma(materia, aplicar)
        return editada

    def eliminar_clase(self, materia: str, clase_id: str) -> bool:
        """Quita una clase del cronograma."""
        if not self.cronograma_repo:
            return False
        if not self.cronograma_repo.obtener_cronograma(materia):
            return False
        quitada = False

        def quitar(clases: list[dict[str, Any]]) -> list[dict[str, Any]]:
            nonlocal quitada
            restantes = [c for c in clases if str(c.get("id")) != clase_id]
            quitada = len(restantes) != len(clases)
            return restantes if quitada else clases

        self.cronograma_repo.actualizar_cronograma(materia, quitar)
        return quitada

    def cambiar_estado_clase(self, materia: str, clase_id: str, nuevo_estado: str) -> bool:
        """Modifica el estado de una clase ('pendiente' o 'completado')."""
        if not self.cronograma_repo:
            return False
        return self.cronograma_repo.marcar_clase(materia, clase_id=clase_id, estado=nuevo_estado)

    # ------------------------------------------------------------------ Cortes de parcial
    def obtener_parciales(self, materia: str) -> list[dict[str, Any]]:
        """Retorna los cortes de parcial definidos para la asignatura."""
        if not self.cronograma_repo:
            return []
        return self.cronograma_repo.obtener_parciales(materia)

    def guardar_parciales(
        self, materia: str, parciales: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """Guarda los cortes de parcial (ej. [{'nombre': 'Parcial 1', 'hasta': 'clase_id'}])"""
        if not self.cronograma_repo:
            raise ValueError("No hay repositorio de cronogramas.")
        self._exigir_materia(materia)
        self.cronograma_repo.guardar_parciales(materia, parciales)
        return parciales


__all__ = ["MateriasService"]
