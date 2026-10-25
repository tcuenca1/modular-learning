"""Contenedor de Inversión de Control (IoC) y arranque del sistema monorepo."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from modular_learning import settings as global_settings
from modular_learning.core.application.configuracion import ConfiguracionService
from modular_learning.core.application.evaluacion import EvaluacionService
from modular_learning.core.application.ingesta import IngestaService
from modular_learning.core.application.materias import MateriasService
from modular_learning.core.application.plugins import PluginsService
from modular_learning.core.application.silabo import SilaboService
from modular_learning.core.application.telemetria import TelemetriaService
from modular_learning.core.application.tutoria import TutoriaService
from modular_learning.core.ports.boveda import BovedaNotasPort
from modular_learning.core.ports.config import AjustesPort
from modular_learning.core.ports.documentos import LectorDocumentosPort
from modular_learning.core.ports.llm import LLMPort
from modular_learning.core.ports.plugin_practico import PluginPracticoBase
from modular_learning.core.ports.repositorios import (
    CronogramaRepo,
    MateriaRepo,
    RegistroMaterialesRepo,
)
from modular_learning.infrastructure.documents.lector_documentos import LectorDocumentosLocal
from modular_learning.infrastructure.llm.gemini_adapter import LLM_GeminiAdapter
from modular_learning.infrastructure.obsidian.boveda_obsidian import BovedaObsidianAdapter
from modular_learning.infrastructure.persistence.json_ajustes import JsonAjustesRepo
from modular_learning.infrastructure.persistence.json_repositorios import (
    JsonCronogramaRepo,
    JsonMateriaRepo,
    JsonRegistroMaterialesRepo,
)
from modular_learning.infrastructure.plugins.cisco import CiscoPlugin
from modular_learning.infrastructure.plugins.nodered import NodeRedPlugin
from modular_learning.infrastructure.plugins.web import WebPlugin


@dataclass
class Container:
    """Contenedor de dependencias ensambladas para Modular Learning."""

    settings: Any

    # Adaptadores de infraestructura
    llm: LLMPort
    cronograma_repo: CronogramaRepo
    materia_repo: MateriaRepo
    registro_repo: RegistroMaterialesRepo
    boveda_port: BovedaNotasPort
    lector_docs: LectorDocumentosPort
    ajustes_repo: AjustesPort
    plugins_dict: dict[str, PluginPracticoBase]

    # Servicios de aplicación
    tutoria_service: TutoriaService
    evaluacion_service: EvaluacionService
    silabo_service: SilaboService
    ingesta_service: IngestaService
    plugins_service: PluginsService
    telemetria_service: TelemetriaService
    configuracion_service: ConfiguracionService
    materias_service: MateriasService


_global_container: Container | None = None


def build_container(settings: Any | None = None) -> Container:
    """Instancia adaptadores de infraestructura y los inyecta en los servicios del core."""
    resolved_settings = settings or global_settings

    # 1. Instanciación de adaptadores de infraestructura
    llm = LLM_GeminiAdapter()
    cronograma_repo = JsonCronogramaRepo()
    materia_repo = JsonMateriaRepo()
    registro_repo = JsonRegistroMaterialesRepo()
    ajustes_repo = JsonAjustesRepo()
    boveda_port = BovedaObsidianAdapter(ajustes=ajustes_repo)
    lector_docs = LectorDocumentosLocal()

    plugins_dict: dict[str, PluginPracticoBase] = {
        "cisco": CiscoPlugin(),
        "nodered": NodeRedPlugin(),
        "web": WebPlugin(),
    }

    # 2. Instanciación e inyección en servicios de aplicación
    plugins_service = PluginsService(
        plugins=plugins_dict,
        ajustes_port=ajustes_repo,
        carpeta_plugins=str(global_settings.ruta_plugins_memoria()),
        lector_docs=lector_docs,
    )

    tutoria_service = TutoriaService(
        llm=llm,
        cronograma_repo=cronograma_repo,
        boveda_port=boveda_port,
        lector_docs=lector_docs,
        ajustes_port=ajustes_repo,
        plugins_service=plugins_service,
    )

    evaluacion_service = EvaluacionService(
        llm=llm,
        cronograma_repo=cronograma_repo,
    )

    silabo_service = SilaboService(
        llm=llm,
        cronograma_repo=cronograma_repo,
        materia_repo=materia_repo,
        lector_docs=lector_docs,
    )

    ingesta_service = IngestaService(
        llm=llm,
        registro_repo=registro_repo,
        boveda_port=boveda_port,
        lector_docs=lector_docs,
        ajustes_port=ajustes_repo,
        plugins_service=plugins_service,
        cronograma_repo=cronograma_repo,
    )

    telemetria_service = TelemetriaService(
        cronograma_repo=cronograma_repo,
        plugins=plugins_dict,
    )

    configuracion_service = ConfiguracionService(
        ajustes_repo=ajustes_repo,
    )

    materias_service = MateriasService(
        materia_repo=materia_repo,
        cronograma_repo=cronograma_repo,
    )

    container = Container(
        settings=resolved_settings,
        llm=llm,
        cronograma_repo=cronograma_repo,
        materia_repo=materia_repo,
        registro_repo=registro_repo,
        boveda_port=boveda_port,
        lector_docs=lector_docs,
        ajustes_repo=ajustes_repo,
        plugins_dict=plugins_dict,
        tutoria_service=tutoria_service,
        evaluacion_service=evaluacion_service,
        silabo_service=silabo_service,
        ingesta_service=ingesta_service,
        plugins_service=plugins_service,
        telemetria_service=telemetria_service,
        configuracion_service=configuracion_service,
        materias_service=materias_service,
    )

    global _global_container
    _global_container = container
    return container


def get_container() -> Container:
    """Retorna o construye la instancia singleton del contenedor."""
    global _global_container
    if _global_container is None:
        _global_container = build_container()
    return _global_container


__all__ = ["Container", "build_container", "get_container"]
