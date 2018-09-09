

def login():
	with open("login.template.html",'r') as descriptor:
		return descriptor.read()