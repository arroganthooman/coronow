from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.dispatch import receiver
import os

# Create your models here.

class BlogQuerySet(models.QuerySet):
    def delete(self, *args, **kwargs):
        for obj in self:
            obj.image.delete(save=True)
        super(BlogQuerySet, self).delete(*args, **kwargs)


class Blog(models.Model):
	objects = BlogQuerySet.as_manager()
	author = models.ForeignKey(User, default=None, on_delete=models.PROTECT, db_constraint=False)
	title = models.CharField(max_length=200, blank=False)
	post_date = models.DateField(auto_now_add = True)
	image = models.ImageField(null = False, blank = False, upload_to='images/')
	body = RichTextField(blank=False, null=False)
	snippet = RichTextField(blank=False, null=False, max_length=100)

	def __str__(self):
		return self.title

	def delete(self, *args, **kwargs):
		self.image.delete(save=True)
		super(Blog, self).delete(*args, **kwargs)


class Comment(models.Model):
	komentar = models.CharField(max_length=200, null=False, blank=False)
	nama = models.CharField(max_length=30)
	blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
	post_date = models.DateField(auto_now_add=True)

	def __str__(self):
		return self.nama


@receiver(models.signals.pre_save, sender=Blog)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    # if not instance.pk:
    #     return False

    try:
        old_file = sender.objects.get(pk=instance.pk).image
    except sender.DoesNotExist:
        return False

    new_file = instance.image
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)