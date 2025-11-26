# Hướng dẫn Test MCP Server

Hướng dẫn này mô tả cách test kiotviet-mcp server, bao gồm các bước lấy token, xác định retailer và test các tools.

## Cấu trúc thư mục tests

```
tests/
├── __init__.py          # Package init
├── get_token.py         # Lấy access_token
├── get_retailer.py      # Lấy/kiểm tra retailer
├── test_mcp.py          # Test MCP server (cơ bản hoặc đầy đủ)
├── token.txt            # Token được lưu ở đây (gitignored)
└── README.md            # File này
```

## Bước 1: Lấy Access Token

### Sử dụng script `get_token.py`

```bash
source venv/bin/activate
python tests/get_token.py
```

Script sẽ:
- Đọc `CLIENT_ID` và `CLIENT_SECRET` từ `promts/auths.env`
- Gọi KiotViet OAuth2 API để lấy `access_token`
- Lưu token vào `tests/token.txt`

**Lưu ý:**
- `access_token` có thời hạn 24 giờ (86400 seconds)
- Nếu token hết hạn, chạy lại `tests/get_token.py` để lấy token mới
- Token được lưu trong `tests/token.txt` (đã gitignored)

## Bước 2: Xác định Retailer

**Retailer** là tên gian hàng bạn đã đăng ký với KiotViet.

### Sử dụng script `get_retailer.py`

```bash
# Kiểm tra retailer
python tests/get_retailer.py
```

Hoặc set environment variable:
```bash
export RETAILER=your_retailer_name
python tests/get_retailer.py
```

**Các cách khác để xác định retailer:**
1. Kiểm tra trong KiotViet dashboard
2. Hoặc thử gọi API với các tên có thể

**Lưu ý:**
- `retailer` phải khớp với tên gian hàng đã đăng ký với KiotViet
- Retailer cần được cung cấp để test các API endpoints

## Bước 3: Test MCP Server

### Cách 1: Test trực tiếp các tools

Sử dụng `test_mcp.py` để test MCP server:

**Test cơ bản** (3 tools: branches, products, customers):
```bash
source venv/bin/activate
python tests/test_mcp.py <retailer>
```

Ví dụ:
```bash
python tests/test_mcp.py nhathuoctestmcp
```

**Test đầy đủ** (5 tools: thêm orders, invoices):
```bash
python tests/test_mcp.py <retailer> --full
```

Hoặc set environment variable:
```bash
export RETAILER=your_retailer_name
python tests/test_mcp.py          # Test cơ bản
python tests/test_mcp.py --full    # Test đầy đủ
```

### Cách 2: Khởi chạy MCP Server

```bash
# Khởi chạy server
source venv/bin/activate
python kiotviet_mcp_server.py
```

Hoặc:
```bash
./start_mcp.sh
```

Server sẽ chạy và sẵn sàng nhận requests từ MCP client.

## Các Tools có thể test

1. **kv_list_branches**: Lấy danh sách chi nhánh
2. **kv_list_products**: Lấy danh sách sản phẩm
3. **kv_get_product**: Lấy thông tin chi tiết sản phẩm
4. **kv_search_customers**: Tìm kiếm khách hàng
5. **kv_get_customer**: Lấy thông tin chi tiết khách hàng
6. **kv_create_customer**: Tạo khách hàng mới
7. **kv_list_orders**: Lấy danh sách đơn hàng
8. **kv_get_order**: Lấy thông tin chi tiết đơn hàng
9. **kv_create_order**: Tạo đơn hàng mới
10. **kv_list_invoices**: Lấy danh sách hóa đơn
11. **kv_get_invoice**: Lấy thông tin chi tiết hóa đơn
12. **kv_list_categories**: Lấy danh sách nhóm hàng hóa

## Lưu ý chung

- Tất cả scripts cần chạy từ root directory của project hoặc với venv activated
- Scripts tự động tìm `promts/auths.env` ở parent directory
- Token được lưu trong `tests/token.txt` (đã gitignored)
- `access_token` có thời hạn 24 giờ (86400 seconds)
- Nếu token hết hạn, chạy lại `tests/get_token.py` để lấy token mới
- `retailer` phải khớp với tên gian hàng đã đăng ký với KiotViet

## Troubleshooting

### Lỗi: "Retailer chưa được cung cấp"
→ Cần truyền `retailer` khi test hoặc set `RETAILER` environment variable

### Lỗi: "401 Unauthorized"
→ Token đã hết hạn hoặc retailer không đúng. Lấy token mới và kiểm tra retailer.

### Lỗi: "CLIENT_ID or CLIENT_SECRET not found"
→ Kiểm tra file `promts/auths.env` có đúng format không:
```
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
```

### Lỗi khi chạy scripts
→ Đảm bảo đã activate virtual environment:
```bash
source venv/bin/activate
```

→ Đảm bảo đang chạy từ root directory của project
