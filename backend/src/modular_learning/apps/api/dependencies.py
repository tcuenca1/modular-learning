"""Inyección de dependencias para los routers de FastAPI."""

from __future__ import annotations

from typing import Annotated

from fastapi import Depends, Request

from modular_learning.apps.api.session_store import SessionStore
from modular_learning.bootstrap import Container
from modular_learning.bootstrap import get_container as default_get_container
from modular_learning.core.application.configuracion import ConfiguracionService
from modular_learning.core.application.evaluacion import EvaluacionService
from modular_learning.core.application.guias import GuiaOfflineService
from modular_learning.core.application.ingesta import IngestaService
from modular_learning.core.application.materias import MateriasService
from modular_learning.core.application.plugins import PluginsService
from modular_learning.core.application.repaso import RepasoService
from modular_learning.core.application.silabo import SilaboService
from modular_learning.core.application.telemetria import TelemetriaService
from modular_learning.core.application.tutoria import TutoriaService


def get_container(request: Request) -> Container:
    """Obtiene el contenedor IoC desde request.app.state o el fallback global."""
    cont = getattr(request.app.state, "container", None)
    if cont is None:
        cont = default_get_container()
    return cont


def get_session_store(request: Request) -> SessionStore:
    """Obtiene el almacén de sesiones registrado en request.app.state."""
    return request.app.state.session_store


ContainerDep = Annotated[Container, Depends(get_container)]
SessionStoreDep = Annotated[SessionStore, Depends(get_session_store)]


def get_tutoria_service(cont: ContainerDep) -> TutoriaService:
    return cont.tutoria_service


def get_evaluacion_service(cont: ContainerDep) -> EvaluacionService:
    return cont.evaluacion_service


def get_silabo_service(cont: ContainerDep) -> SilaboService:
    return cont.silabo_service


def get_ingesta_service(cont: ContainerDep) -> IngestaService:
    return cont.ingesta_service


def get_plugins_service(cont: ContainerDep) -> PluginsService:
    return cont.plugins_service


def get_telemetria_service(cont: ContainerDep) -> TelemetriaService:
    return cont.telemetria_service


def get_configuracion_service(cont: ContainerDep) -> ConfiguracionService:
    return cont.configuracion_service


def get_materias_service(cont: ContainerDep) -> MateriasService:
    return cont.materias_service


def get_repaso_service(cont: ContainerDep) -> RepasoService:
    return cont.repaso_service


def get_guias_service(cont: ContainerDep) -> GuiaOfflineService:
    return cont.guias_service
