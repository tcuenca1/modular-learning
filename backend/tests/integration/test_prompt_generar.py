"""El prompt real de generación de cronogramas se puede rellenar sin errores de formato."""

from __future__ import annotations

from pathlib import Path

import modular_learning.core.prompts as paquete


def test_el_prompt_08_se_formatea_y_conserva_el_json_de_ejemplo():
    texto = (Path(paquete.__file__).parent / "08_generar_cronograma.md").read_text(encoding="utf-8")
    lleno = texto.format(materia="Redes de Datos", num_clases=10, nivel="Medio: ejemplo")
    assert "Redes de Datos" in lleno and "exactamente 10 clases" in lleno
    assert '"fecha": ""' in lleno and "{{" not in lleno  # las llaves del JSON quedan simples
