from database import database as db

def add_sources(user_id,source_name):
	db.add_new_source(user_id,source_name)
	
