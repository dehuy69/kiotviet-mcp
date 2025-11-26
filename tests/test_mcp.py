"""
Script để test MCP server với access_token.
Cần cung cấp retailer (tên gian hàng).

Usage:
    python test_mcp.py <retailer>              # Test cơ bản (3 tools)
    python test_mcp.py <retailer> --full       # Test đầy đủ (5 tools)
    export RETAILER=your_retailer && python test_mcp.py  # Dùng env variable
"""
import httpx
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from kiotviet_mcp_server import (
    kv_list_products,
    kv_list_branches,
    kv_search_customers,
    kv_list_orders,
    kv_list_invoices,
)

# Load environment variables (from parent directory)
env_path = Path(__file__).parent.parent / "promts" / "auths.env"
load_dotenv(env_path)

TOKEN_URL = "https://id.kiotviet.vn/connect/token"

def get_access_token() -> str:
    """Lấy access_token từ KiotViet."""
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    
    if not client_id or not client_secret:
        raise Exception("CLIENT_ID or CLIENT_SECRET not found in auths.env")
    
    data = {
        "scopes": "PublicApi.Access",
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    
    resp = httpx.post(TOKEN_URL, data=data, headers=headers, timeout=15)
    resp.raise_for_status()
    return resp.json()["access_token"]


def test_tools(retailer: str, full: bool = False):
    """Test các tools của MCP server."""
    print(f"🔄 Đang lấy access_token...")
    try:
        access_token = get_access_token()
        print(f"✅ Lấy access_token thành công!")
        print(f"Retailer: {retailer}")
        print(f"Token: {access_token[:50]}...\n")
    except Exception as e:
        print(f"❌ Error getting token: {e}")
        return
    
    print("=" * 60)
    print("TESTING MCP SERVER TOOLS")
    print("=" * 60)
    
    # Test 1: List branches
    print("\n1️⃣ Testing kv_list_branches...")
    try:
        result = kv_list_branches(access_token=access_token, retailer=retailer)
        branches = result.get('data', [])
        print(f"✅ Success! Found {len(branches)} branches")
        if branches:
            print(f"   First branch: {branches[0].get('name', 'N/A')} (ID: {branches[0].get('id', 'N/A')})")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 2: List products
    print("\n2️⃣ Testing kv_list_products...")
    try:
        result = kv_list_products(
            access_token=access_token,
            retailer=retailer,
            page_size=5
        )
        total = result.get('total', 0)
        data = result.get('data', [])
        print(f"✅ Success! Total products: {total}")
        if data:
            print(f"   First product: {data[0].get('name', 'N/A')} (Code: {data[0].get('code', 'N/A')})")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 3: Search customers
    print("\n3️⃣ Testing kv_search_customers...")
    try:
        result = kv_search_customers(
            access_token=access_token,
            retailer=retailer,
            page_size=5
        )
        total = result.get('total', 0)
        data = result.get('data', [])
        print(f"✅ Success! Total customers: {total}")
        if data:
            print(f"   First customer: {data[0].get('name', 'N/A')} (Code: {data[0].get('code', 'N/A')})")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 4 & 5: Chỉ test khi --full
    if full:
        # Test 4: List orders
        print("\n4️⃣ Testing kv_list_orders...")
        try:
            result = kv_list_orders(
                access_token=access_token,
                retailer=retailer,
                page_size=5
            )
            total = result.get('total', 0)
            print(f"✅ Success! Total orders: {total}")
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
        
        # Test 5: List invoices
        print("\n5️⃣ Testing kv_list_invoices...")
        try:
            result = kv_list_invoices(
                access_token=access_token,
                retailer=retailer,
                page_size=5
            )
            total = result.get('total', 0)
            print(f"✅ Success! Total invoices: {total}")
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("✅ Testing completed!")
    print("=" * 60)


if __name__ == "__main__":
    # Parse arguments
    args = sys.argv[1:]
    full = "--full" in args or "-f" in args
    
    # Remove flags from args
    args = [a for a in args if a not in ["--full", "-f"]]
    
    # Get retailer from command line or env
    retailer = args[0] if args else os.getenv("RETAILER")
    
    if not retailer:
        print("❌ Error: Retailer (tên gian hàng) chưa được cung cấp!")
        print("Usage: python test_mcp.py <retailer> [--full]")
        print("   hoặc set RETAILER environment variable")
        print("\nVí dụ:")
        print("   python test_mcp.py nhathuoctestmcp          # Test cơ bản")
        print("   python test_mcp.py nhathuoctestmcp --full   # Test đầy đủ")
        sys.exit(1)
    
    test_tools(retailer, full=full)
