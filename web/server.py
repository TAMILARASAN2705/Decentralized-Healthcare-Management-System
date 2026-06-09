#!/usr/bin/env python3
import http.server
import socketserver
import os

# Change to the web directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Create server
PORT = 8080
Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Healthcare Management System Web Server")
    print(f"Running at: http://localhost:{PORT}")
    print("Press Ctrl+C to stop the server")
    httpd.serve_forever()
