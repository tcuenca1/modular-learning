"""Script idempotente para migrar datos sobre AlmacenDocumentos (archivos locales o Neon Postgres).

1. Normalizar materias.txt a materias.json (slug + nombre).
2. Asignar id único (uuid hex corto) a todas las clases en cronogramas que no lo tengan.
3. Renombrar los cronogramas al formato con slug: schedules/<slug>_cronograma.json.
4. Vincular clase_id en guias/guias.json con sus IDs correspondientes en los cronogramas.
"""

from __future__ import annotations

import argparse
import json
from typing import Any

from modular_learning.core.domain.cronograma import asignar_ids
from modular_learning.core.domain.materias import Materia, slug_materia
from modular_learning.infrastructure.persistence.almacen import (
    AlmacenDocumentos,
    almacen_por_defecto,
)


def migrar(
    almacen: AlmacenDocumentos | None = None,
    simular: bool = False,
) -> dict[str, int]:
    almacen_doc = almacen if almacen is not None else almacen_por_defecto()

    resumen = {
        "materias": 0,
        "cronogramas_procesados": 0,
        "cronogramas_renombrados": 0,
        "ids_asignados": 0,
        "guias_vinculadas": 0,
    }

    # ------------------------------------------------------------------ 1. Materias
    texto_json = almacen_doc.leer("config/materias.json")
    materias: list[Materia] = []
    if texto_json:
        try:
            raw = json.loads(texto_json)
            for item in raw:
                if isinstance(item, dict):
                    m = Materia.desde_dict(item)
                    if m:
                        materias.append(m)
                elif isinstance(item, str):
                    materias.append(Materia.desde_nombre(item))
        except Exception:
            pass
    else:
        texto_txt = almacen_doc.leer("config/materias.txt")
        if texto_txt:
            lineas = [l.strip() for l in texto_txt.splitlines() if l.strip()]
            materias = [Materia.desde_nombre(l) for l in lineas]

    if materias:
        resumen["materias"] = len(materias)
        if not simular:
            almacen_doc.escribir(
                "config/materias.json",
                json.dumps(
                    [m.a_dict() for m in materias], indent=2, ensure_ascii=False
                ),
            )
        prefix = "[SIMULADO] " if simular else "[OK] "
        print(f"{prefix}config/materias.json: {len(materias)} materias.")

    # -------------------------------------------------------------- 2. Cronogramas
    claves_schedules = [
        c
        for c in almacen_doc.listar("schedules/")
        if c.endswith(".json") and "/" not in c[len("schedules/") :]
    ]
    cronogramas_por_slug: dict[str, list[dict[str, Any]]] = {}

    for clave in claves_schedules:
        resumen["cronogramas_procesados"] += 1
        texto_sched = almacen_doc.leer(clave)
        if not texto_sched:
            continue
        try:
            data = json.loads(texto_sched)
        except Exception:
            continue

        if isinstance(data, dict):
            clases = data.get("clases", data.get("cronograma", []))
        elif isinstance(data, list):
            clases = data
            data = {"clases": clases}
        else:
            continue

        sin_id = sum(1 for c in clases if not str(c.get("id") or "").strip())
        ids_creados = asignar_ids(clases)
        resumen["ids_asignados"] += sin_id

        nombre_archivo = clave[len("schedules/") :]
        base = (
            nombre_archivo.removesuffix("_cronograma.json")
            .removesuffix("_cronograma")
            .removesuffix(".json")
        )
        slug = slug_materia(base)
        cronogramas_por_slug[slug] = clases

        nueva_clave = f"schedules/{slug}_cronograma.json"
        renombrado = nueva_clave != clave

        if renombrado:
            resumen["cronogramas_renombrados"] += 1
            if simular:
                print(
                    f"[SIMULADO] Renombrar {clave} -> {nueva_clave} ({len(clases)} clases, nuevos IDs: {ids_creados})"
                )
            else:
                data["clases"] = clases
                almacen_doc.escribir(
                    nueva_clave, json.dumps(data, indent=2, ensure_ascii=False)
                )
                almacen_doc.eliminar(clave)
                print(
                    f"[OK] Renombrado {clave} -> {nueva_clave} ({len(clases)} clases, nuevos IDs: {ids_creados})"
                )
        else:
            if ids_creados > 0:
                if simular:
                    print(
                        f"[SIMULADO] {clave}: {len(clases)} clases ({ids_creados} nuevos IDs)"
                    )
                else:
                    data["clases"] = clases
                    almacen_doc.escribir(
                        clave, json.dumps(data, indent=2, ensure_ascii=False)
                    )
                    print(
                        f"[OK] {clave}: {len(clases)} clases ({ids_creados} nuevos IDs)"
                    )
            else:
                print(f"[OK] {clave}: {len(clases)} clases (al día)")

    # ----------------------------------------------------------- 3. Guías offline
    texto_guias = almacen_doc.leer("guias/guias.json")
    if texto_guias:
        try:
            guias = json.loads(texto_guias)
        except Exception:
            guias = {}

        migradas = 0
        if isinstance(guias, dict):
            for g in guias.values():
                if not isinstance(g, dict):
                    continue
                materia_nombre = g.get("materia", "")
                m_slug = slug_materia(materia_nombre)
                sched_clases = cronogramas_por_slug.get(m_slug, [])

                for c in g.get("clases", []):
                    if not isinstance(c, dict) or c.get("clase_id"):
                        continue
                    # 1. Coincidencia por tema y fecha
                    for sc in sched_clases:
                        if sc.get("tema") == c.get("tema") and sc.get("fecha") == c.get(
                            "fecha"
                        ):
                            c["clase_id"] = sc.get("id")
                            migradas += 1
                            break
                    # 2. Coincidencia por tema si es único en el cronograma
                    if not c.get("clase_id"):
                        matches = [
                            sc for sc in sched_clases if sc.get("tema") == c.get("tema")
                        ]
                        if len(matches) == 1:
                            c["clase_id"] = matches[0].get("id")
                            migradas += 1

        resumen["guias_vinculadas"] = migradas
        if migradas > 0:
            if simular:
                print(f"[SIMULADO] guias/guias.json: {migradas} clases por vincular.")
            else:
                almacen_doc.escribir(
                    "guias/guias.json", json.dumps(guias, indent=2, ensure_ascii=False)
                )
                print(
                    f"[OK] guias/guias.json actualizado ({migradas} clases vinculadas)."
                )
        else:
            print("[OK] guias/guias.json al día.")

    return resumen


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Migración idempotente de datos sobre AlmacenDocumentos."
    )
    parser.add_argument(
        "--simular",
        action="store_true",
        help="Simula los cambios sin escribir en el almacén de datos.",
    )
    args = parser.parse_args()
    migrar(simular=args.simular)


if __name__ == "__main__":
    main()
