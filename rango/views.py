from django.shortcuts import render
from django.http import HttpResponse

def index(r):
	context_dict={'boldmessage':'Crunchy, creamy, cookie, candy, cupcake!'}
	return render(r,'rango/index.html',context=context_dict)

def about(r):
	ctx={'nm':'Bernhard Nicolás Ersfeld Mandujano'}
	return render(r,'rango/about.html',context=ctx)
