# mcp_tool_fetcher.py

import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def open_client() -> ClientSession:
    server_params = StdioServerParameters(
        command="npx",
        args=["-y", "mcp-remote", "https://mcp.turkishtechlab.com/mcp"],
    )

    # Açılan stdio_client ve ClientSession context'lerini saklayacak şekilde manuel enter yapıyoruz
    err_log = open("mcp_errors.log", "w", encoding="utf-8")
    stdio_cm = stdio_client(server_params, errlog=err_log)
    reader, writer = await stdio_cm.__aenter__()

    client_cm = ClientSession(reader, writer)
    client_session = await client_cm.__aenter__()

    # initialize çağrısı başarılı olmalı
    await client_session.initialize()

    # close()'u sarmalayıp context yöneticilerini düzgün kapatıyoruz
    async def _close_wrapper():
        try:
            # Önce ClientSession'in kendi close'ını çağır (varsa)
            orig_close = getattr(client_session, "close", None)
            if orig_close and orig_close is not _close_wrapper:
                res = orig_close()
                if asyncio.iscoroutine(res):
                    await res
        except Exception:
            pass
        try:
            await client_cm.__aexit__(None, None, None)
        except Exception:
            pass
        try:
            await stdio_cm.__aexit__(None, None, None)
        except Exception:
            pass
        try:
            err_log.close()
        except Exception:
            pass

    # Monkey-patch: caller await session.close() dediğinde _close_wrapper çalışacak
    client_session.close = _close_wrapper

    return client_session


async def get_structured_tools(session: ClientSession) -> list:
    """
    MCP sunucusuna bağlanır, kimlik doğrular ve sunucudaki tüm araçları,
    LangGraph için uygun, zengin ve detaylı bir yapıya dönüştürüp döndürür.
    """

    with open("mcp_fetcher_errors.log", "w") as err_log:
                tools_resp = await session.list_tools()
                langgraph_ready_tools = []

                for tool in tools_resp.tools:
                    tool_definition = {
                        "name": tool.name,
                        "description": tool.description or "",
                        "input_schema": tool.inputSchema or {},
                    }
                    langgraph_ready_tools.append(tool_definition)         
                return langgraph_ready_tools