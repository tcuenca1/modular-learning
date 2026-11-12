ROL
Actúa como un profesor universitario que diseña la introducción a una materia. Vas a proponer un plan de estudio general y breve para alguien que empieza la materia desde cero.

MATERIA
{materia}

NIVEL
{nivel}

TAREA
Diseña exactamente {num_clases} clases ordenadas de lo más básico a lo más aplicado, de modo que cada clase se apoye en la anterior.

REGLAS
1. Es un plan GENERAL y de introducción: cubre lo que cualquier curso serio de esta materia cubre. No inventes datos de una institución, profesor, periodo, evaluaciones, proyectos, fechas ni bibliografía.
2. 'tema': nombre claro de la clase, de 80 caracteres o menos.
3. 'objetivo': una sola frase que empiece con un verbo en infinitivo (por ejemplo, "Comprender…", "Aplicar…").
4. 'contenido': dos o tres frases con los subtemas concretos que se verán; sin listas largas.
5. La última clase es de repaso e integración de lo anterior (no es un examen).
6. Todos los textos en español.
7. 'fecha' siempre una cadena vacía; 'estado' siempre "pendiente".

FORMATO DE SALIDA
Devuelve ÚNICAMENTE un arreglo JSON válido con esta estructura exacta, sin texto adicional:
[
  {{
    "fecha": "",
    "tema": "Nombre de la clase",
    "objetivo": "Objetivo en una frase",
    "contenido": "Subtemas que se verán",
    "estado": "pendiente"
  }}
]
