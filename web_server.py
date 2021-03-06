#!/usr/bin/env python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import subprocess,os,re
from server_code.login import login
from server_code.list_sources import list_sources
from server_code.add_sources import add_sources
from server_code.display_results import display_results
from server_code.add_sources import add_sources
from database import database as db

# the default port for HTTP
PORT = 80
# obtains the document root of the webserver
pwd = subprocess.Popen("pwd",stdout=subprocess.PIPE)
DOC_ROOT = str(pwd.stdout.read()[:-1])

class Handler(BaseHTTPRequestHandler):
    def _set_headers(self,extension="html",response=200):
        '''
            sets the headers for the HTTP response
                sets the correct content type (HTML CSS JS JPEG/PNG)
                sets the response type (200 or 404)
                sets the cache headers
        '''
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
        # the following headers ensure none of these pages are cached.
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma","no-cache")
        self.send_header("Expires", "0")
        self.end_headers()

    def do_GET(self):
        '''
            implements the response to an HTTP GET request
        '''
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
        # this URL is invoked when the user wants to add a new source
        # stored in the GET request parameter 'source_name'
        elif "/add_sources?source_name" in self.path:
            user_id = self.path.split("/")[1]
            source_label = self.path.split("=")[1]
            content = add_sources.add_sources(DOC_ROOT,user_id,source_label)
            self.wfile.write(content)
        # invoked when the user loads the add source page
        elif "/add_sources" in self.path:
            content = add_sources.load_add_sources_page(DOC_ROOT)
            self.wfile.write(content)
        # loading login page
        elif "/login" in self.path:
            self._set_headers()
            content = login.login(DOC_ROOT)
            self.wfile.write(content)
        # page that lists all sources the user has
        elif "/list_sources" in self.path:
            self._set_headers()
            user_id = self.path.split("/")[1]
            content = list_sources.list_sources(DOC_ROOT, user_id)
            self.wfile.write(content)
        # page that displays the temp/humidity graphs for a particular source for
        # a particular user
        elif "/display_results" in self.path:
            self._set_headers()
            user_id = self.path.split("/")[1]
            source = self.path.split("/")[3]
            content = display_results.display_results(DOC_ROOT, user_id, source)
            self.wfile.write(content)
        # this is where the user's graphs are temporarily cached 
        # when they're generated to be shown to the user
        elif "/tmp_files" in self.path:
            extension = self.path.split(".")[-1]
            self._set_headers(extension=extension)
            print(self.path)
            with open(DOC_ROOT + self.path) as descriptor:
                content = descriptor.read()
                self.wfile.write(content)
        # invoked when user clicks on the sign out link
        # this deletes all of the temp/humidity files generated for a particular
        # user during his session
        elif "/logout" in self.path:
            user_id = self.path.split("/")[1]
            for f in os.listdir(DOC_ROOT + "/tmp_files/"):
                if re.search("{0}*".format(user_id), f):
                    os.remove(os.path.join(DOC_ROOT + "/tmp_files/", f))
                    print("deleted cached files ...")
        # a catch-all block for random URLs that don't point to anything
        # displays a 404 message
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