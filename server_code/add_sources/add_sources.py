from database import database as db

def load_add_sources_page(DOC_ROOT):
	with open(DOC_ROOT+"/frontend/html/add_sources.template.html",'r') as descriptor:
		return descriptor.read()

def add_sources(user_id,source_name):
	db.add_new_source(user_id,source_name)
	
