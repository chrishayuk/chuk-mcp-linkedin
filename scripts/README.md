# LinkedIn MCP Scripts

This directory previously contained utility scripts for direct LinkedIn API testing with manual access tokens.

## Migration to OAuth

**As of the latest version, this project uses OAuth 2.1 exclusively.**

The legacy scripts that used `LINKEDIN_ACCESS_TOKEN` have been removed:
- ~~`get_person_urn.py`~~ - Removed (OAuth handles this automatically)
- ~~`get_linkedin_token.py`~~ - Removed (use OAuth flow instead)

## For OAuth Examples

To see how OAuth authentication works, check out:
- **[examples/oauth_linkedin_example.py](../examples/oauth_linkedin_example.py)** - Complete OAuth flow demonstration
- **[docs/OAUTH.md](../docs/OAUTH.md)** - OAuth setup guide
- **[docs/OAUTH_SETUP.md](../docs/OAUTH_SETUP.md)** - OAuth configuration reference

## Running the MCP Server

The MCP server uses OAuth authentication:

```bash
# Start HTTP server with OAuth
export LINKEDIN_CLIENT_ID=your_client_id
export LINKEDIN_CLIENT_SECRET=your_client_secret
export SESSION_PROVIDER=memory
uv run linkedin-mcp http --port 8000
```

See [README.md](../README.md) for complete setup instructions.
