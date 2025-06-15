#!/usr/bin/env python3
"""
Simple HTTP server for the onset detection web interface
"""

import http.server
import socketserver
import os
import sys

PORT = 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers to allow loading local files
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def main():
    # Change to the onset-detection directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    Handler = MyHTTPRequestHandler
    
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print(f"Server running at http://localhost:{PORT}/")
            print(f"Open http://localhost:{PORT}/index.html in your browser")
            print("Press Ctrl-C to stop the server")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        sys.exit(0)
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"Port {PORT} is already in use. Try closing other servers or use a different port.")
        else:
            raise

if __name__ == "__main__":
    main()
