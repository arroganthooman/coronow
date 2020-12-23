from django.db import models
from ckeditor.fields import RichTextField
from django.urls import reverse
# Create your models here.

class News(models.Model):
    # fields of the model 
    Judul= models.CharField(max_length = 200)  
    description = models.TextField() 
    post_date = models.DateField(auto_now_add = True)
    isi = RichTextField(blank=False, null=False)
    Foto= models.TextField()
    Sumber= models.TextField()
    # renames the instances of the model 
    # with their title name 
    def __str__(self): 
        return self.Judul
    def get_absolute_url(self):
        return reverse('news', args=[str(self.id)])

class Comment(models.Model):
	komentar = models.CharField(max_length=200, null=False, blank=False)
	nama = models.CharField(max_length=30)
	berita = models.ForeignKey(News, on_delete=models.CASCADE)
	post_date = models.DateField(auto_now_add=True)

	def __str__(self):
		return self.nama