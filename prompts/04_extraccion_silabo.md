ROL
Actúa como un experto en extracción de datos académicos. Analiza este documento (puede ser un sílabo o notas).
Busca la tabla, cronograma o sección de contenidos de clases.

REGLAS DE EXTRACCIÓN Y FILTRADO
1. Extrae cada clase y estructura los datos.
2. Identifica la 'fecha', el 'tema' principal, el 'objetivo' y haz un resumen directo del 'contenido'.
3. REGLA DE EXCLUSIÓN ESTRICTA: No elimines una clase completa si contiene temas académicos válidos (ej. 'Middleware de Excepciones') junto con una evaluación. Elimina la clase SOLO si el TEMA CENTRAL es EXCLUSIVAMENTE presentación de proyectos, revisiones finales o examen parcial/final.
4. REGLA DE OMISIÓN: Sí una clase válida incluye una evaluación en sus contenidos, OMITE la mención a la evaluación en el campo 'contenido' del JSON y conserva únicamente los temas académicos.
5. Agrega a cada registro la clave "estado" con el valor "pendiente".

ENTRADA
Contenido de la Sección del Sílabo ({materia}):
----------------------------------------
{contenido_texto}
----------------------------------------

FORMATO DE SALIDA
Devuelve ÚNICAMENTE un arreglo JSON válido con esta estructura exacta:
[
  {
    "fecha": "DD/MM/YYYY",
    "tema": "Nombre",
    "objetivo": "Objetivo",
    "contenido": "Resumen",
    "estado": "pendiente"
  }
]
