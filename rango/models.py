from django.db import models
from django.template.defaultfilters import slugify

class Category(models.Model):
	name=models.CharField(max_length=128,unique=True)
	views=models.IntegerField(default=0)
	likes=models.IntegerField(default=0)
	slug=models.SlugField(unique=True)
	def save(σ,*a,**k):
		σ.slug=slugify(σ.name)
		super(Category,σ).save(*a,**k)
	class Meta:
		verbose_name_plural='Categories'
	def __str__(σ):
		return σ.name

class Page(models.Model):
	category=models.ForeignKey(Category,on_delete=models.CASCADE)
	title=models.CharField(max_length=128)
	url=models.URLField()
	views=models.IntegerField(default=0)
	def __str__(σ):
		return σ.title
