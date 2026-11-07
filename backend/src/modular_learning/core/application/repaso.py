"""Servicio de aplicación de repaso espaciado e historial de estudio por clase."""

from __future__ import annotations

import random
from collections import defaultdict
from datetime import date, datetime
from typing import Any

from modular_learning.core.domain.repaso_espaciado import Tarjeta, id_tarjeta, programar
from modular_learning.core.ports.repaso import HistorialRepo, TarjetasRepo

LIMITE_REPASO_DIARIO = 10


def _hoy() -> date:
    """Fecha local del estudiante (el repaso se programa por días de su calendario)."""
    return datetime.now().date()


def _misma_clase(tarjeta: Tarjeta, materia: str, tema: str) -> bool:
    """Coincidencia tolerante de materia y tema (mayúsculas y temas parciales)."""
    if tarjeta.materia.strip().lower() != materia.strip().lower():
        return False
    a, b = tarjeta.tema.strip().lower(), tema.strip().lower()
    return bool(a and b) and (a in b or b in a)


class RepasoService:
    """Caso de uso: programa las preguntas falladas/acertadas y registra la actividad de estudio."""

    def __init__(
        self,
        tarjetas_repo: TarjetasRepo,
        historial_repo: HistorialRepo,
        rng: random.Random | None = None,
    ):
        self.tarjetas_repo = tarjetas_repo
        self.historial_repo = historial_repo
        self.rng = rng or random.Random()

    # ------------------------------------------------------------------ registro
    def registrar_resultados(
        self,
        preguntas: list[dict[str, Any]],
        detalle: list[dict[str, Any]],
        hoy: date | None = None,
    ) -> None:
        """Actualiza la programación SM-2 de cada pregunta y anota el repaso en el historial."""
        hoy = hoy or _hoy()
        por_clase: dict[tuple[str, str], dict[str, Any]] = defaultdict(
            lambda: {"aciertos": 0, "total": 0, "falladas": []}
        )

        for pregunta, resultado in zip(preguntas, detalle, strict=False):
            materia = str(pregunta.get("materia") or "").strip()
            tema = str(pregunta.get("tema") or "").strip()
            enunciado = str(pregunta.get("enunciado", ""))
            if not materia or not enunciado:
                continue  # Sin clase de origen no hay a qué ligar la tarjeta

            tarjeta_id = pregunta.get("tarjeta_id") or id_tarjeta(materia, enunciado)
            tarjeta = self.tarjetas_repo.obtener(tarjeta_id) or Tarjeta(
                id=tarjeta_id,
                materia=materia,
                tema=tema,
                enunciado=enunciado,
                opciones=list(pregunta.get("opciones", [])),
                respuesta_correcta=str(pregunta.get("respuesta_correcta", "")),
                explicacion=str(pregunta.get("explicacion", "")),
                creada=hoy.isoformat(),
            )
            correcto = bool(resultado.get("correcto"))
            programar(tarjeta, correcto, hoy, elegida=str(resultado.get("elegida", "")))
            self.tarjetas_repo.guardar(tarjeta)

            resumen = por_clase[(materia, tema)]
            resumen["total"] += 1
            resumen["aciertos"] += int(correcto)
            if not correcto:
                resumen["falladas"].append(enunciado)

        momento = datetime.now().isoformat(timespec="seconds")
        for (materia, tema), resumen in por_clase.items():
            self.historial_repo.registrar(
                {"fecha": momento, "tipo": "repaso", "materia": materia, "tema": tema, **resumen}
            )

    def registrar_tutoria(
        self, materia: str, tema: str, nivel: str, enfoque: str | None = None
    ) -> None:
        """Anota en el historial una sesión de tutoría terminada."""
        evento: dict[str, Any] = {
            "fecha": datetime.now().isoformat(timespec="seconds"),
            "tipo": "tutoria",
            "materia": materia,
            "tema": tema,
            "nivel": nivel,
        }
        if enfoque:
            evento["enfoque"] = enfoque
        self.historial_repo.registrar(evento)

    def registrar_estudio_offline(
        self, materia: str, tema: str, resultado: str, dudas: str = "", guia_id: str | None = None
    ) -> None:
        """Anota en el historial una clase estudiada con una guía offline y cómo le fue."""
        evento: dict[str, Any] = {
            "fecha": datetime.now().isoformat(timespec="seconds"),
            "tipo": "guia",
            "materia": materia,
            "tema": tema,
            "resultado": resultado,
        }
        if dudas:
            evento["dudas"] = dudas
        if guia_id:
            evento["guia_id"] = guia_id
        self.historial_repo.registrar(evento)

    # ------------------------------------------------------------------ consultas
    def pendientes(self, hoy: date | None = None) -> list[Tarjeta]:
        """Tarjetas cuya próxima revisión ya llegó, las más atrasadas primero."""
        hoy = hoy or _hoy()
        vencidas = [t for t in self.tarjetas_repo.listar() if t.vence(hoy)]
        return sorted(vencidas, key=lambda t: t.proxima or "")

    def preguntas_pendientes(
        self, hoy: date | None = None, limite: int = LIMITE_REPASO_DIARIO
    ) -> list[dict[str, Any]]:
        """Arma un repaso con las tarjetas vencidas, barajando de nuevo sus opciones."""
        from modular_learning.core.application.evaluacion import mezclar_opciones

        preguntas = []
        for t in self.pendientes(hoy)[:limite]:
            mezclada = mezclar_opciones(
                {
                    "enunciado": t.enunciado,
                    "opciones": t.opciones,
                    "respuesta_correcta": t.respuesta_correcta,
                },
                self.rng,
            )
            preguntas.append(
                {
                    **mezclada,
                    "tarjeta_id": t.id,
                    "materia": t.materia,
                    "tema": t.tema,
                    "explicacion": t.explicacion,
                }
            )
        return preguntas

    def resumen(self, hoy: date | None = None) -> dict[str, Any]:
        """Conteos para la pantalla de inicio y de repaso."""
        hoy = hoy or _hoy()
        tarjetas = self.tarjetas_repo.listar()
        return {
            "pendientes_hoy": sum(1 for t in tarjetas if t.vence(hoy)),
            "total": len(tarjetas),
            "dominadas": sum(1 for t in tarjetas if t.dominada),
        }

    def fallos_previos(self, materia: str, tema: str, limite: int = 5) -> list[str]:
        """Enunciados que el estudiante falló la última vez que los vio en esa clase."""
        return [
            t.enunciado
            for t in self.tarjetas_repo.listar()
            if t.ultimo_fallo and _misma_clase(t, materia, tema)
        ][:limite]

    def historial(
        self, materia: str | None = None, tema: str | None = None
    ) -> list[dict[str, Any]]:
        return self.historial_repo.listar(materia, tema)

    def eliminar_tarjeta(self, tarjeta_id: str) -> bool:
        """Elimina una tarjeta de repaso espaciado."""
        return self.tarjetas_repo.eliminar([tarjeta_id]) > 0


__all__ = ["LIMITE_REPASO_DIARIO", "RepasoService"]
