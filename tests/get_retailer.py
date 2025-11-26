"""
Script để lấy retailer từ KiotViet API.
Retailer thường là tên gian hàng đã đăng ký.
"""
import httpx
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load environment variables (from parent directory)
env_path = Path(__file__).parent.parent / "promts" / "auths.env"
load_dotenv(env_path)

TOKEN_URL = "https://id.kiotviet.vn/connect/token"
BASE_URL = "https://public.kiotapi.com"

def get_access_token() -> str:
    """Lấy access_token."""
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    
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


def get_retailer_from_api(access_token: str, retailer_guess: str = None) -> str:
    """
    Thử lấy retailer từ API.
    Nếu không được, trả về retailer_guess hoặc yêu cầu user cung cấp.
    """
    # Thử với retailer_guess nếu có
    if retailer_guess:
        try:
            headers = {
                "Retailer": retailer_guess,
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            }
            resp = httpx.get(f"{BASE_URL}/branches", headers=headers, timeout=10)
            if resp.status_code == 200:
                print(f"✅ Retailer '{retailer_guess}' hợp lệ!")
                return retailer_guess
        except:
            pass
    
    # Nếu không có retailer_guess, cần user cung cấp
    print("⚠️  Không thể tự động lấy retailer từ API.")
    print("   Retailer là tên gian hàng bạn đã đăng ký với KiotViet.")
    print("   Ví dụ: taphoaxyz, cuahang123, ...")
    return None


if __name__ == "__main__":
    print("🔄 Đang lấy access_token...")
    access_token = get_access_token()
    print("✅ Lấy access_token thành công!\n")
    
    # Thử lấy retailer từ env hoặc command line
    retailer = os.getenv("RETAILER")
    
    if retailer:
        print(f"📝 Sử dụng retailer từ env: {retailer}")
        valid = get_retailer_from_api(access_token, retailer)
        if valid:
            print(f"\n✅ Retailer hợp lệ: {retailer}")
            print(f"\n💡 Để test MCP server, chạy:")
            print(f"   python test_mcp_simple.py {retailer}")
        else:
            print(f"\n❌ Retailer '{retailer}' không hợp lệ hoặc không có quyền truy cập.")
    else:
        print("❌ Chưa có retailer. Vui lòng:")
        print("   1. Set RETAILER environment variable, hoặc")
        print("   2. Truyền retailer khi chạy test:")
        print("      python test_mcp_simple.py <retailer>")
        print("\n   Retailer là tên gian hàng bạn đã đăng ký với KiotViet.")

