from database import database as db

def load_add_sources_page(DOC_ROOT):
	'''
	loads the html template that displays the page
	where the user can add sources

	Args: 
		DOC_ROOT (str): the Document Root of the webserver
	Returns:
		template (str): the HTML template for the add sources page
	'''
	with open(DOC_ROOT+"/frontend/html/add_sources.template.html",'r') as descriptor:
		return descriptor.read()

def add_sources(DOC_ROOT,user_id,source_label):
	'''
	this function is run when the user requests a new source to be added
	to his "home"

	Args: 
		DOC_ROOT (str): the Document Root of the webserver

	Returns:
		template (str): the *updated* HTML template containing the new
						source that the user just added
	'''
	source_label = source_label.replace("+"," ")
	db.add_source(DOC_ROOT, user_id,source_label)
	with open(DOC_ROOT+"/frontend/html/source_added.template.html",'r') as descriptor:
		template = descriptor.read()
		url = "/" + user_id + "/list_sources"	
		template = template.replace('{{url}}', url)
		return template
