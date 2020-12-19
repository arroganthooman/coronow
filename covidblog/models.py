from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.dispatch import receiver
from cloudinary.models import CloudinaryField
from django.db.models.signals import pre_delete
import cloudinary
import os

# Create your models here.

class BlogQuerySet(models.QuerySet):
    def delete(self, *args, **kwargs):
        for obj in self:
            cloudinary.uploader.destroy(obj.image.public_id)
        super(BlogQuerySet, self).delete(*args, **kwargs)


class Blog(models.Model):
    objects = BlogQuerySet.as_manager()
    author = models.ForeignKey(User, default=None, on_delete=models.PROTECT, db_constraint=False)
    title = models.CharField(max_length=200, blank=False)
    post_date = models.DateField(auto_now_add = True)
    image = CloudinaryField("image")
    body = RichTextField(blank=False, null=False)
    snippet = RichTextField(blank=False, null=False, max_length=100)
    acc = models.BooleanField(default=False)
    
    def __str__(self):
    	return self.title


class Comment(models.Model):
	komentar = models.CharField(max_length=200, null=False, blank=False)
	nama = models.CharField(max_length=30)
	blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
	post_date = models.DateField(auto_now_add=True)

	def __str__(self):
		return self.nama



## delete image when delete models
@receiver(pre_delete, sender=Blog)
def image_delete(sender, instance, **kwargs):
    cloudinary.uploader.destroy(instance.image.public_id)

## delete old image when replacing image
@receiver(models.signals.pre_save, sender=Blog)
def auto_delete_file_on_change(sender, instance, **kwargs):

    try:
        old_file = sender.objects.get(pk=instance.pk).image
    except sender.DoesNotExist:
        return False

    new_file = instance.image
    if not old_file == new_file:
        cloudinary.uploader.destroy(old_file.public_id)
