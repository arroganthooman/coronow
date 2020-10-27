from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.


class Admin(models.Model):
	nama = models.CharField(max_length=30)

	def __str__(self):
		return self.nama


class Blog(models.Model):
	author = models.ForeignKey(Admin, blank=False, on_delete=models.CASCADE)
	title = models.CharField(max_length=200, blank=False)
	post_date = models.DateField(auto_now_add = True)
	image = models.ImageField(null = False, blank = False, upload_to='images/')
	body = RichTextField(blank=False, null=False)

	def __str__(self):
		return self.title


class Comment(models.Model):
	komentar = models.CharField(max_length=200, null=False)
	nama = models.CharField(max_length=30)

	def __str__(self):
		return self.nama