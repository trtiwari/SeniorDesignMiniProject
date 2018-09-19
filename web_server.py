#!/usr/bin/env python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import subprocess,os,re
from server_code.login import login
from server_code.list_sources import list_sources
from server_code.add_sources import add_sources
from server_code.display_results import display_results
from server_code.add_sources import add_sources
from database import database as db

PORT = 80
pwd = subprocess.Popen("pwd",stdout=subprocess.PIPE)
DOC_ROOT = str(pwd.stdout.read()[:-1])

class Handler(BaseHTTPRequestHandler):
    def _set_headers(self,extension="html",response=200):
        self.send_response(response)
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
        # set the default path to login
        if self.path == "/":
            self.path = "/login"
        # this path contains all the images in the web pages.
        # we just read the image file requested and return it
        # as a response to the client
        if "/frontend/images" in self.path:
            extension = self.path.split(".")[-1]
            self._set_headers(extension=extension)
            with open(DOC_ROOT + self.path) as descriptor:
                content = descriptor.read()
                self.wfile.write(content)
        # contains all javascript files
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
        # this URL is invoked when the 
        elif "/add_sources?source_name" in self.path:
            user_id = self.path.split("/")[1]
            source_label = self.path.split("=")[1]
            content = add_sources.add_sources(DOC_ROOT,user_id,source_label)
            self.wfile.write(content)
        elif "/add_sources" in self.path:
            content = add_sources.load_add_sources_page(DOC_ROOT)
            self.wfile.write(content)
        elif "/login" in self.path:
            self._set_headers()
            content = login.login(DOC_ROOT)
            self.wfile.write(content)
        elif "/list_sources" in self.path:
            self._set_headers()
            user_id = self.path.split("/")[1]
            content = list_sources.list_sources(DOC_ROOT, user_id)
            self.wfile.write(content)
        elif "/display_results" in self.path:
            self._set_headers()
            user_id = self.path.split("/")[1]
            source = self.path.split("/")[3]
            content = display_results.display_results(DOC_ROOT, user_id, source)
            self.wfile.write(content)
        elif "/tmp_files" in self.path:
            extension = self.path.split(".")[-1]
            self._set_headers(extension=extension)
            print(self.path)
            with open(DOC_ROOT + self.path) as descriptor:
                content = descriptor.read()
                self.wfile.write(content)
        elif "/logout" in self.path:
            user_id = self.path.split("/")[1]
            for f in os.listdir(DOC_ROOT + "/tmp_files/"):
                if re.search("{0}*".format(user_id), f):
                    os.remove(os.path.join(dir, f))
                    print("reached here")
        else:
            self._set_headers(response=404)
            with open(DOC_ROOT + "/frontend/html/404.template.html") as descriptor:
                content = descriptor.read()
                self.wfile.write(content)
            

    def do_HEAD(self):
        '''
            responds to HTTP HEAD requests by sending just the response headers
        '''
        self._set_headers()
        
    def do_POST(self):
        '''
            A stub POST function. We don't actually ever use POST requests, 
            but if the user accidently submits a POST request, we have this 
            function implemented just so the application doesn't error out.
            It just returns the response headers.
        '''
        self._set_headers()


def run(server_class=HTTPServer, handler_class=Handler, port=PORT):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print '[*] Starting httpd at port', PORT
    httpd.serve_forever()

if __name__ == "__main__":
    db.create_table()
    run()