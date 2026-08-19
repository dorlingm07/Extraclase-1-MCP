# mcp-todo-server

Servidor MCP básico para gestión de tareas pendientes, implementado con el
SDK oficial de Python ([`mcp`](https://github.com/modelcontextprotocol/python-sdk))
usando la API de alto nivel `FastMCP`.

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

## Ejecución

### Opción 1: MCP Inspector (recomendado para pruebas manuales)

El SDK incluye un inspector web que permite invocar resources, tools y
prompts sin necesidad de un cliente como Claude Desktop:

```bash
mcp dev server.py
```

Esto abre una interfaz en el navegador donde se puede:
1. Ver el resource `tasks://pending` y su contenido.
2. Ejecutar la tool `add_task` con parámetros de prueba.
3. Ejecutar la tool `complete_task` indicando un ID.
4. Ejecutar el prompt `daily_summary` y ver el texto generado.

### Opción 2: Ejecución directa (stdio)

```bash
python server.py
```

El servidor queda escuchando por stdio, listo para que un cliente MCP
(por ejemplo Claude Desktop) se conecte a él.

## Pruebas realizadas (mínimo 3 interacciones)

1. **Consultar tareas pendientes** — se invocó el resource `tasks://pending`
   y se verificó que retorna la tarea inicial "Preparar entorno de
   desarrollo" (prioridad alta) definida en `tasks.json`.
2. **Agregar una tarea** — se ejecutó
   `add_task(name="Probar servidor MCP", description="Verificar que las tools respondan correctamente", priority="media")`
   y se confirmó que la tarea se agregó con un nuevo ID y quedó reflejada
   en `tasks.json`.
3. **Completar una tarea** — se ejecutó `complete_task(task_id=1)` y se
   verificó que la tarea pasó a `"completed": true` y ya no aparece en el
   resource `tasks://pending`.
4. **Generar resumen diario** — se invocó el prompt `daily_summary` y se
   verificó que el texto generado refleja correctamente el conteo de
   tareas pendientes/completadas y su desglose por prioridad.

*(Reemplazar esta sección con las capturas de pantalla reales del
Inspector o de Claude Desktop mostrando cada interacción.)*

## Estructura del proyecto

```
mcp-todo-server/
├── server.py         # Servidor MCP principal
├── tasks.json         # Almacenamiento de tareas
├── requirements.txt   # Dependencias
└── README.md          # Este archivo
```
