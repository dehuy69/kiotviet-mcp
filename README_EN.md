# kiotviet-mcp

MCP server connecting to KiotViet software through API. Built with FastMCP, **stateless** - does not manage user sessions.

> 📖 English | [Tiếng Việt](README.md)

## Description

`kiotviet-mcp` is a Model Context Protocol (MCP) server that allows AI agents (like Culi) to interact with KiotViet Public API securely. This server:

- **Stateless**: Does not manage sessions, does not store tokens
- Receives `access_token` and `retailer` from Culi for each request
- Provides tools to query and manipulate KiotViet data
- Simple, lightweight, no state management

## Architecture

```
┌─────────────────────────────────────────┐
│         Culi Backend                    │
│                                          │
│  1. User login                          │
│  2. Get client_id, client_secret        │
│  3. Call OAuth2 to get access_token     │
│     POST https://id.kiotviet.vn/connect/token
│  4. Pass access_token + retailer        │
│     to kiotviet-mcp                     │
└──────────────┬──────────────────────────┘
               │
               │ MCP Tool Call
               │ (access_token, retailer, ...)
               ▼
┌─────────────────────────────────────────┐
│      kiotviet-mcp (Stateless)            │
│                                          │
│  - Receives access_token + retailer     │
│  - Calls KiotViet API                  │
│  - Returns results                     │
│  - DOES NOT store state                │
└──────────────┬──────────────────────────┘
               │
               │ HTTP Request
               │ (Retailer header + Bearer token)
               ▼
┌─────────────────────────────────────────┐
│      KiotViet Public API                 │
└─────────────────────────────────────────┘
```

## Installation

```bash
pip install -r requirements.txt
```

## Project Structure

```
kiotviet-mcp/
├── kiotviet_mcp_server.py  # FastMCP server entrypoint
├── kv_client.py            # HTTP client for KiotViet API (stateless)
├── requirements.txt        # Dependencies
└── README.md              # This documentation
```

## Usage

### Running MCP Server

```bash
python kiotviet_mcp_server.py
```

Or if using with MCP client:

```bash
mcp-server kiotviet-mcp
```

### Workflow

1. **Culi Backend** gets `access_token` from KiotViet OAuth2:
   ```python
   # Culi backend
   import httpx
   
   TOKEN_URL = "https://id.kiotviet.vn/connect/token"
   
   def get_access_token(client_id: str, client_secret: str) -> str:
       data = {
           "scopes": "PublicApi.Access",
           "grant_type": "client_credentials",
           "client_id": client_id,
           "client_secret": client_secret,
       }
       headers = {"Content-Type": "application/x-www-form-urlencoded"}
       resp = httpx.post(TOKEN_URL, data=data, headers=headers)
       resp.raise_for_status()
       return resp.json()["access_token"]
   ```

2. **Culi Backend** calls MCP tools with `access_token` and `retailer`:
   ```python
   # Culi backend calls MCP tool
   access_token = get_access_token(client_id, client_secret)
   retailer = "taphoaxyz"
   
   # Call tool via MCP
   result = kv_list_products(
       access_token=access_token,
       retailer=retailer,
       name="shirt",
       page_size=20
   )
   ```

3. **kiotviet-mcp** calls KiotViet API and returns results

### Available Tools

#### Product Tools
- `kv_list_products`: Get list of products
- `kv_get_product`: Get product details

#### Customer Tools
- `kv_search_customers`: Search customers
- `kv_get_customer`: Get customer details
- `kv_create_customer`: Create new customer

#### Order Tools
- `kv_list_orders`: Get list of orders
- `kv_get_order`: Get order details
- `kv_create_order`: Create new order

#### Invoice Tools
- `kv_list_invoices`: Get list of invoices
- `kv_get_invoice`: Get invoice details

#### Category Tools
- `kv_list_categories`: Get list of product categories

#### Branch Tools
- `kv_list_branches`: Get list of branches

## Usage Examples

### Example 1: Get list of products

```python
# Culi backend
access_token = get_access_token(client_id, client_secret)
retailer = "taphoaxyz"

# Call MCP tool
products = kv_list_products(
    access_token=access_token,
    retailer=retailer,
    name="shirt",
    page_size=20
)
```

### Example 2: Search customers

```python
customers = kv_search_customers(
    access_token=access_token,
    retailer=retailer,
    contact_number="0123456789"
)
```

### Example 3: Create order

```python
order = kv_create_order(
    access_token=access_token,
    retailer=retailer,
    branch_id=1,
    purchase_date="2024-01-15",
    order_details=[
        {
            "productId": 123,
            "quantity": 2,
            "price": 100000
        }
    ],
    customer_id=456
)
```

## Features

### ✅ Stateless
- Does not store tokens
- Does not manage sessions
- Each request is independent

### ✅ Simple
- No registry needed
- No authorization needed
- Just a proxy layer

### ✅ Secure
- Tokens managed by Culi backend
- MCP does not store sensitive information
- Each request has its own token

### ✅ Scalable
- Stateless → easy to scale
- No shared state
- Can run multiple instances

## Token Management

**Tokens are managed by Culi Backend:**

- Culi gets token from KiotViet OAuth2
- Token can be cached in Culi (optional)
- Token is passed to MCP for each request
- MCP does not refresh token (Culi refreshes if needed)

## Resources & Prompts

Server provides resources and prompts to guide LLM to use tools correctly:

- `kiotviet://products_schema`: Schema for products API
- `kiotviet://customers_schema`: Schema for customers API
- `kiotviet://orders_schema`: Schema for orders API
- `kiotviet://invoices_schema`: Schema for invoices API
- `kiotviet_assistant_prompt`: System prompt to guide LLM

## Development

### Adding a new tool

1. Create function with `@mcp.tool` decorator
2. Add parameters: `access_token: str, retailer: str`
3. Use `_create_client(access_token, retailer)` to create client
4. Call API through client methods: `get()`, `post()`, `put()`, `delete()`
5. Add clear docstring for LLM

### Testing

See detailed guide in [TESTING.md](TESTING.md) for:
- Getting access token
- Determining retailer
- Testing tools
- Troubleshooting

Quick test example:
```bash
# Test with access_token and retailer
python -c "
from kiotviet_mcp_server import kv_list_products
result = kv_list_products(
    access_token='your_token',
    retailer='your_retailer',
    page_size=10
)
print(result)
"
```

## Comparison with Old Architecture

### Old Architecture (Multi-tenant with Registry)
- ❌ Complex: Requires registry, authorization
- ❌ Stateful: Stores tokens, manages sessions
- ❌ Culi must register account first

### New Architecture (Stateless)
- ✅ Simple: Just a proxy
- ✅ Stateless: Does not store state
- ✅ Flexible: Culi manages tokens itself

## License

MIT

## Contact

This project is part of the Culi ecosystem - AI agent supporting accounting for small businesses.

