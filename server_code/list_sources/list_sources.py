from database import database as db 

def list_sources(DOC_ROOT, userid):
	'''
	List all user sources.

	Args:
		DOC_ROOT (str): Path to project directory
        userid (str): Unique id for user

	Returns:
		template (str): Updated HTML template
	'''
	# Get sources and their respective labels
	sources_labels = db.get_sources(DOC_ROOT, userid)
	sources = [i[0] for i in sources_labels]
	labels = [i[1] for i in sources_labels]

	with open(DOC_ROOT+"/frontend/html/list_sources.template.html",'r') as descriptor:
		template = descriptor.read()

		# HTML template for listing sources
		box = '''
				<div class = "box" onclick = "location.href='{{url}}'">
				<h2>{{source_label}}</h2>
				</div>
			  '''
		all_boxes = ""

		# Add in new html div box for each source
		if len(sources) != 0:
			for i in range(len(sources)):
				url = "display_results/"+str(sources[i])
				source_label = labels[i]
				mod_box = box.replace("{{url}}", url)
				mod_box = mod_box.replace("{{source_label}}", source_label)
				all_boxes = all_boxes + mod_box
		else:
			all_boxes = '''
						<div class = "box"">
						<h2>You have no sources!</h2>
						</div>
						'''
		# Check html variables exists
		find_list = template.find("{{list}}")
		find_add_sources_url = template.find("{{add_sources_url}}")
		if find_list == -1 or find_add_sources_url == -1:
			print('ERROR: HTML variable missing!')
			return template

		# Replace HTML variables
		template = template.replace('{{list}}', all_boxes)
		template = template.replace('{{add_sources_url}}', userid + "/add_sources/")

		return template

