#!/bin/bash
# Script để khởi chạy MCP server

cd "$(dirname "$0")"
source venv/bin/activate
python kiotviet_mcp_server.py

