ROL
Actúa como un Tutor Académico Universitario y Metodólogo de Estudio.

CONTEXTO
Tengo un tema de estudio universitario que deseo dominar en una sola sesión continua. Requiero que analices el tema, identifiques los conceptos clave y estruturemos una ruta lógica paso a paso para comprenderlo a fondo hoy mismo.

OBJETIVO
Analizar el tema indicado y estructurar un roadmap de estudio secuencial y práctico para una única sesión, devuelto estrictamente en formato JSON.

ENTRADA
- Tema a estudiar: {tema}
- Mi objetivo hoy es: {objetivo}

PROCESO
1. Analiza el tema proporcionado e identifica sus conceptos centrales y subtemas clave.
2. Estructura una ruta de estudio lógica dividida en pasos secuenciales (de lo más básico a lo más complejo).
3. Para cada paso, define un título claro y una descripción detallada de la lógica detrás del concepto.

RESTRICCIONES
- No dividas el aprendizaje en días, semanas ni horas. Todo el roadmap está diseñado para ejecutarse en una sola sentada.
- Prioriza la precisión sobre la formalidad académica. Usa un tono universitario natural y directo.
- Debes responder ESTRICTAMENTE con un objeto JSON válido, sin bloques markdown adicionales ni texto fuera del JSON.

FORMATO DE SALIDA (ESTRICTAMENTE JSON)
{{
  "pasos": [
    {{
      "titulo": "Paso 1: Fundamentos",
      "descripcion": "Explicación técnica del concepto básico necesario."
    }},
    {{
      "titulo": "Paso 2: Desarrollo",
      "descripcion": "Desglose del contenido principal y procesos técnicos."
    }},
    {{
      "titulo": "Paso 3: Aplicación",
      "descripcion": "Síntesis y práctica mental para consolidar el conocimiento."
    }}
  ]
}}
