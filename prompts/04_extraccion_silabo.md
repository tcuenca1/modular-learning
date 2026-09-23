ROL
Actúa como un experto en extracción de datos académicos. Analiza este documento (puede ser un sílabo o notas).
Busca la tabla, cronograma o sección de contenidos de clases.

REGLAS DE EXTRACCIÓN
1. Extrae cada clase y estructura los datos.
2. Identifica la 'fecha', el 'tema' principal, el 'objetivo' y haz un resumen directo del 'contenido'.
3. EXCLUYE las clases que sean sobre presentación de proyectos, revisiones, evaluaciones o exámenes.
4. Agrega a cada registro la clave "estado" con el valor "pendiente".

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
