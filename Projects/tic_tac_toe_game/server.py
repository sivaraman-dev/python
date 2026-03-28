import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from logic import TicTacToeLogic

# Initialize game logic
game = TicTacToeLogic()

class TicTacToeServer(BaseHTTPRequestHandler):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    def do_GET(self):
        # Handle API get requests
        if self.path == '/api/state':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(game.get_state()).encode('utf-8'))
            return
            
        # Handle static files
        if self.path == '/':
            filepath = os.path.join(self.BASE_DIR, 'index.html')
            content_type = 'text/html'
        elif self.path == '/style.css':
            filepath = os.path.join(self.BASE_DIR, 'style.css')
            content_type = 'text/css'
        elif self.path == '/script.js':
            filepath = os.path.join(self.BASE_DIR, 'script.js')
            content_type = 'application/javascript'
        else:
            self.send_error(404, "File Not Found")
            return

        try:
            with open(filepath, 'rb') as file:
                self.send_response(200)
                self.send_header('Content-Type', content_type)
                self.end_headers()
                self.wfile.write(file.read())
        except FileNotFoundError:
            self.send_error(404, f"File {self.path} Not Found")

    def do_POST(self):
        if self.path == '/api/move':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            index = data.get('index')
            if index is not None:
                game.make_move(int(index))
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(game.get_state()).encode('utf-8'))
            return
            
        elif self.path == '/api/reset':
            game.reset()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(game.get_state()).encode('utf-8'))
            return

def run(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, TicTacToeServer)
    print(f"Starting Tic-Tac-Toe server on port {port}...")
    print(f"Open http://localhost:{port}/ in your web browser.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
    httpd.server_close()

if __name__ == '__main__':
    run()
