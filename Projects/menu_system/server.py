# server.py
# Run: python server.py
# Open: http://localhost:8080

import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

import menu_logic as logic

PORT = 8080


def send_json(handler, data):
    body = json.dumps(data).encode()
    handler.send_response(200)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", str(len(body)))
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.end_headers()
    handler.wfile.write(body)


def send_file(handler, filepath):
    f    = open(filepath, "rb")
    body = f.read()
    f.close()
    handler.send_response(200)
    handler.send_header("Content-Type", "text/html")
    handler.end_headers()
    handler.wfile.write(body)


def read_body(handler):
    length = handler.headers.get("Content-Length")
    if length:
        return json.loads(handler.rfile.read(int(length)))
    return {}


class Handler(BaseHTTPRequestHandler):

    def log_message(self, fmt, *args):
        print(fmt % args)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        path = urlparse(self.path).path

        if path == "/" or path == "/index.html":
            folder = os.path.dirname(os.path.abspath(__file__))
            send_file(self, os.path.join(folder, "index.html"))

        elif path == "/api/menu":
            send_json(self, {"ok": True, "menu": logic.menu})

        elif path == "/api/cart":
            send_json(self, {"ok": True, "cart": logic.get_cart()})

        else:
            send_json(self, {"ok": False, "error": "Not found"})

    def do_POST(self):
        path = urlparse(self.path).path
        body = read_body(self)

        if path == "/api/cart/add":
            logic.add_to_cart(int(body["item_id"]))
            send_json(self, {"ok": True, "cart": logic.get_cart()})

        elif path == "/api/cart/update":
            logic.update_qty(int(body["item_id"]), int(body["qty"]))
            send_json(self, {"ok": True, "cart": logic.get_cart()})

        elif path == "/api/cart/remove":
            logic.remove_from_cart(int(body["item_id"]))
            send_json(self, {"ok": True, "cart": logic.get_cart()})

        elif path == "/api/cart/clear":
            logic.clear_cart()
            send_json(self, {"ok": True, "cart": logic.get_cart()})

        elif path == "/api/order":
            result = logic.place_order()
            if result is None:
                send_json(self, {"ok": False, "error": "Cart is empty"})
            else:
                send_json(self, {"ok": True, "order": result})

        else:
            send_json(self, {"ok": False, "error": "Not found"})


if __name__ == "__main__":
    server = HTTPServer(("", PORT), Handler)
    print("Running at http://localhost:" + str(PORT))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Stopped.")
