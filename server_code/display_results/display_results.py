import os
import time
from database import database as db 

def display_results(DOC_ROOT, userid, source):
	# query last 24 hours and save graphs
	queryResults = db.query(DOC_ROOT, userid, source, 1, 24)
	temp = [i[0] for i in queryResults]
	hum = [i[1] for i in queryResults]
	db.save_graph(DOC_ROOT, range(1,25), temp, hum, userid, source)

	with open(DOC_ROOT+"/frontend/html/display_results.template.html",'r') as descriptor:
		template = descriptor.read()

		# Get user + source specific files
		temp_path = DOC_ROOT + '/tmp_files/'+userid+'_'+source+'_temp.png'
		hum_path = DOC_ROOT + '/tmp_files/'+userid+'_'+source+'_hum.png'
		# Get label
		label = db.get_label(DOC_ROOT, userid, source)

		# Check if image paths exist
		if not os.path.exists(temp_path) or not os.path.exists(hum_path):
			print('ERROR: Cannot find png file(s)!')
			return

		### Find and Replace HTML variables
		find_temp = template.find("{{temperature.png}}")
		find_hum = template.find("{{humidity.png}}")
		find_label = template.find("{{source_label}}")

		if find_temp!=-1 and find_hum!=-1 and find_label!=-1:
			template = template.replace("{{temperature.png}}", temp_path)
			template = template.replace("{{humidity.png}}", hum_path)
			template = template.replace("{{source_label}}", label)
		else: 
			print("ERROR: HTML variable missing!")

		return template