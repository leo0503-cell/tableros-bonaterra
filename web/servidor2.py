import http.server, socketserver
class H(http.server.SimpleHTTPRequestHandler):
    def guess_type(self, path):
        t = super().guess_type(path)
        if t == 'text/html':
            return 'text/html; charset=utf-8'
        return t
socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("127.0.0.1", 8914), H) as s:
    s.serve_forever()
