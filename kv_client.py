"""
KiotViet API client - Stateless implementation.
Receives access_token and retailer from Culi, no session management.

Client API KiotViet - Triển khai Stateless.
Nhận access_token và retailer từ Culi, không quản lý phiên.
"""
import httpx
from typing import Any, Dict, Optional


BASE_URL = "https://public.kiotapi.com"


class KiotVietClient:
    """
    Stateless HTTP client for KiotViet Public API.
    Client HTTP Stateless cho KiotViet Public API.
    Receives access_token and retailer from caller (Culi).
    Nhận access_token và retailer từ người gọi (Culi).
    No token management, no session state.
    Không quản lý token, không có trạng thái phiên.
    """
    
    def __init__(self, access_token: str, retailer: str):
        """
        Initialize client with access_token and retailer.
        Khởi tạo client với access_token và retailer.
        
        Args:
            access_token: OAuth2 access token (obtained by Culi) / Token OAuth2 (do Culi cung cấp)
            retailer: Retailer name (tên gian hàng)
        """
        self.access_token = access_token
        self.retailer = retailer
        self._client: Optional[httpx.Client] = None

    def _headers(self) -> Dict[str, str]:
        """Get headers with authentication for API requests. / Lấy headers với xác thực cho các request API."""
        return {
            "Retailer": self.retailer,
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

    def _get_client(self) -> httpx.Client:
        """Get or create HTTP client. / Lấy hoặc tạo HTTP client."""
        if self._client is None:
            self._client = httpx.Client(timeout=30.0)
        return self._client

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """Make a GET request to the KiotViet API. / Thực hiện GET request đến KiotViet API."""
        url = f"{BASE_URL}{path}"
        client = self._get_client()
        resp = client.get(url, headers=self._headers(), params=params)
        resp.raise_for_status()
        return resp.json()

    def post(self, path: str, json_body: Dict[str, Any]) -> Any:
        """Make a POST request to the KiotViet API. / Thực hiện POST request đến KiotViet API."""
        url = f"{BASE_URL}{path}"
        client = self._get_client()
        resp = client.post(url, headers=self._headers(), json=json_body)
        resp.raise_for_status()
        return resp.json()

    def put(self, path: str, json_body: Dict[str, Any]) -> Any:
        """Make a PUT request to the KiotViet API. / Thực hiện PUT request đến KiotViet API."""
        url = f"{BASE_URL}{path}"
        client = self._get_client()
        resp = client.put(url, headers=self._headers(), json=json_body)
        resp.raise_for_status()
        return resp.json()

    def delete(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """Make a DELETE request to the KiotViet API. / Thực hiện DELETE request đến KiotViet API."""
        url = f"{BASE_URL}{path}"
        client = self._get_client()
        resp = client.delete(url, headers=self._headers(), params=params)
        resp.raise_for_status()
        return resp.json() if resp.text else {"message": "success"}

    def close(self) -> None:
        """Close the HTTP client. / Đóng HTTP client."""
        if self._client is not None:
            self._client.close()
            self._client = None
