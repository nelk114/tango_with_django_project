from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from rango.models import Category,Page
from rango.forms import CategoryForm,PageForm,UserForm,UserProfileForm
from datetime import datetime as DT

def visitor_cookie_handler(r,a):
	n=int(r.COOKIES.get('visits','1'))
	c=r.COOKIES.get('last_visit',str(DT.now()))
	t=DT.strptime(c[:-7],'%Y-%m-%d %H:%M:%S')
	if (DT.now()-t).days>0:n+=1;a.set_cookie('last_visit',str(DT.now()))
	else:a.set_cookie('last_visit',c)
	a.set_cookie('visits',n)

def index(r):
	r.session.set_test_cookie()
	context_dict={
		'boldmessage':'Crunchy, creamy, cookie, candy, cupcake!',
		'categories':Category.objects.order_by('-likes')[:5],
		'pages':Page.objects.order_by('-views')[:5],
		'visits':int(r.COOKIES.get('visits','1'))
		}
	a=render(r,'rango/index.html',context=context_dict)
	visitor_cookie_handler(r,a);return a

def about(r):
	if r.session.test_cookie_worked():print('TEST COOKIE WORKED!');r.session.delete_test_cookie()
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

@login_required
def add_category(r):
	f=CategoryForm()
	if r.method=='POST':
		f=CategoryForm(r.POST)
		if f.is_valid():f.save(commit=True);return redirect('/rango/')
		else:print(f.errors)
	return render(r,'rango/add_category.html',{'form':f})

@login_required
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

def register(r):
	reg=False
	if r.method=='POST':
		uf=UserForm(r.POST);pf=UserProfileForm(r.POST)
		if uf.is_valid() and pf.is_valid():
			l=uf.save()
			l.set_password(l.password);l.save()
			p=pf.save(commit=False)
			p.user=l
			if 'picture' in r.FILES:p.picture=r.FILES['picture']
			p.save()
			reg=True
		else:print(uf.errors,pf.errors)
	else:
		uf=UserForm();pf=UserProfileForm()
	return render(r,'rango/register.html',context={'user_form':uf,'profile_form':pf,'registered':reg})

def user_login(r):
	if r.method=='POST':
		n=r.POST.get('username');p=r.POST.get('password')
		l=authenticate(username=n,password=p)
		if l:
			if l.is_active:login(r,l);return redirect(reverse('rango:index'))
			else:return HttpResponse('Your Rango account is disabled.')
		else:print(f'Invalid login details: {n}, {p}');return HttpResponse('Invalid login details supplied.')
	else:return render(r,'rango/login.html')

@login_required
def restricted(r):
	return render(r,'rango/restricted.html')

def user_logout(r):
	logout(r)
	return redirect(reverse('rango:index'))
