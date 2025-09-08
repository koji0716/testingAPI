import os, json, urllib.request, urllib.parse
from http.server import BaseHTTPRequestHandler


def _cors_headers():
    origin = os.environ.get("ALLOWED_ORIGIN", "*")
    return {
        "Access-Control-Allow-Origin": origin,
        "Access-Control-Allow-Methods": "GET, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
        "Cache-Control": "no-store",
        "Content-Type": "application/json"
    }


class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        headers = _cors_headers()
        self.send_response(204)
        for k, v in headers.items():
            self.send_header(k, v)
        self.end_headers()

    def do_GET(self):
        headers = _cors_headers()
        key = os.environ.get("NEWS_API_KEY")
        if not key:
            body = json.dumps({"error": "NEWS_API_KEY is not set"})
            self.send_response(500)
            for k, v in headers.items():
                self.send_header(k, v)
            self.end_headers()
            self.wfile.write(body.encode("utf-8"))
            return

        # クエリ q を受け取り既定は "vercel"
        parsed = urllib.parse.urlparse(self.path)
        qs = urllib.parse.parse_qs(parsed.query)
        q = qs.get("q", ["vercel"])[0]

        url = "https://newsapi.org/v2/everything?" + urllib.parse.urlencode({
            "q": q,
            "pageSize": 10,
            "language": "ja"
        })
        req = urllib.request.Request(url, headers={"X-Api-Key": key})
        try:
            with urllib.request.urlopen(req, timeout=10) as r:
                upstream_body = r.read()
                status = r.getcode()
                # Content-TypeはJSONに固定（NewsAPIはJSON）
                self.send_response(status)
                for k, v in headers.items():
                    self.send_header(k, v)
                self.end_headers()
                self.wfile.write(upstream_body)
        except Exception as e:
            body = json.dumps({"error": str(e)})
            self.send_response(502)
            for k, v in headers.items():
                self.send_header(k, v)
            self.end_headers()
            self.wfile.write(body.encode("utf-8"))
