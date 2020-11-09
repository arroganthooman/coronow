from django.shortcuts import render, redirect
from .models import Comment, Blog

# Create your views here.

def covidBlog(request):
	blog = Blog.objects.all()
	response = {
		'blog': blog,
	}
	return render(request, 'covidBlog.html', response)

def isiBlog(request,pk):

	if request.method == "POST":
		nama = request.POST.get("nama")
		komentar = request.POST.get("komentar")
		blog = Blog.objects.get(id=pk)
		if len(nama)<=30 and len(komentar)<=100:
			Comment.objects.create(nama=nama, komentar=komentar, blog=blog)
			return redirect(f'/covidBlog/blog/{pk}')

	blog = Blog.objects.get(id=pk)
	comments = Comment.objects.all()

	response = {
		'blog' : blog,
		'comments': comments
	}
	
	return render(request, 'isiBlog.html', response)