"""
Demonstrates that requests violates one of paragraphs of rfc6265.

Create issue https://github.com/kennethreitz/requests/issues/2576

Use twoliner to add hosts to /etc/hosts

echo "127.0.0.1       test.com
127.0.0.1       subdomain.test.com" |  sudo tee -a /etc/hosts
"""

import BaseHTTPServer
import requests
import threading


# http server
class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        l = self.headers.get('Host').lower()
        print "Server: processing {}".format(l)

        if l == 'test.com:8000':
            self.send_response(301)
            self.send_header('Set-Cookie', 'Test=True')
            self.send_header('Location', 'http://subdomain.test.com:8000')
        elif l == 'subdomain.test.com:8000':
            print "---> Cookie: {} <---".format(self.headers.get('Cookie'))
            self.send_response(200)
        else:
            assert False, "Not supported"


httpd = BaseHTTPServer.HTTPServer(('', 8000), RequestHandler)


def server_callback():
    while True:
        httpd.handle_request()

server_thread = threading.Thread(target=server_callback)
server_thread.daemon = True
server_thread.start()

# http client
requests.get('http://test.com:8000')
