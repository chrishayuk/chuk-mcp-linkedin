# OAuth Setup Guide

This guide explains how to set up OAuth authentication for the LinkedIn MCP Server, enabling MCP clients to authorize with LinkedIn automatically.

## Architecture Overview

The LinkedIn MCP Server implements a two-layer OAuth architecture:

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────────┐
│   MCP Client    │ OAuth   │  Your MCP Server │ OAuth   │  LinkedIn API   │
│ (Claude Desktop)│◄───────►│  (This Server)   │◄───────►│                 │
└─────────────────┘         └──────────────────┘         └─────────────────┘
     Layer 1: MCP OAuth          Layer 2: LinkedIn OAuth
```

**Benefits:**
- ✅ MCP spec compliant
- ✅ Automatic LinkedIn token refresh
- ✅ Multi-user support (each MCP client user has their own LinkedIn account)
- ✅ Secure (no tokens in config files)
- ✅ One-time authorization per user

## Prerequisites

### 1. LinkedIn App Setup

You need a LinkedIn application with OAuth credentials:

1. Go to [LinkedIn Developers](https://www.linkedin.com/developers/apps)
2. Create a new app or use existing app
3. Navigate to **Auth** tab
4. Note your **Client ID** and **Client Secret**
5. Add redirect URI: `http://localhost:8000/oauth/linkedin/callback`
   - For production, use your server's public URL
6. Request these scopes:
   - `openid`
   - `profile`
   - `w_member_social` (for posting)
   - `email`

### 2. Environment Configuration

Create a `.env` file in your project root:

```bash
# LinkedIn OAuth Credentials (Required)
LINKEDIN_CLIENT_ID=your_linkedin_client_id
LINKEDIN_CLIENT_SECRET=your_linkedin_client_secret

# Session Storage (Required for Development)
SESSION_PROVIDER=memory

# Optional: OAuth Configuration
OAUTH_SERVER_URL=http://localhost:8000
LINKEDIN_REDIRECT_URI=http://localhost:8000/oauth/callback
OAUTH_ENABLED=true

# Optional: Production Redis Configuration
# SESSION_PROVIDER=redis
# SESSION_REDIS_URL=redis://localhost:6379/0
```

## Running the Server with OAuth

### Local Development

```bash
# Start server in HTTP mode (required for OAuth)
linkedin-mcp http --host 0.0.0.0 --port 8000

# Or using uv
uv run linkedin-mcp http --port 8000
```

The server will start and display:

```
✓ OAuth enabled - MCP clients can authorize with LinkedIn
  OAuth server: http://localhost:8000
  Discovery endpoint: http://localhost:8000/.well-known/oauth-authorization-server
```

### Production Deployment

For production, update environment variables:

```bash
LINKEDIN_REDIRECT_URI=https://your-server.com/oauth/linkedin/callback
OAUTH_SERVER_URL=https://your-server.com
```

And ensure your LinkedIn app has the production redirect URI registered.

## MCP Client Configuration

### Claude Desktop Configuration

Add to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "linkedin": {
      "command": "linkedin-mcp",
      "args": ["http", "--port", "8000"],
      "authorization": {
        "type": "oauth2",
        "authorization_url": "http://localhost:8000/oauth/authorize",
        "token_url": "http://localhost:8000/oauth/token"
      }
    }
  }
}
```

### Other MCP Clients

For other MCP clients, configure OAuth discovery:

- **Discovery URL**: `http://localhost:8000/.well-known/oauth-authorization-server`
- **Authorization Endpoint**: `http://localhost:8000/oauth/authorize`
- **Token Endpoint**: `http://localhost:8000/oauth/token`
- **Registration Endpoint**: `http://localhost:8000/oauth/register`

## OAuth Flow

### First-Time Authorization

1. **User starts MCP client** (e.g., Claude Desktop)
2. **Client requests authorization** from OAuth server
3. **Server redirects to LinkedIn** for user authentication
4. **User logs in** to LinkedIn and authorizes the app
5. **LinkedIn redirects back** to server with authorization code
6. **Server exchanges code** for LinkedIn access token
7. **Server creates MCP token** linked to LinkedIn account
8. **Client receives MCP token** and can make requests
9. **Server automatically refreshes** LinkedIn token when needed

### Subsequent Requests

1. MCP client includes access token in requests
2. Server validates MCP token
3. Server looks up linked LinkedIn token
4. If LinkedIn token expired, automatically refreshes
5. Uses LinkedIn token for API calls
6. Returns result to MCP client

## Testing OAuth Flow

### 1. Test OAuth Discovery

```bash
curl http://localhost:8000/.well-known/oauth-authorization-server
```

Expected response:
```json
{
  "issuer": "http://localhost:8000",
  "authorization_endpoint": "http://localhost:8000/oauth/authorize",
  "token_endpoint": "http://localhost:8000/oauth/token",
  "registration_endpoint": "http://localhost:8000/oauth/register",
  "grant_types_supported": ["authorization_code", "refresh_token"],
  "response_types_supported": ["code"],
  ...
}
```

### 2. Register Test Client

```bash
curl -X POST http://localhost:8000/oauth/register \
  -H "Content-Type: application/json" \
  -d '{
    "client_name": "Test Client",
    "redirect_uris": ["http://localhost:3000/callback"]
  }'
```

Response:
```json
{
  "client_id": "...",
  "client_secret": "...",
  "client_name": "Test Client",
  "redirect_uris": ["http://localhost:3000/callback"]
}
```

### 3. Test Authorization Flow

```bash
# Open in browser (replace CLIENT_ID with your registered client ID):
open "http://localhost:8000/oauth/authorize?response_type=code&client_id=CLIENT_ID&redirect_uri=http://localhost:3000/callback&state=test123"
```

This will:
1. Redirect to LinkedIn login
2. After LinkedIn auth, redirect to your callback with authorization code
3. Exchange code for tokens

### 4. Exchange Code for Token

```bash
curl -X POST http://localhost:8000/oauth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=authorization_code&code=AUTH_CODE&client_id=CLIENT_ID&redirect_uri=http://localhost:3000/callback"
```

Response:
```json
{
  "access_token": "...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "refresh_token": "...",
  "scope": "..."
}
```

### 5. Use Access Token

Include in MCP requests:

```bash
curl http://localhost:8000/mcp/v1/tools/list \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Token Management

### Token Storage

Tokens are stored in `.linkedin_drafts/oauth/tokens.json`:

```json
{
  "access_tokens": {
    "mcp_token": {
      "user_id": "linkedin_user_id",
      "client_id": "mcp_client_id",
      "expires_at": "2025-10-24T12:00:00"
    }
  },
  "linkedin_tokens": {
    "linkedin_user_id": {
      "access_token": "linkedin_token",
      "refresh_token": "linkedin_refresh",
      "expires_at": "2025-12-23T12:00:00"
    }
  }
}
```

### Token Lifecycle

- **MCP Access Token**: 1 hour (auto-refreshed with refresh token)
- **MCP Refresh Token**: Long-lived, rotated on each use
- **LinkedIn Access Token**: 60 days (auto-refreshed)
- **LinkedIn Refresh Token**: Permanent (unless revoked)

### Token Refresh

MCP client can refresh tokens:

```bash
curl -X POST http://localhost:8000/oauth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=refresh_token&refresh_token=REFRESH_TOKEN&client_id=CLIENT_ID"
```

## Security Features

### PKCE Support

The server supports PKCE (Proof Key for Code Exchange) for public clients:

```
Authorization: include code_challenge and code_challenge_method=S256
Token Exchange: include code_verifier
```

### Token Rotation

Refresh tokens are rotated on each use (OAuth 2.1 best practice).

### State Parameter

Always use `state` parameter for CSRF protection.

### Secure Storage

Tokens are stored locally in JSON files. For production:
- Use encrypted storage
- Set appropriate file permissions
- Consider using a database

## Troubleshooting

### OAuth Not Enabled

**Symptom**: Server shows "OAuth disabled"

**Solution**: Check environment variables:
```bash
echo $LINKEDIN_CLIENT_ID
echo $LINKEDIN_CLIENT_SECRET
```

### LinkedIn Redirect URI Mismatch

**Symptom**: LinkedIn returns "redirect_uri_mismatch"

**Solution**: Ensure redirect URI in:
1. LinkedIn app settings
2. Environment variable (`LINKEDIN_REDIRECT_URI`)
3. Server logs

All match exactly (including protocol, port, path).

### Token Expired

**Symptom**: "Invalid or expired access token"

**Solution**: Use refresh token to get new access token.

### LinkedIn Token Refresh Failed

**Symptom**: "Failed to refresh LinkedIn token"

**Possible causes**:
- User revoked access
- LinkedIn refresh token invalid
- Network error

**Solution**: User must re-authorize with LinkedIn.

## Note on Direct API Access

The MCP server uses OAuth authentication exclusively. Environment variable-based authentication (`LINKEDIN_ACCESS_TOKEN`) is only supported for standalone scripts and examples that directly call the LinkedIn API.

For the MCP server, you must use OAuth. There is no fallback to manual tokens when running the server in MCP mode.

## Advanced Configuration

### Custom Token Expiration

Modify token lifetimes in `oauth/token_store.py`:

```python
# MCP access token (default: 1 hour)
"expires_at": (datetime.now() + timedelta(hours=1)).isoformat()

# MCP refresh token (default: no expiration)
# LinkedIn access token (default: 60 days)
```

### Multiple LinkedIn Apps

Support multiple LinkedIn apps by using different redirect URIs:

```bash
LINKEDIN_CLIENT_ID_1=app1_id
LINKEDIN_CLIENT_SECRET_1=app1_secret
LINKEDIN_REDIRECT_URI_1=http://localhost:8000/oauth/linkedin/callback/app1
```

### Custom Scopes

Modify scopes in `oauth/linkedin_client.py`:

```python
DEFAULT_SCOPES = [
    "openid",
    "profile",
    "w_member_social",
    "email",
    # Add more scopes as needed
]
```

## Support

For issues or questions:
- GitHub: https://github.com/chrishayuk/chuk-mcp-linkedin/issues
- Documentation: https://github.com/chrishayuk/chuk-mcp-linkedin
