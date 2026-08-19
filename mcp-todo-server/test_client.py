"""Cliente de prueba: se conecta a server.py por stdio y ejercita las 4
capacidades del servidor (resource, 2 tools, prompt). Sirve como evidencia
reproducible de las interacciones pedidas en el Ejercicio 2.
"""

import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

sys.stdout.reconfigure(encoding="utf-8")

SERVER_DIR = Path(__file__).parent
SERVER_SCRIPT = SERVER_DIR / "server.py"


async def main() -> None:
    params = StdioServerParameters(
        command=sys.executable,
        args=[str(SERVER_SCRIPT)],
        cwd=str(SERVER_DIR),
    )

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            init_result = await session.initialize()
            print(f"Conectado a '{init_result.server_info.name}' "
                  f"(protocolo {init_result.protocol_version})\n")

            print("=== Interacción 1: Resource tasks://pending ===")
            resource = await session.read_resource("tasks://pending")
            print(resource.contents[0].text)

            print("\n=== Interacción 2: Tool add_task ===")
            result = await session.call_tool(
                "add_task",
                {
                    "name": "Probar servidor MCP",
                    "description": "Verificar que las tools respondan correctamente",
                    "priority": "media",
                },
            )
            print(result.content[0].text)

            print("\n=== Interacción 3: Tool complete_task ===")
            result = await session.call_tool("complete_task", {"task_id": 1})
            print(result.content[0].text)

            print("\n=== Interacción 4: Prompt daily_summary ===")
            prompt = await session.get_prompt("daily_summary")
            print(prompt.messages[0].content.text)


if __name__ == "__main__":
    asyncio.run(main())
