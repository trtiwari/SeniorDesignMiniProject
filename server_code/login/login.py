

def login(DOC_ROOT):
	'''
	loads the login page
	Args: 
		DOC_ROOT (str): the document root of the webserver
	Returns:
		template (str): HTML template for the login page
	'''
	with open(DOC_ROOT+"/frontend/html/login.template.html",'r') as descriptor:
		return descriptor.read()