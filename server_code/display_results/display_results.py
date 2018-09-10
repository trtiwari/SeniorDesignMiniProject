
def display_results():
	with open("display_results.template.html",'r') as descriptor:
		template = descriptor.read()
		filename = "trtiwari_livingroom.png"
		template.find("{{tem}}")

