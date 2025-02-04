from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import HttpResponse
from rango.models import Category,Page
from rango.forms import CategoryForm,PageForm

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

def add_page(r,category_name_slug):
	try:cat=Category.objects.get(slug=category_name_slug)
	except Category.DoesNotExist:cat=None
	if cat is None:return redirect('/rango/')
	f=PageForm()
	if r.method=='POST':
		f=PageForm(r.POST)
		if f.is_valid():
			if cat:
				p=f.save(commit=False)
				p.category=cat;p.views=0
				p.save()
				return redirect(reverse('rango:show_category',kwargs={'category_name_slug':category_name_slug}))
		else:print(f.errors)
	return render(r,'rango/add_page.html',context={'form':f,'category':cat})
