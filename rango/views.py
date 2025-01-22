from django.shortcuts import render
from django.http import HttpResponse

def index(r):
	return HttpResponse('Rango says hey there partner!<br><a href=\'/rango/about/\'>About</a>')

def about(r):
	return HttpResponse('Rango says here is the about page.<br><a href=\'/rango/\'>Index</a>')
