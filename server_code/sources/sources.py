
def sources(user_id):
	sources_labels = get_sources(user_id)
	sources = [i[0] for i in sources_labels]
	labels = [i[1] for i in sources_labels]

	with open("sources.template.html",'r') as descriptor:
		template = descriptor.read()

	return template

def add_sources(user_id):
	add_new_source(user_id,source_name)
	
