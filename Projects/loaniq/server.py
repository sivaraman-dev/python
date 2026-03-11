"""
server.py — Pure Python web server (no frameworks, no pip install needed)
Uses only Python built-in modules: http.server, json, urllib
Run: python server.py
Open: http://localhost:5000
"""

import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from loan_logic import check_loan_eligibility

PORT = 5000
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ── MIME types for static files ───────────────────────────────────
MIME_TYPES = {
    '.html': 'text/html',
    '.css':  'text/css',
    '.js':   'application/javascript',
    '.ico':  'image/x-icon',
}


class LoanHandler(BaseHTTPRequestHandler):

    # ── Silence default request logs (optional: comment out to see logs) ──
    def log_message(self, format, *args):
        print(f"  → {self.command} {self.path}")

    # ── Handle GET: serve static files ───────────────────────────
    def do_GET(self):
        # Map "/" to index.html
        path = '/index.html' if self.path == '/' else self.path

        # Strip query strings
        path = path.split('?')[0]

        filepath = os.path.join(BASE_DIR, path.lstrip('/'))

        if os.path.isfile(filepath):
            ext = os.path.splitext(filepath)[1]
            mime = MIME_TYPES.get(ext, 'text/plain')
            with open(filepath, 'rb') as f:
                content = f.read()
            self._send(200, mime, content)
        else:
            self._send(404, 'text/plain', b'404 Not Found')

    # ── Handle POST: run Python eligibility logic ─────────────────
    def do_POST(self):
        if self.path == '/check':
            length = int(self.headers.get('Content-Length', 0))
            body   = self.rfile.read(length)

            try:
                data = json.loads(body)

                age          = int(data.get('age', 0))
                income       = int(data.get('income', 0))
                credit_score = int(data.get('credit_score', 0))
                loan_amount  = int(data.get('loan_amount', 0))
                employment   = str(data.get('employment', '')).strip().lower()

                if not employment:
                    raise ValueError("Employment is required")

                result = check_loan_eligibility(
                    age, income, credit_score, loan_amount, employment
                )
                response = json.dumps(result).encode()
                self._send(200, 'application/json', response)

            except (ValueError, KeyError) as e:
                err = json.dumps({'error': str(e)}).encode()
                self._send(400, 'application/json', err)
        else:
            self._send(404, 'text/plain', b'Not Found')

    # ── Helper: send HTTP response ────────────────────────────────
    def _send(self, code, content_type, body):
        self.send_response(code)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(body)


# ── Start server ──────────────────────────────────────────────────
if __name__ == '__main__':
    server = HTTPServer(('localhost', PORT), LoanHandler)
    print("\n╔══════════════════════════════════════╗")
    print("║     LoanIQ — Pure Python Server      ║")
    print("╠══════════════════════════════════════╣")
    print(f"║  Open: http://localhost:{PORT}          ║")
    print("║  Stop: Ctrl + C                       ║")
    print("╚══════════════════════════════════════╝\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Server stopped.")
        server.server_close()
