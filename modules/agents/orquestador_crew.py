from crewai import Agent, Task, Crew, Process
from modules.agents.herramientas_agentes import (
    ejecutar_pruebas,
    modificar_codigo,
    ejecutar_git,
    actualizar_documentacion,
)


qa_agent = Agent(
    role="QA",
    goal="Calidad y verificación de pruebas",
    backstory="Experto en testing de software y aseguramiento de calidad.",
    tools=[ejecutar_pruebas],
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
    goal="Mantener el registro del proyecto actualizado de forma clara y concisa.",
    backstory="Especialista en documentación técnica responsable de registrar los cambios del sistema en el CHANGELOG.",
    tools=[actualizar_documentacion],
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
task_fix = Task(
    description="Corregir código si se detectan errores.",
    agent=dev_agent,
    expected_output="Código corregido",
)
task_docs = Task(
    description="Actualizar la documentación del proyecto con un resumen de los cambios recientes.",
    agent=docs_agent,
    expected_output="Registro actualizado en changelog",
)
task_commit = Task(
    description="Consolidar los cambios en git usando Conventional Commits.",
    agent=devops_agent,
    expected_output="Commit realizado exitosamente",
)

crew = Crew(
    agents=[qa_agent, dev_agent, docs_agent, devops_agent],
    tasks=[task_test, task_fix, task_docs, task_commit],
    process=Process.sequential,
)

if __name__ == "__main__":
    crew.kickoff()
