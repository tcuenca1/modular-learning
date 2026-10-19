"""Puertos e interfaces (contratos abstractos) del core hexagonal."""

from modular_learning.core.ports.boveda import BovedaNotasPort
from modular_learning.core.ports.config import AjustesPort
from modular_learning.core.ports.documentos import LectorDocumentosPort
from modular_learning.core.ports.llm import LLMAdapterBase, LLMPort
from modular_learning.core.ports.plugin_practico import PluginPracticoBase
from modular_learning.core.ports.repositorios import (
    CronogramaRepo,
    MateriaRepo,
    RegistroMaterialesRepo,
)

__all__ = [
    "AjustesPort",
    "BovedaNotasPort",
    "CronogramaRepo",
    "LLMAdapterBase",
    "LLMPort",
    "LectorDocumentosPort",
    "MateriaRepo",
    "PluginPracticoBase",
    "RegistroMaterialesRepo",
]
