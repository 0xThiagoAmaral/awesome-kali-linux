#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Synthetic loopback-only HTTP fixture; no Internet required."""
import http.server
import json

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        code = 200 if self.path in ['/admin', '/health'] else 404
        body = json.dumps({'path':self.path, 'fixture':True, 'status':code}).encode()
        self.send_response(code)
        self.send_header('Content-Type','application/json')
        self.send_header('Content-Length',str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    def log_message(self, *args):
        pass

if __name__ == '__main__':
    server = http.server.ThreadingHTTPServer(('127.0.0.1',8000),Handler)
    print('Fixture local: http://127.0.0.1:8000 — Ctrl+C para encerrar',flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
