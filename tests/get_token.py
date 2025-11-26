"""
Script để lấy access_token từ KiotViet OAuth2.
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

def get_access_token(client_id: str, client_secret: str) -> dict:
    """
    Lấy access_token từ KiotViet OAuth2.
    
    Args:
        client_id: Client ID từ KiotViet
        client_secret: Client Secret từ KiotViet
    
    Returns:
        dict: Chứa access_token, expires_in, token_type
    """
    data = {
        "scopes": "PublicApi.Access",
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    
    try:
        resp = httpx.post(TOKEN_URL, data=data, headers=headers, timeout=15)
        resp.raise_for_status()
        return resp.json()
    except httpx.HTTPStatusError as e:
        raise Exception(f"Failed to get access token: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        raise Exception(f"Error requesting token: {str(e)}")


if __name__ == "__main__":
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    
    if not client_id or not client_secret:
        print("❌ Error: CLIENT_ID or CLIENT_SECRET not found in auths.env")
        exit(1)
    
    print("🔄 Đang lấy access_token từ KiotViet...")
    try:
        result = get_access_token(client_id, client_secret)
        print("✅ Lấy access_token thành công!")
        print(f"Access Token: {result['access_token'][:50]}...")
        print(f"Expires in: {result['expires_in']} seconds")
        print(f"Token Type: {result['token_type']}")
        
        # Lưu vào file để test (trong tests folder)
        token_file = Path(__file__).parent / "token.txt"
        with open(token_file, "w") as f:
            f.write(result['access_token'])
        print(f"\n💾 Token đã được lưu vào {token_file}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        exit(1)

