from crewai import Agent, Crew, Process, Task

from modules.agents.herramientas_agentes import (
    actualizar_documentacion,
    ejecutar_git,
    ejecutar_pruebas,
    leer_archivo,
    modificar_codigo,
)

qa_agent = Agent(
    role="QA",
    goal="Calidad y verificación de pruebas",
    backstory="REGLA CRÍTICA DE ARQUITECTURA: Está estrictamente prohibido que el código fuente (.py) contenga textos largos que actúen como prompts. Todo prompt debe existir en un archivo .md en 'prompts/'. Si detectas un prompt hardcodeado, instruye al Dev para extraerlo. Experto en testing de software y aseguramiento de calidad.",
    tools=[ejecutar_pruebas],
    llm="gemini/gemini-3.5-flash-lite",
)

arquitecto_agent = Agent(
    role="Guardián de la Arquitectura Hexagonal",
    goal="Asegurar que la capa de dominio puro jamás dependa de infraestructura externa",
    backstory="Revisas estrictamente las importaciones. Si detectas que algún archivo dentro de `modules/core/domain/` importa algo de `modules/core/adapters/` o librerías externas de infraestructura, reportas un fallo arquitectónico crítico.",
    llm="gemini/gemini-3.5-flash-lite",
)

seguridad_agent = Agent(
    role="Auditor de Seguridad Estática",
    goal="Prevenir la filtración de credenciales y ejecución de código inseguro",
    backstory="Auditas el código en busca de variables como `API_KEY` con valores hardcodeados, uso inseguro de `subprocess` sin sanitizar, o credenciales expuestas. Si encuentras un riesgo, obligas al Agente Dev a corregirlo antes del commit.",
    llm="gemini/gemini-3.5-flash-lite",
)

dev_agent = Agent(
    role="Dev",
    goal="Corregir errores de código",
    backstory="Desarrollador backend encargado de corregir e implementar mejoras en el código.",
    tools=[modificar_codigo],
    llm="gemini/gemini-3.5-flash-lite",
)

docs_agent = Agent(
    role="Agente Técnico de Documentación",
    goal="Ser el responsable absoluto de la precisión, actualización y exhaustividad de toda la carpeta `docs/` y del archivo `README.md` en la raíz del proyecto.",
    backstory=(
        "Especialista en documentación técnica y Technical Writer experto. "
        "REGLA CRÍTICA DE PRESERVACIÓN: NUNCA sobrescribas un archivo de documentación completo. "
        "Tu obligación estricta es PRIMERO LEER el contenido completo del archivo (usando la herramienta correspondiente). "
        "Debes PRESERVAR intacto el 100% del contexto histórico del proyecto (ej. Arquitectura Hexagonal, puertos, adaptadores, propósito académico) "
        "y limitarte a INSERTAR o ACTUALIZAR únicamente las secciones relevantes con las nuevas características. "
        "Si borras el contexto general del proyecto, serás penalizado."
    ),
    tools=[leer_archivo, actualizar_documentacion, modificar_codigo],
    llm="gemini/gemini-3.5-flash-lite",
)

devops_agent = Agent(
    role="DevOps",
    goal="Consolidar cambios en git usando estrictamente Conventional Commits",
    backstory="Ingeniero DevOps estricto. DEBE usar Conventional Commits obligatoriamente para todos los mensajes de commit (ej. 'fix: corrige error de importación', 'feat: añade nuevo módulo', 'docs: actualiza changelog', 'chore: limpieza de archivos').",
    tools=[ejecutar_git],
    llm="gemini/gemini-3.5-flash-lite",
)

task_test = Task(
    description="Ejecutar pruebas unitarias y verificar calidad.",
    agent=qa_agent,
    expected_output="Informe de pruebas",
)

task_arquitectura = Task(
    description="Revisar estrictamente que la capa de dominio puro (modules/core/domain/) no dependa de adaptadores ni de infraestructura externa.",
    agent=arquitecto_agent,
    expected_output="Informe de auditoría arquitectónica",
    context=[task_test],
)

task_seguridad = Task(
    description="Auditar el código en busca de credenciales hardcodeadas, claves API expuestas o ejecución insegura.",
    agent=seguridad_agent,
    expected_output="Informe de seguridad estática",
    context=[task_test],
)

task_fix = Task(
    description="Corregir código si se detectan errores, fallos arquitectónicos o riesgos de seguridad.",
    agent=dev_agent,
    expected_output="Código corregido",
    context=[task_arquitectura, task_seguridad],
)

task_docs = Task(
    description=(
        "Paso 1: Lee el archivo actual utilizando la herramienta de lectura. "
        "Paso 2: Analiza dónde encajan los nuevos cambios (ej. Lazy Loading, nuevos comandos). "
        "Paso 3: Redacta la adición manteniendo todo el texto anterior intacto y preservando la Arquitectura Hexagonal y el propósito académico. "
        "Paso 4: Guarda el archivo con la documentación actualizada."
    ),
    agent=docs_agent,
    expected_output="Documentación actualizada preservando el contexto histórico y la arquitectura",
    context=[task_fix],
)

task_commit = Task(
    description="Consolidar los cambios en git usando Conventional Commits.",
    agent=devops_agent,
    expected_output="Commit realizado exitosamente",
    context=[task_docs],
)

crew = Crew(
    agents=[qa_agent, arquitecto_agent, seguridad_agent, dev_agent, docs_agent, devops_agent],
    tasks=[task_test, task_arquitectura, task_seguridad, task_fix, task_docs, task_commit],
    process=Process.sequential,
    verbose=True,
)

if __name__ == "__main__":
    print("Iniciando auditoría de agentes...")
    crew.kickoff()
    print("Auditoría finalizada.")
