# Keycloak OAuth Integration

This guide explains how to use Keycloak as the OAuth provider for the LinkedIn MCP Server, implementing the OAuth Protected Resource pattern.

## Architecture Overview

```
┌─────────────┐         ┌──────────────┐         ┌──────────────┐
│ MCP Client  │────────▶│   Keycloak   │────────▶│   LinkedIn   │
│  (Claude)   │         │ (Auth Server)│         │     API      │
└─────────────┘         └──────────────┘         └──────────────┘
       │                        │
       │                        │
       ▼                        ▼
┌─────────────────────────────────────────────────────────────────┐
│                    MCP LinkedIn Server                          │
│                  (Resource Server)                              │
│                                                                 │
│  /.well-known/oauth-protected-resource                         │
│  - Points to Keycloak as authorization server                  │
│  - Does NOT proxy OAuth calls                                  │
│  - Validates Keycloak tokens                                   │
│  - Exchanges for LinkedIn tokens via Keycloak broker          │
└─────────────────────────────────────────────────────────────────┘
```

## Key Concepts

### 1. OAuth Protected Resource Pattern

The MCP server acts as a **Resource Server** (not an Authorization Server):

- **Resource Server (MCP Server)**: `http://localhost:8000`
  - Serves: `/.well-known/oauth-protected-resource`
  - Says: "I am protected. Get tokens from Keycloak."
  - Does NOT handle OAuth flows directly

- **Authorization Server (Keycloak)**: `http://localhost:8080/realms/my-realm`
  - Serves: `/.well-known/oauth-authorization-server`
  - Handles: All OAuth flows (authorize, token, refresh)
  - Manages: LinkedIn as Identity Provider

### 2. Token Flow

```
1. MCP Client → Keycloak: "I want to access MCP LinkedIn Server"
2. Keycloak → User: "Authorize with LinkedIn"
3. User → LinkedIn: Authenticates
4. LinkedIn → Keycloak: Returns LinkedIn token
5. Keycloak: Stores LinkedIn token (if "Store Tokens" enabled)
6. Keycloak → MCP Client: Returns Keycloak token
7. MCP Client → MCP Server: Sends Keycloak token
8. MCP Server → Keycloak: Validates token + gets LinkedIn token
9. MCP Server → LinkedIn API: Uses LinkedIn token
```

## Setup Instructions

### Step 1: Configure Keycloak

#### 1.1 Create Realm

```bash
# Access Keycloak admin console
http://localhost:8080/admin

# Create a new realm (or use existing)
Realm name: my-realm
```

#### 1.2 Configure LinkedIn Identity Provider

1. Navigate to: **Identity Providers** → **Add provider** → **LinkedIn**

2. Configure LinkedIn IdP **General Settings**:
   ```
   Alias: linkedin
   Display Name: LinkedIn
   Enabled: ON
   Store Tokens: ON  ⚠️ CRITICAL - Must be enabled!
   Trust Email: ON
   ```

3. Get LinkedIn OAuth credentials from: https://www.linkedin.com/developers/apps
   - Your LinkedIn app must have **Community Management API** or **Share on LinkedIn** product access
   - Required scopes in LinkedIn app: `openid`, `profile`, `w_member_social`, `email`

4. Configure **OAuth Settings** in Keycloak:
   ```
   Client ID: [Your LinkedIn App Client ID]
   Client Secret: [Your LinkedIn App Client Secret]
   ```

5. **CRITICAL: Configure LinkedIn Scopes in Keycloak**
   
   Scroll down to **Advanced Settings** section and find the **Scopes** field:
   ```
   Scopes: openid profile w_member_social email
   ```
   
   ⚠️ **Important**: This tells Keycloak which scopes to request from LinkedIn when users authenticate. Without `w_member_social`, the stored LinkedIn token won't have posting permissions, resulting in 403 errors.

6. Copy the **Redirect URI** from Keycloak:
   ```
   http://localhost:8080/realms/my-realm/broker/linkedin/endpoint
   ```

7. Add this Redirect URI to your LinkedIn app settings

8. Click **Save** to apply all changes

#### 1.3 Configure Token Broker Permissions

Users need permission to read their own stored tokens.

**Add read-token to Default Realm Role (Recommended)**

This automatically grants all users permission to read their stored tokens:

1. Navigate to: **Realm Settings** → **User Registration** tab
2. Scroll down to **Default Roles** section
3. Click **Assign role** button
4. In the dialog, search for `read-token`
5. Select the checkbox next to `read-token` role
6. Click **Assign** button

Now all users (existing and new) will have permission to read their stored LinkedIn tokens.

⚠️ **Important**: Without the `read-token` role, users will get a 403 Forbidden error when the MCP server tries to retrieve their LinkedIn tokens from Keycloak.

#### 1.4 Create OpenID Scope (If Missing)

⚠️ **Important**: Some Keycloak configurations may be missing the `openid` scope. Check if it exists first:

1. Navigate to: **Client scopes**
2. Look for a scope named `openid`
3. If it exists, skip to step 1.5

**If `openid` scope is missing, create it:**

1. Navigate to: **Client scopes** → **Create client scope**

2. Fill in the form:
   ```
   Name: openid
   Description: OpenID Connect built-in scope: openid
   Type: Default
   Protocol: OpenID Connect
   Display on consent screen: OFF
   Include in token scope: ON
   ```

3. Click **Save**

#### 1.5 Create MCP Client

Create a client in Keycloak for MCP applications to authenticate:

1. Navigate to: **Clients** → **Create client**

2. **General Settings:**
   ```
   Client type: OpenID Connect
   Client ID: mcp-linkedin-client
   ```
   Click **Next**

3. **Capability config:**
   ```
   Client authentication: ON (for confidential) or OFF (for public)
   Authorization: OFF
   Authentication flow:
     ☑ Standard flow
     ☐ Direct access grants (optional)
     ☐ Implicit flow
     ☐ Service accounts roles
   ```
   Click **Next**

4. **Login settings:**
   ```
   Valid redirect URIs: http://localhost:4444/oauth/callback
   Valid post logout redirect URIs: +
   Web origins: +
   ```
   Click **Save**

5. **Configure PKCE Support (CRITICAL):**
   - Go to **Advanced** tab (or scroll down to Advanced Settings)
   - Find: **Proof Key for Code Exchange Code Challenge Method**
   - Set to: **S256** (recommended) or **plain**
   - Click **Save**

6. **Add Required Client Scopes:**
   - Go to **Client Scopes** tab
   - Check **Assigned default client scopes** section
   - Ensure these scopes are present:
     - `openid` (REQUIRED - without this you'll get 403 errors)
     - `profile`
     - `email`
   - If any are missing:
     - Click **Add client scope**
     - Select the missing scope
     - Click **Add** → **Default**

7. **Get Client Credentials (if confidential):**
   - Go to **Credentials** tab
   - Copy the **Client Secret** (click eye icon to reveal)
   - Store securely - you'll need this for your MCP client


### Step 2: Configure MCP LinkedIn Server

#### 2.1 Environment Variables

Create `.env` file:

```bash
# Enable Keycloak mode
OAUTH_MODE=keycloak
OAUTH_ENABLED=true
OAUTH_SERVER_URL=http://localhost:8000

# Keycloak configuration
KEYCLOAK_BASE_URL=http://localhost:8080
KEYCLOAK_REALM=my-realm
KEYCLOAK_PROVIDER_ALIAS=linkedin

# Session storage
SESSION_PROVIDER=memory
```

#### 2.2 Start MCP Server

```bash
# Install dependencies
pip install -e .

# Run server
python -m chuk_mcp_linkedin.cli
```

You should see:
```
✓ OAuth enabled - Keycloak mode
  MCP Resource Server: http://localhost:8000
  Keycloak Authorization Server: http://localhost:8080/realms/my-realm
  Protected Resource: http://localhost:8000/.well-known/oauth-protected-resource
  LinkedIn Provider Alias: linkedin

  ⚠️  Important Keycloak Configuration:
     1. Enable 'Store Tokens' in LinkedIn Identity Provider settings
     2. Add 'broker -> read-token' role to users
     3. Configure LinkedIn as Identity Provider in Keycloak
```

### Step 3: Test the Integration

#### 3.1 Verify OAuth Metadata

```bash
# Check Protected Resource metadata
curl http://localhost:8000/.well-known/oauth-protected-resource

# Expected response:
{
  "resource": "http://localhost:8000",
  "authorization_servers": [
    "http://localhost:8080/realms/my-realm"
  ],
  "scopes_supported": [
    "linkedin.posts",
    "linkedin.profile",
    "linkedin.documents"
  ]
}

```

## How It Works

### Token Validation Flow

When an MCP client makes a request:

```python
# 1. Client sends Keycloak token
Authorization: Bearer <keycloak_token>

# 2. MCP Server validates with Keycloak
GET http://localhost:8080/realms/my-realm/protocol/openid-connect/userinfo
Authorization: Bearer <keycloak_token>

# 3. MCP Server gets LinkedIn token from Keycloak
GET http://localhost:8080/realms/my-realm/broker/linkedin/token
Authorization: Bearer <keycloak_token>

# 4. MCP Server uses LinkedIn token for API calls
GET https://api.linkedin.com/v2/userinfo
Authorization: Bearer <linkedin_token>
```

### Code Implementation

The `KeycloakOAuthProvider` class handles this flow:

```python
async def validate_access_token(self, token: str) -> Dict[str, Any]:
    # 1. Validate Keycloak token
    user_info = await self._get_keycloak_userinfo(token)
    user_id = user_info["sub"]
    
    # 2. Get LinkedIn token from Keycloak broker
    linkedin_token = await self._get_linkedin_token(token)
    
    # 3. Return token data
    return {
        "user_id": user_id,
        "external_access_token": linkedin_token,
    }
```

## OAuth Endpoints Reference

### Keycloak Authorization Server Endpoints

For realm **"my-realm"**, the following endpoints are available:

**Authorization Endpoint:**
```
http://localhost:8080/realms/my-realm/protocol/openid-connect/auth
```

**Token Endpoint:**
```
http://localhost:8080/realms/my-realm/protocol/openid-connect/token
```

**Userinfo Endpoint:**
```
http://localhost:8080/realms/my-realm/protocol/openid-connect/userinfo
```

**Token Broker Endpoint** (LinkedIn token exchange):
```
http://localhost:8080/realms/my-realm/broker/linkedin/token
```

**Registration Endpoint** (Dynamic Client Registration):
```
http://localhost:8080/realms/my-realm/clients-registrations/openid-connect
```

**Discovery Endpoint:**
```
http://localhost:8080/realms/my-realm/.well-known/openid-configuration
```

### MCP Server Endpoints

**Protected Resource Metadata:**
```
http://localhost:8000/.well-known/oauth-protected-resource
```

## Troubleshooting

### Error: LinkedIn 403 "ACCESS_DENIED" - Not enough permissions

**Symptom**: When publishing posts, you get:
```json
{
  "status": "error",
  "error": "LinkedIn API error: 403 - {'status': 403, 'serviceErrorCode': 100, 'code': 'ACCESS_DENIED', 'message': 'Not enough permissions to access: partnerApiPostsExternal.CREATE'}"
}
```

**Cause**: The LinkedIn token stored in Keycloak doesn't have the `w_member_social` scope. This happens when:
1. The LinkedIn IdP scopes were not configured before first authentication
2. You added `w_member_social` to IdP scopes AFTER the user already authenticated

**Solution**: Force LinkedIn re-authentication to get a new token with correct scopes

1. Go to: `http://localhost:8080/admin`
2. Navigate to: **Users** → Search for your user
3. Click on the user to open details
4. Go to **Identity provider links** tab (or **Federated Identity**)
5. Find the **LinkedIn** row
6. Click **Unlink** or **Delete** button
7. Confirm the deletion

**Then:**

1. Clear MCP server tokens:
   ```bash
   rm -rf .linkedin_drafts/oauth/
   ```

2. Restart MCP server:
   ```bash
   linkedin-mcp http --port 8000
   ```

3. Restart your MCP client (e.g., restart Claude Desktop)

4. When you authenticate again:
   - Keycloak will redirect to LinkedIn
   - LinkedIn will show authorization screen with ALL permissions (including posting)
   - Click "Allow"
   - New token will have `w_member_social` scope
   - Posts will work! ✅

**Verify the fix:**
```
publish_post(text="Test post with correct scopes!", visibility="PUBLIC")
```

### Error: "Invalid scopes: openid profile w_member_social email"

**Symptom**: Keycloak logs show:
```
error="invalid_request", reason="Invalid scopes: openid profile w_member_social email"
```

**Cause**: Your MCP client is requesting `w_member_social` from Keycloak, but that's a LinkedIn scope, not a Keycloak scope.

**Solution**: Update your MCP client configuration to request only Keycloak scopes:

```json
{
  "mcpServers": {
    "linkedin": {
      "authorization": {
        "scope": "openid profile email"
      }
    }
  }
}
```

**Key points:**
- ✅ MCP Client → Keycloak: `openid profile email` (Keycloak scopes)
- ✅ Keycloak → LinkedIn: `openid profile w_member_social email` (configured in IdP)
- ❌ Don't request `w_member_social` from Keycloak - it doesn't recognize it

### Error: "Invalid parameter: code_challenge"

**Cause**: PKCE is not enabled for the client, even though the client is sending PKCE parameters.

**Solution**:

1. **Via Admin Console:**
   - Go to: `http://localhost:8080/admin`
   - Navigate to: **Clients** → **mcp-linkedin-client** → **Settings**
   - Scroll to **Advanced Settings**
   - Set **Proof Key for Code Exchange Code Challenge Method** to: **S256**
   - Click **Save**

**Note**: If you're using a **confidential client** (with client secret), PKCE is optional but recommended for additional security. If you're using a **public client** (no secret), PKCE is required for security.

## Advantages of Keycloak Mode

1. **Centralized Authentication**: Single sign-on across multiple services
2. **Token Management**: Keycloak handles token storage and refresh
3. **Security**: Tokens never exposed to MCP server
4. **Flexibility**: Easy to add more identity providers
5. **Enterprise Ready**: LDAP, SAML, 2FA support

## Client Types: Public vs Confidential

Understanding the difference between public and confidential clients is crucial for proper OAuth configuration:

### Public Client (`publicClient: true`)

**Characteristics:**
- ❌ **No client secret** - cannot keep secrets safe
- ✅ **Must use PKCE** for security
- 🎯 **Use cases**: Browser apps, mobile apps, desktop apps, CLI tools
- 🔒 **Security**: PKCE prevents authorization code interception

**Configuration:**
```
Client authentication: OFF
Standard flow: ON
PKCE Code Challenge Method: S256 (required)
```

**When to use:**
- MCP clients running on user devices
- Applications where code is visible to users
- Cannot securely store client secret

### Confidential Client (`publicClient: false`)

**Characteristics:**
- ✅ **Has client secret** - can keep secrets safe
- ⚠️ **PKCE optional** but recommended
- 🎯 **Use cases**: Server-to-server, backend services, trusted environments
- 🔒 **Security**: Client secret + optional PKCE for defense in depth

**Configuration:**
```
Client authentication: ON
Standard flow: ON
PKCE Code Challenge Method: S256 (recommended)
```

**When to use:**
- MCP servers or gateways
- Backend services
- Applications running in secure environments

### How to Get Client Secret

**For Confidential Clients Only:**

1. Go to Keycloak Admin Console: `http://localhost:8080/admin`
2. Navigate to: **Clients** → **mcp-linkedin-client**
3. Go to **Credentials** tab
4. Click the **eye icon** 👁️ to reveal the secret
5. Click **Copy** to copy to clipboard

**To Regenerate Secret:**
1. Go to **Credentials** tab
2. Click **Regenerate** button
3. Copy the new secret immediately

**Note**: If you don't see the Credentials tab, your client is set to public. Change **Client authentication** to **ON** in Settings to make it confidential.

### Choosing the Right Type

| Scenario | Client Type | PKCE | Secret |
|----------|-------------|------|--------|
| MCP client on user's machine | Public | Required | No |
| MCP gateway/proxy server | Confidential | Recommended | Yes |
| Browser-based app | Public | Required | No |
| Server-to-server | Confidential | Recommended | Yes |

## Comparison: LinkedIn Direct vs Keycloak Mode

| Feature | LinkedIn Direct | Keycloak Mode |
|---------|----------------|---------------|
| OAuth Server | MCP Server | Keycloak |
| Token Storage | MCP Server | Keycloak |
| LinkedIn Credentials | Required | Not required (in Keycloak) |
| Token Refresh | MCP Server | Keycloak |
| Multi-Provider | No | Yes |
| SSO Support | No | Yes |
| Enterprise Features | No | Yes |

## Security Considerations

1. **Token Storage**: LinkedIn tokens stored in Keycloak, not MCP server
2. **Token Scope**: MCP server only gets tokens for authenticated users
3. **Token Validation**: Every request validated with Keycloak
4. **Token Expiry**: Keycloak manages token lifecycle
5. **Audit Trail**: Keycloak logs all authentication events

## Production Deployment

### Keycloak Configuration

```bash
# Use PostgreSQL for production
KEYCLOAK_DB=postgres
KEYCLOAK_DB_URL=jdbc:postgresql://localhost/keycloak
KEYCLOAK_DB_USERNAME=keycloak
KEYCLOAK_DB_PASSWORD=secure_password

# Enable HTTPS
KEYCLOAK_HTTPS_CERTIFICATE_FILE=/path/to/cert.pem
KEYCLOAK_HTTPS_CERTIFICATE_KEY_FILE=/path/to/key.pem
```

### MCP Server Configuration

```bash
# Use Redis for session storage
SESSION_PROVIDER=redis
SESSION_REDIS_URL=redis://localhost:6379/0

# Use HTTPS
OAUTH_SERVER_URL=https://mcp.example.com
KEYCLOAK_BASE_URL=https://keycloak.example.com
```

## References

- [Keycloak Documentation](https://www.keycloak.org/docs/latest/)
- [OAuth 2.0 Protected Resource Metadata](https://datatracker.ietf.org/doc/html/rfc8414)
- [LinkedIn OAuth Documentation](https://learn.microsoft.com/en-us/linkedin/shared/authentication/authorization-code-flow)
- [Keycloak Identity Brokering](https://www.keycloak.org/docs/latest/server_admin/#_identity_broker)