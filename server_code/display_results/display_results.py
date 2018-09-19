import os
from database import database as db 

def display_results(DOC_ROOT, userid, source):
	'''
	Display temp and hum graph for source belonging to user.

	Args:
		DOC_ROOT (str): Path to project directory
        userid (str): Unique id for user
        source (int): Source number

	Returns:
		template (str): Updated HTML template
	'''
	# query last 24 hours and save graphs
	queryResults = db.query(DOC_ROOT, userid, source, 0, 23)
	temp = [i[0] for i in queryResults]
	hum = [i[1] for i in queryResults]
	db.save_graph(DOC_ROOT, range(24), temp, hum, userid, source)

	# Modify html file
	with open(DOC_ROOT+"/frontend/html/display_results.template.html",'r') as descriptor:
		template = descriptor.read()

		# Get user + source specific files
		temp_path = '/tmp_files/'+userid+'_'+source+'_temp.png'
		hum_path = '/tmp_files/'+userid+'_'+source+'_hum.png'
		# Get label of source
		label = db.get_label(DOC_ROOT, userid, source)

		### Find and Replace HTML variables
		# Check that images exist
		if not os.path.isfile(DOC_ROOT + temp_path) or not os.path.isfile(DOC_ROOT + hum_path):
			print('ERROR: Image path does not exist!')
			return template;
		

		# Check if variables in html file
		find_temp = template.find("{{temperature.png}}")
		find_hum = template.find("{{humidity.png}}")
		find_label = template.find("{{source_label}}")
		if find_temp!=-1 and find_hum!=-1 and find_label!=-1:
			# Replace variables
			template = template.replace("{{temperature.png}}", temp_path)
			template = template.replace("{{humidity.png}}", hum_path)
			template = template.replace("{{source_label}}", label)
		else: 
			print("ERROR: HTML variable missing!")

		return template