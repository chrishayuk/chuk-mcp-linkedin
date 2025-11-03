"""
MCP server for LinkedIn post creation.

Entry point for running the server.
This module provides backward compatibility and delegates to the CLI.
"""

import sys

from .cli import main

# For backward compatibility, keep the old entry point
if __name__ == "__main__":
    # If no arguments provided, default to stdio mode
    if len(sys.argv) == 1:
        sys.argv.append("stdio")
    main()
