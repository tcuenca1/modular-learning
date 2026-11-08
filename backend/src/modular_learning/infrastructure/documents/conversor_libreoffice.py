"""Adaptador de ConversorPdfPort utilizando LibreOffice (soffice)."""

from __future__ import annotations

import logging
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

from modular_learning.core.ports.conversor_pdf import ConversorPdfPort

logger = logging.getLogger(__name__)


def buscar_ejecutable_soffice() -> str | None:
    """Busca el ejecutable soffice en ML_SOFFICE, PATH o rutas estándar."""
    env_soffice = os.getenv("ML_SOFFICE")
    if env_soffice and os.path.isfile(env_soffice):
        return env_soffice

    en_path = shutil.which("soffice")
    if en_path:
        return en_path

    rutas_comunes = [
        r"C:\Program Files\LibreOffice\program\soffice.exe",
        r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
        "/usr/bin/soffice",
        "/usr/local/bin/soffice",
    ]
    for r in rutas_comunes:
        if os.path.isfile(r):
            return r

    return None


class ConversorLibreOffice(ConversorPdfPort):
    """Convierte presentaciones y documentos a PDF temporal mediante LibreOffice."""

    def __init__(self, ruta_soffice: str | None = None, timeout: int = 60) -> None:
        self.ruta_soffice = ruta_soffice or buscar_ejecutable_soffice()
        self.timeout = timeout

    def convertir_a_pdf(self, ruta_archivo: str) -> str | None:
        if not self.ruta_soffice or not os.path.isfile(ruta_archivo):
            return None

        tmp_dir = tempfile.mkdtemp(prefix="ml_soffice_")
        perfil_dir = os.path.join(tmp_dir, "perfil")
        perfil_url = Path(perfil_dir).as_uri()
        try:
            cmd = [
                self.ruta_soffice,
                f"-env:UserInstallation={perfil_url}",
                "--headless",
                "--convert-to",
                "pdf",
                "--outdir",
                tmp_dir,
                ruta_archivo,
            ]
            resultado = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                check=False,
            )
            if os.path.isdir(perfil_dir):
                shutil.rmtree(perfil_dir, ignore_errors=True)
            if resultado.returncode != 0:
                logger.warning(
                    "Fallo al convertir con soffice (%s): %s",
                    resultado.returncode,
                    resultado.stderr,
                )
                shutil.rmtree(tmp_dir, ignore_errors=True)
                return None

            nombre_esperado = Path(ruta_archivo).stem + ".pdf"
            ruta_pdf = os.path.join(tmp_dir, nombre_esperado)
            if os.path.isfile(ruta_pdf):
                return ruta_pdf

            # Buscar cualquier archivo .pdf en el directorio temporal
            for f in os.listdir(tmp_dir):
                if f.lower().endswith(".pdf"):
                    return os.path.join(tmp_dir, f)

            shutil.rmtree(tmp_dir, ignore_errors=True)
            return None
        except Exception as e:
            logger.warning("Error durante la conversión con LibreOffice: %s", e)
            shutil.rmtree(tmp_dir, ignore_errors=True)
            return None

    def borrar_temporal(self, ruta_pdf: str) -> None:
        if not ruta_pdf:
            return
        if os.path.isfile(ruta_pdf):
            try:
                os.remove(ruta_pdf)
            except Exception as e:
                logger.warning("No se pudo eliminar archivo PDF temporal %s: %s", ruta_pdf, e)
        dir_tmp = os.path.dirname(ruta_pdf)
        if os.path.basename(dir_tmp).startswith("ml_soffice_") and os.path.isdir(dir_tmp):
            shutil.rmtree(dir_tmp, ignore_errors=True)


__all__ = ["ConversorLibreOffice", "buscar_ejecutable_soffice"]
