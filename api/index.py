import sys
import urllib.parse
from pathlib import Path

# Đảm bảo thư mục gốc dự án nằm trong sys.path khi chạy trên Vercel Serverless
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from server import B2BAgentHttpHandler


class handler(B2BAgentHttpHandler):
    """Vercel Python Serverless entrypoint kế thừa toàn bộ API từ B2BAgentHttpHandler."""

    def _restore_api_path(self):
        parsed = urllib.parse.urlparse(self.path)

        # 1. Ưu tiên header X-Api-Path do frontend app.js đính kèm (miễn nhiễm với mọi rewrite của Vercel)
        header_api_path = (self.headers.get("X-Api-Path") or "").strip()
        if header_api_path.startswith("/api/"):
            qs = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)
            qs.pop("__api_path", None)
            new_query = urllib.parse.urlencode(qs, doseq=True)
            self.path = f"{header_api_path}?{new_query}" if new_query else header_api_path
            return

        # 2. Khôi phục từ query param __api_path của vercel.json (:path*)
        qs = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)
        api_subpath = qs.pop("__api_path", [None])[0]
        if api_subpath and not api_subpath.startswith("$"):
            clean_sub = api_subpath.lstrip("/")
            new_path = f"/api/{clean_sub}" if clean_sub else "/api"
            new_query = urllib.parse.urlencode(qs, doseq=True)
            self.path = f"{new_path}?{new_query}" if new_query else new_path
            return

        # 3. Fallback qua các header gốc của Vercel nếu có
        if parsed.path in ("/api/index.py", "/index.py", "/api", "/"):
            orig_path = (
                self.headers.get("x-vercel-original-path")
                or self.headers.get("x-invoke-path")
                or self.headers.get("x-matched-path")
            )
            if orig_path and orig_path.startswith("/api/") and orig_path != "/api/index.py":
                self.path = f"{orig_path}?{parsed.query}" if parsed.query else orig_path

    def do_GET(self):
        self._restore_api_path()
        return super().do_GET()

    def do_POST(self):
        self._restore_api_path()
        return super().do_POST()
