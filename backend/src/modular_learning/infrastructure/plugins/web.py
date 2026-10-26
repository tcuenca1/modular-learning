from modular_learning.core.ports.plugin_practico import PluginPracticoBase
from modular_learning.infrastructure.persistence.almacen import DocumentoJson


class WebPlugin(PluginPracticoBase):
    """Adaptador práctico para Desarrollo y Programación Web."""

    def __init__(self):
        self._memoria = DocumentoJson("plugins/web_memoria.json")

    def guardar_contexto_extraido(self, metadatos: str) -> None:
        metadatos = metadatos.strip()
        if not metadatos:
            return

        historial = self._memoria.leer([])
        if not isinstance(historial, list):
            historial = []

        historial.append(metadatos)
        historial = historial[-3:]

        try:
            self._memoria.escribir(historial, sangria=4)
        except Exception as e:
            print(f"⚠️ No se pudo guardar la memoria del plugin Web: {e}")

    def cargar_contexto_reciente(self) -> str:
        try:
            historial = self._memoria.leer([])
        except Exception:
            return ""
        if isinstance(historial, list) and historial:
            return historial[-1]
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
