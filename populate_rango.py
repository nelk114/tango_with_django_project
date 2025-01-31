import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','tango_with_django_project.settings')

import django
django.setup()
from rango.models import Category,Page

def add_page(c,t,l,v=0):
	p=Page.objects.get_or_create(category=c,title=t)[0]
	p.url=l;p.views=v
	p.save()
	return p
def add_cat(n,v,l):
	c=Category.objects.get_or_create(name=n,views=v,likes=l)[0]
	c.save()
	return c

def populate():
	pPyþ=[
		{'title':'Official Python Tutorial','url':'http://docs.python.org/3/tutorial/','views':5},
		{'title':'How to Think like a Computer Scientist','url':'http://www.greenteapress.com/thinkpython/','views':8},
		{'title':'Learn Python in 10 Minutes','url':'http://www.korokithakis.net/tutorials/python/','views':95},
		]
	pDja=[
		{'title':'Official Django Tutorial','url':'https://docs.djangoproject.com/en/2.1/intro/tutorial01/','views':3},
		{'title':'Django Rocks','url':'http://www.djangorocks.com/','views':2},
		{'title':'How to Tango with Django','url':'http://www.tangowithdjango.com/','views':5},
		]
	pOþ=[
		{'title':'Bottle','url':'http://bottlepy.org/docs/dev/','views':1},
		{'title':'Flask','url':'http://flask.pocoo.org','views':1},
		]
	cats={'Python':{'pages':pPyþ,'views':128,'likes':64},'Django':{'pages':pDja,'views':64,'likes':32},'Other Frameworks':{'pages':pOþ,'views':32,'likes':16},}
	for c,d in cats.items():
		m=add_cat(c,d['views'],d['likes'])
		for p in d['pages']:add_page(m,p['title'],p['url'],p['views'])
	for c in Category.objects.all():
		for p in Page.objects.filter(category=c):print(f'- {c}: {p}')

if __name__=='__main__':
	print('Starting Rango population script...')
	populate()
