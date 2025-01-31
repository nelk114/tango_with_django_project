from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category

def index(r):
	context_dict={
		'boldmessage':'Crunchy, creamy, cookie, candy, cupcake!',
		'categories':Category.objects.order_by('-likes')[:5],
		}
	return render(r,'rango/index.html',context=context_dict)

def about(r):
	ctx={'nm':'Bernhard Nicolás Ersfeld Mandujano'}
	return render(r,'rango/about.html',context=ctx)
