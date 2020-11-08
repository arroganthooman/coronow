from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

# Create your models here.
class Blog(models.Model):
	author = models.ForeignKey(User, default=None, on_delete=models.PROTECT, db_constraint=False)
	title = models.CharField(max_length=200, blank=False)
	post_date = models.DateField(auto_now_add = True)
	image = models.ImageField(null = False, blank = False, upload_to='images/')
	body = RichTextField(blank=False, null=False)
	snippet = RichTextField(blank=False, null=False, max_length=100)

	def __str__(self):
		return self.title


class Comment(models.Model):
	komentar = models.CharField(max_length=200, null=False, blank=False)
	nama = models.CharField(max_length=30)
	blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
	post_date = models.DateField(auto_now_add=True)

	def __str__(self):
		return self.nama