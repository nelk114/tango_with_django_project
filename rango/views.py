from django.shortcuts import render
from django.http import HttpResponse

def index(r):
	context_dict={'boldmessage':'Crunchy, creamy, cookie, candy, cupcake!'}
	return render(r,'rango/index.html',context=context_dict)

def about(r):
	return HttpResponse('Rango says here is the about page.<br><a href=\'/rango/\'>Index</a>')
