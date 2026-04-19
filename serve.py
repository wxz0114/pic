#!/usr/bin/env python3
"""启动后浏览器访问 http://localhost:8000 即可查看图片"""
import json, os, re, sys
from http.server import HTTPServer, SimpleHTTPRequestHandler

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
MEDIA_EXT = re.compile(r'\.(jpe?g|png|gif|webp|bmp|svg|mp4|webm|mov|avi)$', re.I)

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/files':
            files = []
            for root, _, names in os.walk('.'):
                for name in sorted(names):
                    if MEDIA_EXT.search(name):
                        rel = os.path.join(root, name).replace('\\', '/').lstrip('./')
                        if not rel.startswith('.'):
                            files.append(rel)
            files.sort()
            data = json.dumps(files, ensure_ascii=False).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', len(data))
            self.end_headers()
            self.wfile.write(data)
        else:
            super().do_GET()

os.chdir(os.path.dirname(os.path.abspath(__file__)) or '.')
print(f'Serving at http://localhost:{PORT}')
HTTPServer(('0.0.0.0', PORT), Handler).serve_forever()
