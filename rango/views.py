from django.shortcuts import render
from django.http import HttpResponse

def index(r):
	return HttpResponse('Rango says hey there partner!')
