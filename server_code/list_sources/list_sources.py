from database import database as db 

def list_sources(user_id):
	sources_labels = db.get_sources(user_id)
	sources = [i[0] for i in sources_labels]
	labels = [i[1] for i in sources_labels]

	with open("sources.template.html",'r') as descriptor:
		template = descriptor.read()


		box = '''
				<div class = "box" onclick = "location.href='{{url}}'">
				<h2>{{source_label}}</h2>
				</div>
			'''

		all_boxes = ""

		for i in range(len(sources)):
			url = userid+"/display_results/"+sources[i]
			source_label = labels[i]
			mod_box = box.replace("{{url}}", url)
			mod_box = mod_box.replace("{{source_label}}", source_label)
			all_boxes = all_boxes + mod_box

		template.replace('{{list}}', all_boxes)

	return template
