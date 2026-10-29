import os
import socket
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class H(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            body, code, ctype = b'{"ok":true}', 200, "application/json"
        elif self.path == "/":
            body, code, ctype = (
                f"<h1>instinct-smoke works</h1><p>host: {socket.gethostname()}</p>"
            ).encode(), 200, "text/html; charset=utf-8"
        else:
            body, code, ctype = b"not found", 404, "text/plain"
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    # ponytail: threaded stdlib server is plenty for a smoke test
    print(f"listening on :{port}", flush=True)
    ThreadingHTTPServer(("0.0.0.0", port), H).serve_forever()
