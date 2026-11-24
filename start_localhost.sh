#!/bin/bash
# Script khởi chạy Hệ thống AI Agent Xử lý Cơ hội Bán hàng B2B - Minh An Company

PORT=${PORT:-8888}

# Tự động giải phóng cổng nếu đang có tiến trình cũ chiếm dụng
PID=$(lsof -ti :${PORT} 2>/dev/null)
if [ -n "$PID" ]; then
    echo "⚠️ Đang giải phóng cổng ${PORT} từ tiến trình cũ (PID: $PID)..."
    kill -9 $PID 2>/dev/null || PORT=8889
fi
echo "=========================================================================="
echo "  🚀 AI301: HỆ THỐNG AI AGENT XỬ LÝ CƠ HỘI BÁN HÀNG B2B - MINH AN COMPANY"
echo "  🌸 Thiết kế theo phong cách DataLens Studio · Lê Yến Như (Nền Vàng Pastel)"
echo "=========================================================================="
echo "👉 Truy cập Web tại: http://localhost:${PORT}"
echo ""

# Ưu tiên các lệnh Python khả dụng trên hệ thống
if command -v python3 >/dev/null 2>&1; then
    echo "▶️ Đang khởi chạy với Python 3..."
    PORT=${PORT} python3 server.py
elif command -v python >/dev/null 2>&1; then
    echo "▶️ Đang khởi chạy với Python..."
    PORT=${PORT} python server.py
elif command -v py >/dev/null 2>&1; then
    echo "▶️ Đang khởi chạy với Python Launcher..."
    PORT=${PORT} py server.py
else
    echo "❌ Không tìm thấy Python! Vui lòng cài đặt Python 3.8+ để khởi chạy hệ thống."
    exit 1
fi
