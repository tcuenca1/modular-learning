from google.genai import types

from modular_learning.infrastructure.llm.gemini_adapter import LLM_GeminiAdapter


def test_normalizar_historial_con_strings(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "dummy_key")
    adapter = LLM_GeminiAdapter()

    historial_entrada = [
        {"role": "user", "parts": ["Hola tutor"]},
        {"role": "model", "parts": ["Hola, ¿en qué te ayudo?"]},
    ]

    resultado = adapter._normalizar_historial(historial_entrada)

    assert len(resultado) == 2
    assert isinstance(resultado[0], types.Content)
    assert resultado[0].role == "user"
    assert resultado[0].parts[0].text == "Hola tutor"
    assert resultado[1].role == "model"
    assert resultado[1].parts[0].text == "Hola, ¿en qué te ayudo?"


def test_normalizar_historial_vacio(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "dummy_key")
    adapter = LLM_GeminiAdapter()

    assert adapter._normalizar_historial(None) == []
    assert adapter._normalizar_historial([]) == []


def test_normalizar_historial_con_content_existente(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "dummy_key")
    adapter = LLM_GeminiAdapter()

    content = types.Content(role="user", parts=[types.Part.from_text(text="Test")])
    resultado = adapter._normalizar_historial([content])

    assert len(resultado) == 1
    assert resultado[0] is content


def test_parsear_json_limpieza_claves_y_bloques_markdown():
    json_con_saltos_y_markdown = """```json
    {
        "\\n \\"pasos\\"": [
            {"titulo": "Paso 1"}
        ],
        "  subtemas  ": ["a", "b"]
    }
    ```"""
    resultado = LLM_GeminiAdapter._parsear_json(json_con_saltos_y_markdown)

    assert "pasos" in resultado
    assert "subtemas" in resultado
    assert resultado["pasos"][0]["titulo"] == "Paso 1"
    assert resultado["subtemas"] == ["a", "b"]
