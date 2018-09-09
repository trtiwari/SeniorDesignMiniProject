

def login(DOC_ROOT):
	with open(DOC_ROOT+"/templates/html/login.template.html",'r') as descriptor:
		return descriptor.read()