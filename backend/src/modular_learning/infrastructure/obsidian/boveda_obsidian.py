"""Adaptador concreto para la persistencia de notas y guías de estudio en Obsidian."""

from __future__ import annotations

import os
from datetime import datetime

from modular_learning.core.ports.boveda import BovedaNotasPort
from modular_learning.core.ports.config import AjustesPort


class BovedaObsidianAdapter(BovedaNotasPort):
    """Implementación del puerto BovedaNotasPort para Obsidian."""

    def __init__(self, ruta_boveda_defecto: str | None = None, ajustes: AjustesPort | None = None):
        self._ruta_boveda_defecto = ruta_boveda_defecto
        self._ajustes = ajustes

    def _resolver_ruta_boveda(self, ruta_boveda: str | None) -> str:
        if ruta_boveda:
            return ruta_boveda
        if self._ruta_boveda_defecto:
            return self._ruta_boveda_defecto
        if self._ajustes:
            return self._ajustes.ruta_boveda()
        raise ValueError("No hay una ruta de bóveda de Obsidian configurada.")

    def guardar_nota(
        self,
        materia: str,
        subcarpeta: str,
        nombre_base: str,
        contenido: str,
        ruta_boveda: str | None = None,
    ) -> str:
        """Escribe la nota Markdown tal cual en <bóveda>/<materia>/<subcarpeta>/."""
        carpeta = os.path.join(self._resolver_ruta_boveda(ruta_boveda), materia, subcarpeta)
        os.makedirs(carpeta, exist_ok=True)
        ruta = os.path.join(carpeta, f"{nombre_base}.md")
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(contenido)
        return os.path.abspath(ruta)

    def guardar_resumen(
        self, materia: str, tema: str, contenido: str, ruta_boveda: str | None = None
    ) -> bool:
        """Crea un archivo .md dentro de la bóveda de Obsidian y actualiza su índice."""
        try:
            vault = self._resolver_ruta_boveda(ruta_boveda)
            carpeta_materia = os.path.join(vault, materia)
            os.makedirs(carpeta_materia, exist_ok=True)

            tema_sanitizado = (
                "".join(c if c.isalnum() or c in (" ", "_", "-") else "" for c in tema)
                .strip()
                .replace(" ", "_")
            )
            if not tema_sanitizado:
                tema_sanitizado = "resumen_sesion"

            nombre_archivo = f"{tema_sanitizado}.md"
            ruta_archivo = os.path.join(carpeta_materia, nombre_archivo)

            fecha_actual = datetime.now().strftime("%Y-%m-%d")
            materia_sin_espacios = materia.lower().replace(" ", "_")

            frontmatter = f"""---
materia: {materia}
fecha: {fecha_actual}
estado: pendiente_repaso
tags: [{materia_sin_espacios}, repaso, tutor_ia]
---

# Sesión de Estudio: {tema}
> **Asignatura principal:** [[{materia}]]

---

"""
            contenido_final = (
                frontmatter
                + contenido
                + f"\n\n---\n*Nota generada por Sistema de Tutoría CLI.*\nConexión raíz: [[{materia}]]\n"
            )

            with open(ruta_archivo, "w", encoding="utf-8") as archivo:
                archivo.write(contenido_final)

            self.actualizar_indice_materia(materia, tema_sanitizado, vault)
            return True

        except Exception as e:
            print(f"❌ Error al guardar el resumen en Obsidian: {e}")
            return False

    def actualizar_indice_materia(
        self, materia: str, tema_sanitizado: str, ruta_boveda: str | None = None
    ) -> bool:
        """Actualiza o crea el archivo índice de la asignatura con un enlace a la nota."""
        try:
            vault = self._resolver_ruta_boveda(ruta_boveda)
            materia_sin_espacios = materia.lower().replace(" ", "_")
            ruta_indice = os.path.join(vault, f"{materia}.md")
            link_tag = f"[[{tema_sanitizado}]]"

            if not os.path.exists(ruta_indice):
                with open(ruta_indice, "w", encoding="utf-8") as idx_file:
                    idx_file.write(
                        f"---\nmateria: {materia}\ntipo: indice_asignatura\ntags: [{materia_sin_espacios}, indice]\n---\n# 📚 Asignatura: {materia}\n\n## 🕸️ Grafo de Constelación de Temas\n- {link_tag}\n"
                    )
            else:
                with open(ruta_indice, "r", encoding="utf-8") as idx_file:
                    idx_content = idx_file.read()
                if link_tag not in idx_content:
                    with open(ruta_indice, "w", encoding="utf-8") as idx_file:
                        idx_file.write(idx_content + f"\n- {link_tag}")
            return True
        except Exception as e:
            print(f"⚠️ Error al actualizar el índice de Obsidian para {materia}: {e}")
            return False

    def eliminar_nota(self, ruta: str, ruta_boveda: str | None = None) -> bool:
        """Borra la nota si es un .md dentro de la bóveda; nunca toca nada fuera de ella."""
        try:
            boveda = os.path.realpath(self._resolver_ruta_boveda(ruta_boveda))
        except ValueError:
            return False
        destino = os.path.realpath(ruta)
        dentro = os.path.commonpath([boveda, destino]) == boveda and destino != boveda
        if not dentro or not destino.lower().endswith(".md") or not os.path.isfile(destino):
            return False
        os.remove(destino)
        return True


__all__ = ["BovedaObsidianAdapter"]
