# Datos de Ejemplo Anonimizados (data/examples/)

Esta carpeta contiene archivos de ejemplo con datos sintéticos y anonimizados que replican la estructura utilizada por el sistema en producción.

## Estructura
- `config/`:
  - `materias.txt`: Lista de asignaturas registradas.
  - `registro_materiales.json`: Registro histórico de material pedagógico ingestado.
- `plugins/`:
  - `cisco_memoria.json`: Memoria sintética para actividades Packet Tracer.
  - `nodered_memoria.json`: Memoria de flujos de IoT / Node-RED.
  - `web_memoria.json`: Memoria de proyectos web detectados.
- `schedules/`:
  - `EJEMPLO_ASIGNATURA_cronograma.json`: Modelo de cronograma curricular por clases.

## Uso local
Para inicializar un entorno local de desarrollo con estos datos de prueba:
```bash
cp -r data/examples/* data/
```
