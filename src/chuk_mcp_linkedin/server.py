"""
MCP server for LinkedIn post creation.

Entry point for running the server.
The tools are registered via decorators in their respective modules.
"""

import asyncio
import os

# Import everything from async_server
from .async_server import *


def main():
    """
    Main entry point for the LinkedIn MCP server.

    Supports:
    - STDIO mode (for Claude Desktop)
    - HTTP mode (for API access - future)
    """
    # Detect mode
    mode = os.environ.get("MCP_STDIO", "stdio" if not os.isatty(0) else None)

    if mode == "stdio" or not os.isatty(0):
        # Run in STDIO mode
        asyncio.run(run_stdio())
    else:
        print("LinkedIn MCP Server")
        print("===================")
        print()
        print("Run in STDIO mode for Claude Desktop:")
        print("  python -m chuk_mcp_linkedin.server")
        print()
        print("Or set MCP_STDIO=true")


async def run_stdio():
    """Run server in STDIO mode"""
    from mcp.server.stdio import stdio_server

    async with stdio_server() as (read_stream, write_stream):
        await mcp.run(
            read_stream,
            write_stream,
            mcp.create_initialization_options()
        )


if __name__ == "__main__":
    main()
