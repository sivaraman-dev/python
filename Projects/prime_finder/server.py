from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json

from prime_logic import find_primes


class PrimeHandler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        return

    def send_json(self, data, status=200):
        body = json.dumps(data).encode()

        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()

        self.wfile.write(body)

    def serve_index(self):
        try:
            with open("index.html", "rb") as f:
                html = f.read()

            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(html)

        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):

        # Serve website
        if self.path == "/" or self.path == "/index.html":
            self.serve_index()
            return

        # API
        if self.path.startswith("/api/primes"):
            self.handle_prime_api()
            return

        self.send_response(404)
        self.end_headers()

    def handle_prime_api(self):
        try:
            query = parse_qs(urlparse(self.path).query)

            start = int(query.get("start", ["1"])[0])
            end = int(query.get("end", ["100"])[0])

            if start < 1 or end > 1000 or start > end:
                raise ValueError("start ≥1, end ≤1000, start ≤ end")

            primes, steps = find_primes(start, end)

            response = {
                "start": start,
                "end": end,
                "primes": primes,
                "count": len(primes),
                "steps": steps
            }

            self.send_json(response)

        except Exception as e:
            self.send_json({"error": str(e)}, 400)


def run_server(port=8001):
    server = HTTPServer(("localhost", port), PrimeHandler)

    print(f"✅ Server running at http://localhost:{port}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")


if __name__ == "__main__":
    run_server()