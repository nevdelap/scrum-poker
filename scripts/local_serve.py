#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# ///

import http.server
import os
import socket
import webbrowser
from pathlib import Path

PORT = 8766
DIR = Path(__file__).parent.parent

os.chdir(DIR)

class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        print(f"{self.address_string()} - {format % args}")

class ReuseAddrServer(http.server.HTTPServer):
    allow_reuse_address = True

def lan_ip():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except OSError:
        return None

local_url = f"http://localhost:{PORT}"
ip = lan_ip()
lan_url   = f"http://{ip}:{PORT}" if ip else None
print(f"Serving Scrum Poker")
print(f"  Local:  {local_url}")
if lan_url:
    print(f"  Mobile: {lan_url}")
print("Press Ctrl+C to stop.")

webbrowser.open(lan_url or local_url)

try:
    with ReuseAddrServer(("0.0.0.0", PORT), Handler) as httpd:
        httpd.serve_forever()
except KeyboardInterrupt:
    pass
