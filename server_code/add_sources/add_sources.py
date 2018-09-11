from database import database as db

def load_add_sources_page(DOC_ROOT):
	with open(DOC_ROOT+"/frontend/html/add_sources.template.html",'r') as descriptor:
		return descriptor.read()

def add_sources(DOC_ROOT,user_id,source_label):
	source_label = source_label.replace("+"," ")
	db.add_source(user_id,source_label)
	with open(DOC_ROOT+"/frontend/html/source_added.template.html",'r') as descriptor:
		return descriptor.read()	
	
