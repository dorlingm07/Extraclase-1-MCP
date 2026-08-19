import json
from pathlib import Path
from typing import Literal

from mcp.server.fastmcp import FastMCP

TASKS_FILE = Path(__file__).parent / "tasks.json"

mcp = FastMCP("todo-server")


def _load_tasks() -> dict:
    with open(TASKS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_tasks(data: dict) -> None:
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


@mcp.resource("tasks://pending")
def get_pending_tasks() -> str:
    """Lista de tareas pendientes almacenadas en tasks.json."""
    data = _load_tasks()
    pending = [t for t in data["tasks"] if not t["completed"]]
    return json.dumps(pending, ensure_ascii=False, indent=2)


@mcp.tool()
def add_task(name: str, description: str, priority: Literal["alta", "media", "baja"]) -> str:
    """Agrega una nueva tarea pendiente con nombre, descripción y prioridad."""
    data = _load_tasks()
    task_id = data["next_id"]
    data["tasks"].append(
        {
            "id": task_id,
            "name": name,
            "description": description,
            "priority": priority,
            "completed": False,
        }
    )
    data["next_id"] += 1
    _save_tasks(data)
    return f"Tarea #{task_id} '{name}' agregada con prioridad {priority}."


@mcp.tool()
def complete_task(task_id: int) -> str:
    """Marca como completada la tarea con el ID indicado."""
    data = _load_tasks()
    for task in data["tasks"]:
        if task["id"] == task_id:
            if task["completed"]:
                return f"La tarea #{task_id} ya estaba completada."
            task["completed"] = True
            _save_tasks(data)
            return f"Tarea #{task_id} '{task['name']}' marcada como completada."
    return f"No se encontró ninguna tarea con ID {task_id}."


@mcp.prompt()
def daily_summary() -> str:
    """Genera un resumen del estado actual de las tareas."""
    data = _load_tasks()
    tasks = data["tasks"]
    pending = [t for t in tasks if not t["completed"]]
    completed = [t for t in tasks if t["completed"]]

    by_priority = {"alta": 0, "media": 0, "baja": 0}
    for t in pending:
        by_priority[t["priority"]] += 1

    lines = [
        "Genera un resumen diario del estado de las tareas con estos datos:",
        f"- Total de tareas: {len(tasks)}",
        f"- Pendientes: {len(pending)} (alta: {by_priority['alta']}, "
        f"media: {by_priority['media']}, baja: {by_priority['baja']})",
        f"- Completadas: {len(completed)}",
        "",
        "Detalle de pendientes:",
    ]
    for t in pending:
        lines.append(f"  #{t['id']} [{t['priority']}] {t['name']}: {t['description']}")

    return "\n".join(lines)


if __name__ == "__main__":
    mcp.run()
