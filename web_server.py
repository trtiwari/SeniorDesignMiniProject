#!/usr/bin/env python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from server_code.login.login import login
from server_code.sources.sources import sources
from server_code.display_results.display_results import display_results

PORT = 80
DOC_ROOT = "/root/Documents/Senior/SeniorThesis/SeniorDesignMiniProject"

class Handler(BaseHTTPRequestHandler):
    def _set_headers(self,extension="html"):
        self.send_response(200)
        if extension == "js":
        	self.send_header("Content-type","text/javascript")
        elif extension == "css":
        	self.send_header("Content-type","text/css")
        elif extension == "jpeg" or extension == "jpg":
            self.send_header("Content-type","image/jpeg")
        elif extension == "png":
            self.send_header("Content-type","image/png")
        else:
        	self.send_header("Content-type","text/html")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma","no-cache")
        self.send_header("Expires", "0")
        self.end_headers()

    def do_GET(self):
        if self.path == "/":
            self.path = "/login"
        if "/frontend/images" in self.path:
            extension = self.path.split(".")[-1]
            self._set_headers(extension=extension)
            with open(DOC_ROOT + self.path) as descriptor:
                content = descriptor.read()
                self.wfile.write(content)
        elif "/frontend/javascript" in self.path:
            extension = self.path.split(".")[-1]
            self._set_headers(extension=extension)
            with open(DOC_ROOT + self.path) as descriptor:
                content = descriptor.read()
                self.wfile.write(content)
        elif "/frontend/css" in self.path:
            extension = self.path.split(".")[-1]
            self._set_headers(extension=extension)
            with open(DOC_ROOT + self.path) as descriptor:
                content = descriptor.read()
                self.wfile.write(content)
        elif "/sources/add_sources" in self.path:
            pass
        elif "/login" in self.path:
            self._set_headers()
            content = login(DOC_ROOT)
            self.wfile.write(content)
        elif "/list_sources" in self.path:
            self._set_headers()
            sources()
        elif "/display_results" in self.path:
            self._set_headers()
            user_id = self.path.split("/")[0]
            source = self.path.split("/")[1]
            content = display_results(user_id, source)
            self.wfile.write(content)
        elif "/sources" in self.path:
            self._set_headers()
            print self.path
            user_id = self.path.split("/")[0]
            print user_id
            content = sources(user_id)

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        self._set_headers()


def run(server_class=HTTPServer, handler_class=Handler, port=PORT):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print '[*] Starting httpd at port', PORT
    httpd.serve_forever()

if __name__ == "__main__":
    run()

# add_sources
# sign_out
# urls