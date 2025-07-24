"""
Run it with:
    python list_tools.py
"""

import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def server() -> None:
    # Mirror the config you provided
    server_params = StdioServerParameters(
        command="npx",
        args=[
            "-y",
            "mcp-remote",
            "https://mcp.turkishtechlab.com/mcp",
        ],
    )

    # 1) Launch the npx process and open a bi‑directional stdio stream
    async with stdio_client(server_params) as (reader, writer):
        # 2) Create a high‑level session on top of that stream
        async with ClientSession(reader, writer) as session:
            await session.initialize()           # handshake
            tools_resp = await session.list_tools()  # 🚀 fetch the catalogue

            print("\nAvailable tools on the server:\n")
            for tool in tools_resp.tools:
                desc = f" — {tool.description}" if tool.description else ""
                print(f"• {tool.name}{desc}")

            return tools_resp.tools



if __name__ == "__main__":
    asyncio.run(server())