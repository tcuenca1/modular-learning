"""Script idempotente para migrar datos existentes:
1. Normalizar materias.txt a materias.json (slug + nombre).
2. Asignar id único (uuid hex corto) a todas las clases en data/schedules/*.json.
3. Vincular clase_id en data/guias/guias.json con sus IDs en los cronogramas.
"""

from __future__ import annotations

import json
from pathlib import Path

from modular_learning.core.domain.cronograma import asignar_ids
from modular_learning.core.domain.materias import Materia, slug_materia


def migrar() -> None:
    data_dir = Path("data")
    if not data_dir.exists():
        print("Directorio data/ no encontrado.")
        return

    # 1. Materias
    config_dir = data_dir / "config"
    p_txt = config_dir / "materias.txt"
    p_json = config_dir / "materias.json"

    materias: list[Materia] = []
    if p_json.exists():
        raw = json.loads(p_json.read_text(encoding="utf-8"))
        for item in raw:
            if isinstance(item, dict):
                m = Materia.desde_dict(item)
                if m:
                    materias.append(m)
            elif isinstance(item, str):
                materias.append(Materia.desde_nombre(item))
    elif p_txt.exists():
        lineas = [l.strip() for l in p_txt.read_text(encoding="utf-8").splitlines() if l.strip()]
        materias = [Materia.desde_nombre(l) for l in lineas]

    if materias:
        p_json.write_text(
            json.dumps([m.a_dict() for m in materias], indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        print(f"[OK] materias.json actualizado ({len(materias)} materias).")

    # 2. Cronogramas
    sched_dir = data_dir / "schedules"
    cronogramas_por_slug: dict[str, list[dict]] = {}
    if sched_dir.exists():
        for p in sched_dir.glob("*.json"):
            data = json.loads(p.read_text(encoding="utf-8"))
            clases = data.get("clases", [])
            ids_creados = asignar_ids(clases)
            p.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
            base = p.stem.removesuffix("_cronograma").removesuffix(".json")
            slug = slug_materia(base)
            cronogramas_por_slug[slug] = clases
            print(f"[OK] {p.name}: {len(clases)} clases (nuevos IDs: {ids_creados})")

    # 3. data/examples/schedules
    ex_sched_dir = data_dir / "examples" / "schedules"
    if ex_sched_dir.exists():
        for p in ex_sched_dir.glob("*.json"):
            data = json.loads(p.read_text(encoding="utf-8"))
            clases = data.get("clases", [])
            ids_creados = asignar_ids(clases)
            p.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
            print(f"[OK] {p.name}: {len(clases)} clases (nuevos IDs: {ids_creados})")

    # 4. Guias offline
    guias_p = data_dir / "guias" / "guias.json"
    if guias_p.exists():
        guias = json.loads(guias_p.read_text(encoding="utf-8"))
        migradas = 0
        for g in guias.values():
            if not isinstance(g, dict):
                continue
            materia_nombre = g.get("materia", "")
            m_slug = slug_materia(materia_nombre)
            sched_clases = cronogramas_por_slug.get(m_slug, [])
            for c in g.get("clases", []):
                if not isinstance(c, dict):
                    continue
                if not c.get("clase_id"):
                    # Disambiguate by (tema, fecha)
                    for sc in sched_clases:
                        if sc.get("tema") == c.get("tema") and sc.get("fecha") == c.get("fecha"):
                            c["clase_id"] = sc.get("id")
                            migradas += 1
                            break
                    # Fallback by tema only if unique
                    if not c.get("clase_id"):
                        matches = [sc for sc in sched_clases if sc.get("tema") == c.get("tema")]
                        if len(matches) == 1:
                            c["clase_id"] = matches[0].get("id")
                            migradas += 1

        guias_p.write_text(json.dumps(guias, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"[OK] guias.json actualizado (clases vinculadas: {migradas}).")


if __name__ == "__main__":
    migrar()
