"""
KiotViet MCP Server - FastMCP implementation
Stateless: receives access_token and retailer from Culi, no session management.

KiotViet MCP Server - Triển khai FastMCP
Stateless: nhận access_token và retailer từ Culi, không quản lý phiên.
"""
from fastmcp import FastMCP
from fastmcp.prompts.prompt import PromptMessage, TextContent
from typing import Optional, List, Dict, Any
from kv_client import KiotVietClient

# Initialize FastMCP server / Khởi tạo FastMCP server
mcp = FastMCP(name="kiotviet-mcp")


def _create_client(access_token: str, retailer: str) -> KiotVietClient:
    """
    Create KiotVietClient from access_token and retailer.
    Tạo KiotVietClient từ access_token và retailer.
    
    Args:
        access_token: OAuth2 access token (obtained by Culi) / Token OAuth2 (do Culi cung cấp)
        retailer: Retailer name (tên gian hàng)
    
    Returns:
        KiotVietClient instance / Instance KiotVietClient
    """
    return KiotVietClient(access_token=access_token, retailer=retailer)


# ============================================================================
# Product Tools / Công cụ Sản phẩm
# ============================================================================

@mcp.tool
def kv_list_products(
    access_token: str,
    retailer: str,
    page_size: int = 50,
    current_item: int = 0,
    name: Optional[str] = None,
    category_id: Optional[int] = None,
    include_inventory: bool = True,
    order_by: Optional[str] = None,
    order_direction: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Get list of KiotViet products.
    Lấy danh sách sản phẩm KiotViet.
    Used when agent wants to look up products, reports, price consultation, inventory, etc.
    Dùng khi agent muốn tra cứu hàng hóa, báo cáo, tư vấn giá, tồn kho,...
    
    Args:
        access_token: OAuth2 access token (provided by Culi) / Token OAuth2 (do Culi cung cấp)
        retailer: KiotViet retailer name / Tên gian hàng KiotViet
        page_size: Number of items per page (default 50, max 100) / Số items trong 1 trang (mặc định 50, tối đa 100)
        current_item: Get data from current record (default 0) / Lấy dữ liệu từ bản ghi hiện tại (mặc định 0)
        name: Search by product name / Tìm kiếm theo tên sản phẩm
        category_id: Filter by category ID / Lọc theo ID nhóm hàng
        include_inventory: Whether to include inventory information / Có lấy thông tin tồn kho hay không
        order_by: Sort by field (e.g., "name", "code") / Sắp xếp theo trường (ví dụ: "name", "code")
        order_direction: Sort direction ("Asc" or "Desc") / Hướng sắp xếp ("Asc" hoặc "Desc")
    """
    client = _create_client(access_token, retailer)
    params: Dict[str, Any] = {
        "pageSize": min(page_size, 100),  # Max 100 / Tối đa 100
        "currentItem": current_item,
        "includeInventory": include_inventory,
    }
    if name:
        params["name"] = name
    if category_id:
        params["categoryId"] = category_id
    if order_by:
        params["orderBy"] = order_by
    if order_direction:
        params["orderDirection"] = order_direction

    return client.get("/products", params)


@mcp.tool
def kv_get_product(
    access_token: str,
    retailer: str,
    product_id: Optional[int] = None,
    product_code: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Get detailed information of a product by ID or product code.
    Lấy thông tin chi tiết của một sản phẩm theo ID hoặc mã sản phẩm.
    
    Args:
        access_token: OAuth2 access token (provided by Culi) / Token OAuth2 (do Culi cung cấp)
        retailer: KiotViet retailer name / Tên gian hàng KiotViet
        product_id: Product ID / ID sản phẩm
        product_code: Product code (if product_id is not provided) / Mã sản phẩm (nếu không có product_id)
    """
    client = _create_client(access_token, retailer)
    if product_id:
        return client.get(f"/products/{product_id}")
    elif product_code:
        return client.get(f"/products/code/{product_code}")
    else:
        raise ValueError("Need to provide product_id or product_code / Cần cung cấp product_id hoặc product_code")


# ============================================================================
# Customer Tools / Công cụ Khách hàng
# ============================================================================

@mcp.tool
def kv_search_customers(
    access_token: str,
    retailer: str,
    name: Optional[str] = None,
    contact_number: Optional[str] = None,
    code: Optional[str] = None,
    page_size: int = 20,
    current_item: int = 0,
    include_total: bool = False,
) -> Dict[str, Any]:
    """
    Search customers by name, phone number, or customer code.
    Tìm khách hàng theo tên, số điện thoại hoặc mã khách hàng.
    
    Args:
        access_token: OAuth2 access token (provided by Culi) / Token OAuth2 (do Culi cung cấp)
        retailer: KiotViet retailer name / Tên gian hàng KiotViet
        name: Search by customer name / Tìm kiếm theo tên khách hàng
        contact_number: Search by phone number / Tìm kiếm theo số điện thoại
        code: Search by customer code / Tìm kiếm theo mã khách hàng
        page_size: Number of items per page (default 20, max 100) / Số items trong 1 trang (mặc định 20, tối đa 100)
        current_item: Get data from current record (default 0) / Lấy dữ liệu từ bản ghi hiện tại (mặc định 0)
        include_total: Whether to include TotalInvoice, TotalPoint, TotalRevenue / Có lấy thông tin TotalInvoice, TotalPoint, TotalRevenue
    """
    client = _create_client(access_token, retailer)
    params: Dict[str, Any] = {
        "pageSize": min(page_size, 100),
        "currentItem": current_item,
        "includeTotal": include_total,
    }
    if name:
        params["name"] = name
    if contact_number:
        params["contactNumber"] = contact_number
    if code:
        params["code"] = code

    return client.get("/customers", params)


@mcp.tool
def kv_get_customer(
    access_token: str,
    retailer: str,
    customer_id: Optional[int] = None,
    customer_code: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Get detailed information of a customer by ID or customer code.
    Lấy thông tin chi tiết của một khách hàng theo ID hoặc mã khách hàng.
    
    Args:
        access_token: OAuth2 access token (provided by Culi) / Token OAuth2 (do Culi cung cấp)
        retailer: KiotViet retailer name / Tên gian hàng KiotViet
        customer_id: Customer ID / ID khách hàng
        customer_code: Customer code (if customer_id is not provided) / Mã khách hàng (nếu không có customer_id)
    """
    client = _create_client(access_token, retailer)
    if customer_id:
        return client.get(f"/customers/{customer_id}")
    elif customer_code:
        return client.get(f"/customers/code/{customer_code}")
    else:
        raise ValueError("Need to provide customer_id or customer_code / Cần cung cấp customer_id hoặc customer_code")


@mcp.tool
def kv_create_customer(
    access_token: str,
    retailer: str,
    name: str,
    code: Optional[str] = None,
    contact_number: Optional[str] = None,
    email: Optional[str] = None,
    address: Optional[str] = None,
    gender: Optional[bool] = None,
    birth_date: Optional[str] = None,
    comments: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Create a new customer in KiotViet.
    Tạo mới khách hàng trong KiotViet.
    
    Args:
        access_token: OAuth2 access token (provided by Culi) / Token OAuth2 (do Culi cung cấp)
        retailer: KiotViet retailer name / Tên gian hàng KiotViet
        name: Customer name (required) / Tên khách hàng (bắt buộc)
        code: Customer code / Mã khách hàng
        contact_number: Phone number / Số điện thoại
        email: Email address / Email
        address: Address / Địa chỉ
        gender: Gender (true: male, false: female) / Giới tính (true: nam, false: nữ)
        birth_date: Birth date (format: YYYY-MM-DD) / Ngày sinh (format: YYYY-MM-DD)
        comments: Notes / Ghi chú
    """
    client = _create_client(access_token, retailer)
    body: Dict[str, Any] = {
        "name": name,
    }
    if code:
        body["code"] = code
    if contact_number:
        body["contactNumber"] = contact_number
    if email:
        body["email"] = email
    if address:
        body["address"] = address
    if gender is not None:
        body["gender"] = gender
    if birth_date:
        body["birthDate"] = birth_date
    if comments:
        body["comments"] = comments

    return client.post("/customers", body)


# ============================================================================
# Order Tools / Công cụ Đơn hàng
# ============================================================================

@mcp.tool
def kv_list_orders(
    access_token: str,
    retailer: str,
    branch_ids: Optional[List[int]] = None,
    status: Optional[List[int]] = None,
    customer_ids: Optional[List[int]] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    page_size: int = 50,
    current_item: int = 0,
    include_payment: bool = False,
) -> Dict[str, Any]:
    """
    Get list of orders from KiotViet.
    Lấy danh sách đơn đặt hàng (orders) từ KiotViet.
    Used by agent to view revenue, undelivered orders, unpaid orders, etc.
    Agent dùng để xem doanh thu, đơn chưa giao, đơn chưa thanh toán,...
    
    Args:
        access_token: OAuth2 access token (provided by Culi) / Token OAuth2 (do Culi cung cấp)
        retailer: KiotViet retailer name / Tên gian hàng KiotViet
        branch_ids: Filter by list of branch IDs / Lọc theo danh sách ID chi nhánh
        status: Filter by order status (list of numbers) / Lọc theo trạng thái đơn hàng (danh sách số)
        customer_ids: Filter by list of customer IDs / Lọc theo danh sách ID khách hàng
        from_date: From date (format: YYYY-MM-DD) / Từ ngày (format: YYYY-MM-DD)
        to_date: To date (format: YYYY-MM-DD) / Đến ngày (format: YYYY-MM-DD)
        page_size: Number of items per page (default 50, max 100) / Số items trong 1 trang (mặc định 50, tối đa 100)
        current_item: Get data from current record (default 0) / Lấy dữ liệu từ bản ghi hiện tại (mặc định 0)
        include_payment: Whether to include payment information / Có lấy thông tin thanh toán hay không
    """
    client = _create_client(access_token, retailer)
    params: Dict[str, Any] = {
        "pageSize": min(page_size, 100),
        "currentItem": current_item,
        "includePayment": include_payment,
    }
    if branch_ids:
        params["branchIds"] = branch_ids
    if status:
        params["status"] = status
    if customer_ids:
        params["customerIds"] = customer_ids
    if from_date:
        params["fromDate"] = from_date
    if to_date:
        params["toDate"] = to_date

    return client.get("/orders", params)


@mcp.tool
def kv_get_order(
    access_token: str,
    retailer: str,
    order_id: Optional[int] = None,
    order_code: Optional[str] = None,
    include_payment: bool = False,
) -> Dict[str, Any]:
    """
    Get detailed information of an order by ID or order code.
    Lấy thông tin chi tiết của một đơn hàng theo ID hoặc mã đơn hàng.
    
    Args:
        access_token: OAuth2 access token (provided by Culi) / Token OAuth2 (do Culi cung cấp)
        retailer: KiotViet retailer name / Tên gian hàng KiotViet
        order_id: Order ID / ID đơn hàng
        order_code: Order code (if order_id is not provided) / Mã đơn hàng (nếu không có order_id)
        include_payment: Whether to include payment information / Có lấy thông tin thanh toán hay không
    """
    client = _create_client(access_token, retailer)
    params = {"includePayment": include_payment} if include_payment else None
    
    if order_id:
        return client.get(f"/orders/{order_id}", params)
    elif order_code:
        return client.get(f"/orders/code/{order_code}", params)
    else:
        raise ValueError("Need to provide order_id or order_code / Cần cung cấp order_id hoặc order_code")


@mcp.tool
def kv_create_order(
    access_token: str,
    retailer: str,
    branch_id: int,
    purchase_date: str,
    order_details: List[Dict[str, Any]],
    customer_id: Optional[int] = None,
    description: Optional[str] = None,
    total_payment: Optional[float] = None,
    discount: Optional[float] = None,
    method: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Create a new KiotViet order. Only call after user has confirmed the content.
    Tạo mới đơn đặt hàng KiotViet. Chỉ gọi sau khi user đã xác nhận nội dung.
    
    Args:
        access_token: OAuth2 access token (provided by Culi) / Token OAuth2 (do Culi cung cấp)
        retailer: KiotViet retailer name / Tên gian hàng KiotViet
        branch_id: Branch ID / ID chi nhánh
        purchase_date: Purchase date (format: YYYY-MM-DD) / Ngày đặt hàng (format: YYYY-MM-DD)
        order_details: List of products, each item includes: / Danh sách sản phẩm, mỗi item gồm:
            - productId: Product ID / ID sản phẩm
            - quantity: Quantity / Số lượng
            - price: Price / Giá
            - discount (optional): Discount / Giảm giá
        customer_id: Customer ID (optional) / ID khách hàng (optional)
        description: Notes / Ghi chú
        total_payment: Total amount paid by customer / Tổng tiền khách đã trả
        discount: Order discount / Giảm giá trên đơn
        method: Payment method (Cash, Card, Transfer) / Phương thức thanh toán (Cash, Card, Transfer)
    """
    client = _create_client(access_token, retailer)

    body: Dict[str, Any] = {
        "branchId": branch_id,
        "purchaseDate": purchase_date,
        "orderDetails": order_details,
    }
    if customer_id:
        body["customer"] = {"id": customer_id}
    if description:
        body["description"] = description
    if total_payment is not None:
        body["totalPayment"] = total_payment
    if discount is not None:
        body["discount"] = discount
    if method:
        body["method"] = method

    return client.post("/orders", body)


# ============================================================================
# Invoice Tools / Công cụ Hóa đơn
# ============================================================================

@mcp.tool
def kv_list_invoices(
    access_token: str,
    retailer: str,
    branch_ids: Optional[List[int]] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    from_purchase_date: Optional[str] = None,
    to_purchase_date: Optional[str] = None,
    customer_ids: Optional[List[int]] = None,
    page_size: int = 50,
    current_item: int = 0,
    include_payment: bool = False,
) -> Dict[str, Any]:
    """
    Get list of sales invoices within a time period.
    Lấy danh sách hóa đơn bán hàng trong khoảng thời gian.
    Used for use cases: revenue summary, daily analysis, customer analysis, etc.
    Dùng cho các use case: tổng hợp doanh thu, phân tích theo ngày, theo khách,...
    
    Args:
        access_token: OAuth2 access token (provided by Culi) / Token OAuth2 (do Culi cung cấp)
        retailer: KiotViet retailer name / Tên gian hàng KiotViet
        branch_ids: Filter by list of branch IDs / Lọc theo danh sách ID chi nhánh
        from_date: From update date (format: YYYY-MM-DD) / Từ ngày cập nhật (format: YYYY-MM-DD)
        to_date: To update date (format: YYYY-MM-DD) / Đến ngày cập nhật (format: YYYY-MM-DD)
        from_purchase_date: From transaction date (format: YYYY-MM-DD) / Từ ngày giao dịch (format: YYYY-MM-DD)
        to_purchase_date: To transaction date (format: YYYY-MM-DD) / Đến ngày giao dịch (format: YYYY-MM-DD)
        customer_ids: Filter by list of customer IDs / Lọc theo danh sách ID khách hàng
        page_size: Number of items per page (default 50, max 100) / Số items trong 1 trang (mặc định 50, tối đa 100)
        current_item: Get data from current record (default 0) / Lấy dữ liệu từ bản ghi hiện tại (mặc định 0)
        include_payment: Whether to include payment information / Có lấy thông tin thanh toán hay không
    """
    client = _create_client(access_token, retailer)
    params: Dict[str, Any] = {
        "pageSize": min(page_size, 100),
        "currentItem": current_item,
        "includePayment": include_payment,
    }
    if branch_ids:
        params["branchIds"] = branch_ids
    if from_date:
        params["fromDate"] = from_date
    if to_date:
        params["toDate"] = to_date
    if from_purchase_date:
        params["fromPurchaseDate"] = from_purchase_date
    if to_purchase_date:
        params["toPurchaseDate"] = to_purchase_date
    if customer_ids:
        params["customerIds"] = customer_ids

    return client.get("/invoices", params)


@mcp.tool
def kv_get_invoice(
    access_token: str,
    retailer: str,
    invoice_id: Optional[int] = None,
    invoice_code: Optional[str] = None,
    include_payment: bool = False,
) -> Dict[str, Any]:
    """
    Get detailed information of an invoice by ID or invoice code.
    Lấy thông tin chi tiết của một hóa đơn theo ID hoặc mã hóa đơn.
    
    Args:
        access_token: OAuth2 access token (provided by Culi) / Token OAuth2 (do Culi cung cấp)
        retailer: KiotViet retailer name / Tên gian hàng KiotViet
        invoice_id: Invoice ID / ID hóa đơn
        invoice_code: Invoice code (if invoice_id is not provided) / Mã hóa đơn (nếu không có invoice_id)
        include_payment: Whether to include payment information / Có lấy thông tin thanh toán hay không
    """
    client = _create_client(access_token, retailer)
    params = {"includePayment": include_payment} if include_payment else None
    
    if invoice_id:
        return client.get(f"/invoices/{invoice_id}", params)
    elif invoice_code:
        return client.get(f"/invoices/code/{invoice_code}", params)
    else:
        raise ValueError("Need to provide invoice_id or invoice_code / Cần cung cấp invoice_id hoặc invoice_code")


# ============================================================================
# Category Tools / Công cụ Nhóm hàng
# ============================================================================

@mcp.tool
def kv_list_categories(
    access_token: str,
    retailer: str,
    hierarchical_data: bool = True,
    page_size: int = 100,
    current_item: int = 0,
) -> Dict[str, Any]:
    """
    Get list of product categories.
    Lấy danh sách nhóm hàng hóa (categories).
    
    Args:
        access_token: OAuth2 access token (provided by Culi) / Token OAuth2 (do Culi cung cấp)
        retailer: KiotViet retailer name / Tên gian hàng KiotViet
        hierarchical_data: If True, returns hierarchical data (with children) / Nếu True, trả về dữ liệu phân cấp (có children)
        page_size: Number of items per page (default 100) / Số items trong 1 trang (mặc định 100)
        current_item: Get data from current record (default 0) / Lấy dữ liệu từ bản ghi hiện tại (mặc định 0)
    """
    client = _create_client(access_token, retailer)
    params: Dict[str, Any] = {
        "pageSize": min(page_size, 100),
        "currentItem": current_item,
        "hierachicalData": hierarchical_data,  # Note: API uses "hierachicalData" (typo in API) / Lưu ý: API dùng "hierachicalData" (lỗi chính tả trong API)
    }
    return client.get("/categories", params)


# ============================================================================
# Branch Tools / Công cụ Chi nhánh
# ============================================================================

@mcp.tool
def kv_list_branches(
    access_token: str,
    retailer: str,
) -> Dict[str, Any]:
    """
    Get list of store branches.
    Lấy danh sách chi nhánh của cửa hàng.
    Used to get branch_id when creating orders or filtering data.
    Dùng để lấy branch_id khi tạo đơn hàng hoặc lọc dữ liệu.
    
    Args:
        access_token: OAuth2 access token (provided by Culi) / Token OAuth2 (do Culi cung cấp)
        retailer: KiotViet retailer name / Tên gian hàng KiotViet
    """
    client = _create_client(access_token, retailer)
    return client.get("/branches")


# ============================================================================
# Resources / Tài nguyên
# ============================================================================

@mcp.resource("kiotviet://products_schema")
def kv_products_schema():
    """
    Simple description of /products schema for LLM to understand.
    Mô tả đơn giản schema /products để LLM hiểu.
    """
    return {
        "endpoint": "/products",
        "fields": [
            "id", "code", "name", "categoryName",
            "basePrice", "inventories[].branchName", "inventories[].onHand",
        ],
        "notes": "Used for inventory consultation, selling price, product analysis. / Dùng để tư vấn tồn kho, giá bán, phân tích hàng hóa."
    }


@mcp.resource("kiotviet://customers_schema")
def kv_customers_schema():
    """
    Description of /customers schema for LLM to understand.
    Mô tả schema /customers để LLM hiểu.
    """
    return {
        "endpoint": "/customers",
        "fields": [
            "id", "code", "name", "contactNumber", "email",
            "address", "debt", "totalInvoiced", "totalPoint", "totalRevenue"
        ],
        "notes": "Used to search customers, view purchase history, debts. / Dùng để tìm kiếm khách hàng, xem lịch sử mua hàng, nợ."
    }


@mcp.resource("kiotviet://orders_schema")
def kv_orders_schema():
    """
    Description of /orders schema for LLM to understand.
    Mô tả schema /orders để LLM hiểu.
    """
    return {
        "endpoint": "/orders",
        "fields": [
            "id", "code", "purchaseDate", "branchName",
            "customerName", "total", "totalPayment", "status", "statusValue"
        ],
        "notes": "Used to view orders, create new orders. / Dùng để xem đơn đặt hàng, tạo đơn hàng mới."
    }


@mcp.resource("kiotviet://invoices_schema")
def kv_invoices_schema():
    """
    Description of /invoices schema for LLM to understand.
    Mô tả schema /invoices để LLM hiểu.
    """
    return {
        "endpoint": "/invoices",
        "fields": [
            "id", "code", "purchaseDate", "branchName",
            "customerName", "total", "totalPayment", "status"
        ],
        "notes": "Used to view sales invoices, revenue summary. / Dùng để xem hóa đơn bán hàng, tổng hợp doanh thu."
    }


# ============================================================================
# Prompts / Lời nhắc
# ============================================================================

@mcp.prompt
def kiotviet_assistant_prompt() -> PromptMessage:
    text = """
Bạn là trợ lý kế toán/kho cho hộ kinh doanh, đang làm việc với dữ liệu từ phần mềm KiotViet qua MCP.

Nguyên tắc:
- Chỉ xem và thao tác trên dữ liệu bằng cách gọi các tool kiotviet-* (kv_*).
- Không bịa dữ liệu. Nếu cần thêm thông tin (chi nhánh, ngày, khách hàng) hãy hỏi lại user.
- Khi user muốn tra cứu hàng hóa, hãy dùng kv_list_products hoặc kv_get_product.
- Khi user muốn tìm khách hàng, hãy dùng kv_search_customers hoặc kv_get_customer.
- Khi user muốn xem/hoặc lập đơn hàng, hãy dùng kv_list_orders, kv_get_order hoặc kv_create_order.
- Khi user muốn xem hóa đơn bán hàng, hãy dùng kv_list_invoices hoặc kv_get_invoice.
- Khi cần lấy danh sách chi nhánh, hãy dùng kv_list_branches.
- Khi cần lấy danh sách nhóm hàng, hãy dùng kv_list_categories.

BẢO MẬT:
- Tất cả tools yêu cầu access_token và retailer (do hệ thống cung cấp).
- KHÔNG BAO GIỜ hỏi user về client_id, client_secret hay access_token.
- access_token và retailer được cung cấp tự động bởi hệ thống cho mỗi phiên chat.
"""
    return PromptMessage(role="system", content=TextContent(type="text", text=text))


# ============================================================================
# Main entry point / Điểm vào chính
# ============================================================================

if __name__ == "__main__":
    mcp.run()
