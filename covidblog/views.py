from django.shortcuts import render
from .models import Comment, Admin, Blog

# Create your views here.

def covidBlog(request):
	blog = Blog.objects.all()
	response = {
		'blog': blog,
	}
	return render(request, 'covidBlog.html', response)
