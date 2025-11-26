# kiotviet-mcp

MCP server kết nối đến phần mềm KiotViet thông qua API. Được xây dựng bằng FastMCP, **stateless** - không quản lý phiên của user.

> 📖 [English Version](README_EN.md) | Tiếng Việt

## Mô tả

`kiotviet-mcp` là một Model Context Protocol (MCP) server cho phép AI agents (như Culi) tương tác với KiotViet Public API một cách an toàn. Server này:

- **Stateless**: Không quản lý phiên, không lưu trữ token
- Nhận `access_token` và `retailer` từ Culi cho mỗi request
- Cung cấp các tools để truy vấn và thao tác dữ liệu KiotViet
- Đơn giản, nhẹ, không có state management

## Kiến trúc

```
┌─────────────────────────────────────────┐
│         Culi Backend                    │
│                                          │
│  1. User đăng nhập                      │
│  2. Lấy client_id, client_secret        │
│  3. Gọi OAuth2 để lấy access_token      │
│     POST https://id.kiotviet.vn/connect/token
│  4. Truyền access_token + retailer      │
│     xuống kiotviet-mcp                  │
└──────────────┬──────────────────────────┘
               │
               │ MCP Tool Call
               │ (access_token, retailer, ...)
               ▼
┌─────────────────────────────────────────┐
│      kiotviet-mcp (Stateless)            │
│                                          │
│  - Nhận access_token + retailer         │
│  - Gọi KiotViet API                     │
│  - Trả về kết quả                       │
│  - KHÔNG lưu trữ state                  │
└──────────────┬──────────────────────────┘
               │
               │ HTTP Request
               │ (Retailer header + Bearer token)
               ▼
┌─────────────────────────────────────────┐
│      KiotViet Public API                 │
└─────────────────────────────────────────┘
```

## Cài đặt

```bash
pip install -r requirements.txt
```

## Cấu trúc dự án

```
kiotviet-mcp/
├── kiotviet_mcp_server.py  # FastMCP server entrypoint
├── kv_client.py            # HTTP client cho KiotViet API (stateless)
├── requirements.txt        # Dependencies
└── README.md              # Tài liệu này
```

## Sử dụng

### Chạy MCP Server

```bash
python kiotviet_mcp_server.py
```

Hoặc nếu sử dụng với MCP client:

```bash
mcp-server kiotviet-mcp
```

### Flow hoạt động

1. **Culi Backend** lấy `access_token` từ KiotViet OAuth2:
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

2. **Culi Backend** gọi MCP tools với `access_token` và `retailer`:
   ```python
   # Culi backend gọi MCP tool
   access_token = get_access_token(client_id, client_secret)
   retailer = "taphoaxyz"
   
   # Gọi tool qua MCP
   result = kv_list_products(
       access_token=access_token,
       retailer=retailer,
       name="áo",
       page_size=20
   )
   ```

3. **kiotviet-mcp** gọi KiotViet API và trả về kết quả

### Các Tools có sẵn

#### Product Tools
- `kv_list_products`: Lấy danh sách sản phẩm
- `kv_get_product`: Lấy chi tiết sản phẩm

#### Customer Tools
- `kv_search_customers`: Tìm kiếm khách hàng
- `kv_get_customer`: Lấy chi tiết khách hàng
- `kv_create_customer`: Tạo khách hàng mới

#### Order Tools
- `kv_list_orders`: Lấy danh sách đơn hàng
- `kv_get_order`: Lấy chi tiết đơn hàng
- `kv_create_order`: Tạo đơn hàng mới

#### Invoice Tools
- `kv_list_invoices`: Lấy danh sách hóa đơn
- `kv_get_invoice`: Lấy chi tiết hóa đơn

#### Category Tools
- `kv_list_categories`: Lấy danh sách nhóm hàng

#### Branch Tools
- `kv_list_branches`: Lấy danh sách chi nhánh

## Ví dụ sử dụng

### Ví dụ 1: Lấy danh sách sản phẩm

```python
# Culi backend
access_token = get_access_token(client_id, client_secret)
retailer = "taphoaxyz"

# Gọi MCP tool
products = kv_list_products(
    access_token=access_token,
    retailer=retailer,
    name="áo",
    page_size=20
)
```

### Ví dụ 2: Tìm khách hàng

```python
customers = kv_search_customers(
    access_token=access_token,
    retailer=retailer,
    contact_number="0123456789"
)
```

### Ví dụ 3: Tạo đơn hàng

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

## Đặc điểm

### ✅ Stateless
- Không lưu trữ token
- Không quản lý phiên
- Mỗi request độc lập

### ✅ Đơn giản
- Không cần registry
- Không cần authorization
- Chỉ là proxy layer

### ✅ An toàn
- Token được quản lý bởi Culi backend
- MCP không lưu trữ thông tin nhạy cảm
- Mỗi request có token riêng

### ✅ Scalable
- Stateless → dễ scale
- Không có shared state
- Có thể chạy nhiều instances

## Token Management

**Token được quản lý bởi Culi Backend:**

- Culi lấy token từ KiotViet OAuth2
- Token có thể được cache trong Culi (tùy chọn)
- Token được truyền xuống MCP cho mỗi request
- MCP không refresh token (Culi tự refresh nếu cần)

## Resources & Prompts

Server cung cấp các resources và prompts để hướng dẫn LLM sử dụng đúng tools:

- `kiotviet://products_schema`: Schema cho products API
- `kiotviet://customers_schema`: Schema cho customers API
- `kiotviet://orders_schema`: Schema cho orders API
- `kiotviet://invoices_schema`: Schema cho invoices API
- `kiotviet_assistant_prompt`: System prompt hướng dẫn LLM

## Phát triển

### Thêm tool mới

1. Tạo function với decorator `@mcp.tool`
2. Thêm parameters: `access_token: str, retailer: str`
3. Sử dụng `_create_client(access_token, retailer)` để tạo client
4. Gọi API thông qua client methods: `get()`, `post()`, `put()`, `delete()`
5. Thêm docstring mô tả rõ ràng cho LLM

### Testing

Xem hướng dẫn chi tiết trong [TESTING.md](TESTING.md) để biết cách:
- Lấy access token
- Xác định retailer
- Test các tools
- Troubleshooting

Ví dụ test nhanh:
```bash
# Test với access_token và retailer
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

## So sánh với kiến trúc cũ

### Kiến trúc cũ (Multi-tenant với Registry)
- ❌ Phức tạp: Cần registry, authorization
- ❌ Stateful: Lưu trữ token, quản lý phiên
- ❌ Culi phải đăng ký account trước

### Kiến trúc mới (Stateless)
- ✅ Đơn giản: Chỉ là proxy
- ✅ Stateless: Không lưu trữ state
- ✅ Linh hoạt: Culi tự quản lý token

## License

MIT

## Liên hệ

Dự án này là một phần của hệ sinh thái Culi - AI agent hỗ trợ kế toán cho hộ kinh doanh.
