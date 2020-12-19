from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Comment, Blog
from .forms import BlogForm#, PhotoForm

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
			comment = Comment.objects.create(nama=nama, komentar=komentar, blog=blog)
			return redirect(f'/covidBlog/blog/{pk}#{comment.id}')

	blog = Blog.objects.get(id=pk)
	comments = Comment.objects.all()

	response = {
		'blog' : blog,
		'comments': comments
	}
	
	return render(request, 'isiBlog.html', response)

@login_required(login_url='/login')
def addPost(request):
	context = {
	'form':BlogForm()
	}

	if request.method == "POST":
		# form_photo = PhotoForm(request.POST, request.FILES)
		form = BlogForm(request.POST, request.FILES)
		context['posted'] = form.instance
		if form.is_valid():
			instance = form.save(commit=False)
			instance.author = request.user
			instance.save()
			return render(request, "thanks.html")

	return render(request, 'addBlog.html', context)
