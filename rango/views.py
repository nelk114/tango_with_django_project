from django.shortcuts import render,redirect
from django.http import HttpResponse
from rango.models import Category,Page
from rango.forms import CategoryForm

def index(r):
	context_dict={
		'boldmessage':'Crunchy, creamy, cookie, candy, cupcake!',
		'categories':Category.objects.order_by('-likes')[:5],
		'pages':Page.objects.order_by('-views')[:5],
		}
	return render(r,'rango/index.html',context=context_dict)

def about(r):
	ctx={'nm':'Bernhard Nicolás Ersfeld Mandujano'}
	return render(r,'rango/about.html',context=ctx)

def show_category(r,category_name_slug):	#Slug as 2nd param
	ctx={}
	try:
		cat=Category.objects.get(slug=category_name_slug)
		ctx['category']=cat;ctx['pages']=Page.objects.filter(category=cat)
	except Category.DoesNotExist:
		ctx['category']=None;ctx['pages']=None
	return render(r,'rango/category.html',context=ctx)

def add_category(r):
	f=CategoryForm()
	if r.method=='POST':
		f=CategoryForm(r.POST)
		if f.is_valid():f.save(commit=True);return redirect('/rango/')
		else:print(f.errors)
	return render(r,'rango/add_category.html',{'form':f})
