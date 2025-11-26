"""
Example usage of kiotviet-mcp server.
This demonstrates how to register an account and use the tools.
"""
from kiotviet_mcp_server import (
    kv_register_account,
    kv_list_products,
    kv_search_customers,
    kv_list_branches,
    kv_list_orders,
    kv_list_invoices,
)


def example_register_and_use():
    """Example: Register account and use tools."""
    
    # Step 1: Register a KiotViet account
    # This should be done by culi-backend, not by LLM
    print("Registering account...")
    result = kv_register_account(
        account_id="example_user_123",
        retailer="your_retailer_name",
        client_id="your_client_id",
        client_secret="your_client_secret"
    )
    print(f"Registration result: {result}")
    
    account_id = "example_user_123"
    
    # Step 2: List branches
    print("\nFetching branches...")
    branches = kv_list_branches(account_id=account_id)
    print(f"Branches: {branches}")
    
    # Step 3: Search for products
    print("\nSearching products...")
    products = kv_list_products(
        account_id=account_id,
        name="áo",
        page_size=10
    )
    print(f"Found {products.get('total', 0)} products")
    
    # Step 4: Search for customers
    print("\nSearching customers...")
    customers = kv_search_customers(
        account_id=account_id,
        contact_number="0123456789",
        page_size=10
    )
    print(f"Found {customers.get('total', 0)} customers")
    
    # Step 5: List orders
    print("\nFetching orders...")
    orders = kv_list_orders(
        account_id=account_id,
        page_size=10
    )
    print(f"Found {orders.get('total', 0)} orders")
    
    # Step 6: List invoices
    print("\nFetching invoices...")
    invoices = kv_list_invoices(
        account_id=account_id,
        from_date="2024-01-01",
        to_date="2024-12-31",
        page_size=10
    )
    print(f"Found {invoices.get('total', 0)} invoices")


if __name__ == "__main__":
    # Note: Replace with your actual KiotViet credentials
    print("This is an example script.")
    print("Please update the credentials in the code before running.")
    print("\nTo use this example:")
    print("1. Get your KiotViet API credentials (retailer, client_id, client_secret)")
    print("2. Update the values in example_register_and_use()")
    print("3. Run: python example_usage.py")
    
    # Uncomment to run:
    # example_register_and_use()

