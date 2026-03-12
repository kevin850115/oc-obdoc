#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import http.server
import socketserver

PORT = 8000

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()
    
    def do_GET(self):
        if self.path.endswith('.html') or self.path.endswith('.md'):
            self.send_response(200)
            if self.path.endswith('.html'):
                self.send_header('Content-type', 'text/html;charset=utf-8')
            else:
                self.send_header('Content-type', 'text/plain;charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            with open(self.path.lstrip('/'), 'rb') as f:
                self.wfile.write(f.read())
        else:
            super().do_GET()

if __name__ == '__main__':
    with socketserver.TCPServer(('', PORT), MyHandler) as httpd:
        print(f'✅ 服务已启动，端口：{PORT}')
        print(f'📱 访问地址：http://0.0.0.0:{PORT}/')
        httpd.serve_forever()
