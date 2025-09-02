import asyncio
import sys
import json
from mcp_tool_fetcher import open_client
from mcp_tool_executer import execute_tool_with_params

async def main():
    session = await open_client()
    try:
        tool_name = "get_flight_status_by_route"
        cases = {
            "empty_args": {},
            "invalid_from_len": {"fromAirport": "IS", "flightDate": "2025-08-31"},
            "valid": {"fromAirport": "IST", "toAirport": "ESB", "flightDate": "2025-08-31"},
        }

        for name, args in cases.items():
            print(f"CASE: {name}")
            result = await execute_tool_with_params(tool_name=tool_name, tool_args=args, session=session)

            if result.get("error") == "validation_error":
                print("  validation failed:", result["errors"])
            elif result.get("error"):
                print("  execution error:", result)
            else:
                tool_resp = result["result"]
                print("  tool response:", tool_resp)

            print("-" * 50)
    finally:
        await session.close()

if __name__ == "__main__":
    if sys.platform == "win32" and isinstance(asyncio.get_event_loop(), asyncio.SelectorEventLoop):
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    asyncio.run(main())