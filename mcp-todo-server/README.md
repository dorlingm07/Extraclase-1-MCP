# mcp-todo-server

Servidor MCP básico para gestión de tareas pendientes, implementado con el
SDK oficial de Python ([`mcp`](https://github.com/modelcontextprotocol/python-sdk),
versión `2.0.0`) usando la API de alto nivel `MCPServer`.

Este proyecto corresponde al Ejercicio 2 del trabajo extraclase de Model
Context Protocol (Programación IV, UNA).

## Capacidades expuestas

| Tipo | Nombre | Descripción |
|---|---|---|
| Resource | `tasks://pending` | Retorna en JSON las tareas pendientes (no completadas) almacenadas en `tasks.json` |
| Tool | `add_task(name, description, priority)` | Agrega una nueva tarea. `priority` debe ser `alta`, `media` o `baja` |
| Tool | `complete_task(task_id)` | Marca como completada la tarea con el ID indicado |
| Prompt | `daily_summary` | Genera un resumen del estado actual de las tareas (total, pendientes por prioridad, completadas) |

## Requisitos

- Python 3.10 o superior
- pip

## Instalación

```bash
# Crear y activar un entorno virtual (opcional pero recomendado)
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate # macOS / Linux

# Instalar dependencias
pip install -r requirements.txt
```

## Ejecución y pruebas

### Opción 1: Script cliente incluido (recomendado)

`test_client.py` se conecta al servidor por stdio usando el protocolo MCP
real (JSON-RPC) y ejercita, en orden, las 4 capacidades: lee el resource,
llama ambas tools y obtiene el prompt. Es la forma más confiable de generar
evidencia reproducible por terminal:

```bash
python test_client.py
```

Salida esperada (resumida):

```
Conectado a 'todo-server' (protocolo 2025-11-25)

=== Interacción 1: Resource tasks://pending ===
[... tarea #1 "Preparar entorno de desarrollo" ...]

=== Interacción 2: Tool add_task ===
Tarea #3 'Probar servidor MCP' agregada con prioridad media.

=== Interacción 3: Tool complete_task ===
Tarea #1 'Preparar entorno de desarrollo' marcada como completada.

=== Interacción 4: Prompt daily_summary ===
[... resumen con conteo de pendientes/completadas ...]
```

> Cada corrida modifica `tasks.json` (agrega la tarea de prueba y completa
> la #1). Si se quiere repetir la demostración desde cero, restaurar
> `tasks.json` a su contenido original antes de re-ejecutar.

### Opción 2: MCP Inspector (interfaz web)

```bash
mcp dev server.py --with "mcp[cli]==2.0.0"
```

> El flag `--with "mcp[cli]==2.0.0"` es necesario: por defecto `mcp dev`
> arma el comando `uv run --with mcp==2.0.0 mcp run server.py`, pero
> `mcp run` requiere las dependencias del extra `[cli]` (p. ej. `typer`),
> que no vienen incluidas en ese `--with` por defecto. Sin este flag
> adicional la conexión falla con `Error: typer is required`.

Esto abre `http://127.0.0.1:6274` en el navegador. Activar el switch de
conexión del servidor listado (`uv`) y esperar a que el estado cambie a
"Connected".

### Opción 3: Ejecución directa (stdio), para integrarlo con un cliente como Claude Desktop

```bash
python server.py
```

## Pruebas realizadas (4 interacciones, vía `test_client.py`)

1. **Consultar tareas pendientes** — se leyó el resource `tasks://pending`
   y se confirmó que retorna solo la tarea #1 "Preparar entorno de
   desarrollo" (prioridad alta), la única pendiente en el estado inicial.
2. **Agregar una tarea** — se invocó
   `add_task(name="Probar servidor MCP", description="Verificar que las tools respondan correctamente", priority="media")`
   y se confirmó la creación de la tarea #3, persistida en `tasks.json`.
3. **Completar una tarea** — se invocó `complete_task(task_id=1)` y se
   verificó el mensaje de confirmación y el cambio a `"completed": true`
   en `tasks.json`.
4. **Generar resumen diario** — se invocó el prompt `daily_summary` y se
   verificó que el texto refleja correctamente el total de tareas (3),
   pendientes por prioridad y completadas, tras las operaciones anteriores.

*(Agregar aquí las capturas de pantalla de la terminal ejecutando
`python test_client.py`, o del MCP Inspector si se usó la Opción 2.)*

## Estructura del proyecto

```
mcp-todo-server/
├── server.py         # Servidor MCP principal
├── test_client.py     # Cliente de prueba (evidencia de las 4 interacciones)
├── tasks.json         # Almacenamiento de tareas
├── requirements.txt   # Dependencias
└── README.md          # Este archivo
```

## Nota sobre la versión del SDK

Este proyecto se desarrolló con `mcp==2.0.0`. Esta versión renombró la API
de alto nivel: `FastMCP` (usado en documentación/tutoriales más antiguos)
ahora es `MCPServer`, importado desde `mcp.server.mcpserver` en lugar de
`mcp.server.fastmcp`. Los decoradores (`@mcp.resource`, `@mcp.tool`,
`@mcp.prompt`) y el método `mcp.run()` mantienen la misma interfaz.
