#!/usr/bin/env python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import os,subprocess,ast,json

PORT = 8000
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
        # this is so no one caches our page as caching would give false positives
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma","no-cache")
        self.send_header("Expires", "0")
        self.end_headers()

    def do_GET(self):
        if self.path == "/":
		    with open(DOC_ROOT+"/index/index.html") as handler:
		        self._set_headers()
		        content = handler.read()
		        self.wfile.write(content)
		elif self.path == "login":
			pass
		elif self.path == "list_sources":
			pass
		elif self.path == "display_results":
			pass
		elif self.path == "add_source":
			pass



    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        self._set_headers()


def run(server_class=HTTPServer, handler_class=Handler, port=PORT):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print '[*] Starting httpd at port', PORT
    httpd.serve_forever()


# write_file()
run()