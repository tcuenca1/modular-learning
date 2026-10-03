import os
import json
from modules.plugins.ports.base_plugin import PluginPracticoBase


class WebPlugin(PluginPracticoBase):
    """Adaptador práctico para Desarrollo y Programación Web."""

    def __init__(self):
        self.ruta_memoria = os.path.join("data", "plugins", "web_memoria.json")

    def guardar_contexto_extraido(self, metadatos: str) -> None:
        metadatos = metadatos.strip()
        if not metadatos:
            return

        historial = []
        os.makedirs(os.path.dirname(self.ruta_memoria), exist_ok=True)
        if os.path.exists(self.ruta_memoria):
            try:
                with open(self.ruta_memoria, "r", encoding="utf-8") as f:
                    contenido = json.load(f)
                    if isinstance(contenido, list):
                        historial = contenido
            except Exception:
                historial = []

        historial.append(metadatos)
        historial = historial[-3:]

        try:
            with open(self.ruta_memoria, "w", encoding="utf-8") as f:
                json.dump(historial, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ No se pudo guardar la memoria del plugin Web: {e}")

    def cargar_contexto_reciente(self) -> str:
        if not os.path.exists(self.ruta_memoria):
            return ""
        try:
            with open(self.ruta_memoria, "r", encoding="utf-8") as f:
                historial = json.load(f)
            if isinstance(historial, list) and historial:
                return historial[-1]
            return ""
        except Exception:
            return ""

    def obtener_instrucciones_ia(self) -> str:
        contexto_extra = self.cargar_contexto_reciente()
        instrucciones = (
            "[ADAPTADOR PRÁCTICO: DESARROLLO Y PROGRAMACIÓN WEB]\n"
            "Reglas estrictas de mentoría:\n"
            "1. Enfócate en buenas prácticas de arquitectura web (separación frontend/backend, controladores, rutas, modelos).\n"
            "2. Proporciona ejemplos limpios, modernos y estructurados (HTML5 semántico, CSS/Tailwind, JavaScript ES6+ / Frameworks).\n"
            "3. Si el estudiante trabaja sobre su propio código, respeta su arquitectura y convenciones actuales.\n"
        )
        if contexto_extra:
            instrucciones += (
                f"\n[CONTEXTO Y CÓDIGO ACTUAL DEL PROYECTO LOCAL EN VSCODE]:\n{contexto_extra}\n"
            )
        return instrucciones

    def generar_ejercicio_base(self, tema: str) -> str:
        return (
            f"### 💻 Ejercicio Práctico de Programación Web\n"
            f"- **Tema:** {tema}\n"
            f"- **Estructura recomendada:** Modular, con controladores limpios y manejo de solicitudes HTTP.\n"
        )
