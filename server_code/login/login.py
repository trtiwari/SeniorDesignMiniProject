

def login(DOC_ROOT):
	with open(DOC_ROOT+"/frontend/html/login.template.html",'r') as descriptor:
		return descriptor.read()