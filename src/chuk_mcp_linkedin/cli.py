"""
Command-line interface for LinkedIn MCP Server.

Provides multiple modes of operation:
- STDIO mode for Claude Desktop integration
- HTTP mode for API access (future)
- Auto mode to detect best transport
"""

import argparse
import asyncio
import logging
import os
import sys
from typing import Optional

from .async_server import mcp

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def run_stdio() -> None:
    """Run server in STDIO mode for Claude Desktop integration."""
    logger.info("Starting LinkedIn MCP Server in STDIO mode")

    from mcp.server.stdio import stdio_server

    async with stdio_server() as (read_stream, write_stream):
        await mcp.run(read_stream, write_stream, mcp.create_initialization_options())  # type: ignore[attr-defined]


async def run_http(host: str = "0.0.0.0", port: int = 8000) -> None:  # nosec B104
    """
    Run server in HTTP mode for API access.

    Args:
        host: Host to bind to (default: 0.0.0.0)
        port: Port to listen on (default: 8000)
    """
    logger.info(f"Starting LinkedIn MCP Server in HTTP mode on {host}:{port}")

    try:
        from mcp.server.sse import SseServerTransport
        from starlette.applications import Starlette
        from starlette.routing import Route
        import uvicorn

        # Create SSE transport
        sse = SseServerTransport("/messages")

        # Create Starlette app
        async def handle_sse(request):  # type: ignore[no-untyped-def]
            async with sse.connect_sse(request.scope, request.receive, request._send) as streams:
                await mcp.run(streams[0], streams[1], mcp.create_initialization_options())  # type: ignore[attr-defined]

        async def handle_messages(request):  # type: ignore[no-untyped-def]
            await sse.handle_post_message(request.scope, request.receive, request._send)

        # Health check endpoint
        async def health(request):  # type: ignore[no-untyped-def]
            from starlette.responses import JSONResponse

            return JSONResponse({"status": "healthy", "mode": "http"})

        app = Starlette(
            routes=[
                Route("/sse", endpoint=handle_sse),
                Route("/messages", endpoint=handle_messages, methods=["POST"]),
                Route("/health", endpoint=health),
            ]
        )

        # Run server
        config = uvicorn.Config(app, host=host, port=port, log_level="info")
        server = uvicorn.Server(config)
        await server.serve()

    except ImportError as e:
        logger.error(f"HTTP mode requires additional dependencies: {e}")
        logger.error("Install with: uv pip install uvicorn starlette")
        sys.exit(1)


def detect_mode() -> str:
    """
    Auto-detect the best transport mode.

    Returns:
        "stdio" or "http" based on environment
    """
    # Check environment variable
    if os.environ.get("MCP_STDIO"):
        return "stdio"

    if os.environ.get("MCP_HTTP"):
        return "http"

    # Check if running in a TTY
    if not sys.stdin.isatty():
        return "stdio"

    # Default to showing help
    return "help"


def setup_logging(debug: bool = False, log_level: Optional[str] = None) -> None:
    """
    Configure logging based on arguments.

    Args:
        debug: Enable debug mode
        log_level: Explicit log level (DEBUG, INFO, WARNING, ERROR)
    """
    level = logging.DEBUG if debug else logging.INFO

    if log_level:
        level = getattr(logging, log_level.upper(), logging.INFO)

    logging.basicConfig(
        level=level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", force=True
    )


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser for CLI."""
    parser = argparse.ArgumentParser(
        description="LinkedIn MCP Server - Create and publish LinkedIn content",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run in STDIO mode (for Claude Desktop)
  %(prog)s stdio

  # Run in HTTP mode
  %(prog)s http --port 8000

  # Run with debug logging
  %(prog)s stdio --debug

  # Auto-detect mode
  %(prog)s auto

Environment Variables:
  MCP_STDIO=1           Force STDIO mode
  MCP_HTTP=1            Force HTTP mode
  LINKEDIN_ACCESS_TOKEN LinkedIn API access token
  DEBUG=1               Enable debug logging
        """,
    )

    parser.add_argument("--version", action="version", version="%(prog)s 1.0.0")

    parser.add_argument("--debug", action="store_true", help="Enable debug logging")

    parser.add_argument(
        "--log-level", choices=["DEBUG", "INFO", "WARNING", "ERROR"], help="Set logging level"
    )

    # Subcommands
    subparsers = parser.add_subparsers(dest="command", help="Server mode")

    # STDIO mode
    subparsers.add_parser("stdio", help="Run in STDIO mode (for Claude Desktop)")

    # HTTP mode
    http_parser = subparsers.add_parser("http", help="Run in HTTP mode (API server)")
    http_parser.add_argument(  # fmt: skip
        "--host",
        default="0.0.0.0",  # nosec B104
        help="Host to bind to (default: 0.0.0.0)",
    )
    http_parser.add_argument(
        "--port", type=int, default=8000, help="Port to listen on (default: 8000)"
    )

    # Auto mode
    auto_parser = subparsers.add_parser("auto", help="Auto-detect best transport mode")
    auto_parser.add_argument(  # fmt: skip
        "--http-host",
        default="0.0.0.0",  # nosec B104
        help="Host for HTTP mode (default: 0.0.0.0)",
    )
    auto_parser.add_argument(
        "--http-port", type=int, default=8000, help="Port for HTTP mode (default: 8000)"
    )

    return parser


def main() -> None:
    """Main entry point for CLI."""
    parser = create_parser()
    args = parser.parse_args()

    # Setup logging
    debug_val: bool = bool(args.debug or os.environ.get("DEBUG"))
    setup_logging(
        debug=debug_val,
        log_level=args.log_level or os.environ.get("MCP_LOG_LEVEL"),
    )

    # Handle commands
    if args.command == "stdio":
        asyncio.run(run_stdio())

    elif args.command == "http":
        asyncio.run(run_http(host=args.host, port=args.port))

    elif args.command == "auto":
        mode = detect_mode()
        if mode == "stdio":
            logger.info("Auto-detected STDIO mode")
            asyncio.run(run_stdio())
        elif mode == "http":
            logger.info("Auto-detected HTTP mode")
            asyncio.run(run_http(host=args.http_host, port=args.http_port))
        else:
            parser.print_help()

    else:
        # No command specified
        parser.print_help()
        print()
        print("Tip: Use 'stdio' for Claude Desktop, 'http' for API access")
        sys.exit(1)


if __name__ == "__main__":
    main()
