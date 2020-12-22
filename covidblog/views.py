from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Comment, Blog
from .forms import BlogForm
from django.core import serializers
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def covidBlog(request):
	blog = Blog.objects.all()
	# data = serializers.serialize("json", blog)
	# blog_dict = model_to_dict(blog)
	# blog_json = json.dumps(blog_dict)
	response = {
		'blog': blog,
	}
	return render(request, 'covidBlog.html', response)
	# return JsonResponse(blog_json)
	# return HttpResponse(data, content_type="text/json-comment-filtered")

def isiBlog(request,pk):
	# if request.method == "POST":
	# 	nama = request.POST.get("nama")
	# 	komentar = request.POST.get("komentar")
	# 	blog = Blog.objects.get(id=pk)
	# 	if len(nama)<=30 and len(komentar)<=100:
	# 		comment = Comment.objects.create(nama=nama, komentar=komentar, blog=blog)
	# 		return redirect(f'/covidBlog/blog/{pk}#{comment.id}')

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
		form = BlogForm(request.POST, request.FILES)
		context['posted'] = form.instance
		if form.is_valid():
			instance = form.save(commit=False)
			instance.author = request.user
			instance.save()
			return render(request, "thanks.html")

	return render(request, 'addBlog.html', context)



def getAllComment(request,pk):
	blog = Blog.objects.get(id=int(pk))
	comment = Comment.objects.filter(blog=blog)
	data = serializers.serialize("json", comment)
	return HttpResponse(data, content_type="text/json-comment-filtered")


def postComment(request, pk):
	if request.method == "POST":
		nama = request.POST.get('nama')
		komentar = request.POST.get('komentar')
		blog_obj = Blog.objects.get(id=int(pk))

		comment = Comment.objects.create(nama=nama, komentar=komentar, blog=blog_obj)
		comment.save()
		comments = Comment.objects.filter(blog=blog_obj)
		comment_data = serializers.serialize("json", comments)
		return HttpResponse(comment_data, content_type="text/json-comment-filtered")