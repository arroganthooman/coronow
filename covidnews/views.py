from django.shortcuts import render,redirect
from .models import Comment, News
from django.views.generic.edit import CreateView
from .forms import NewsForm
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse


# Create your views here.
def covidNews(request):
	news = News.objects.all()
	response = {
		'news': news,
	}
	return render(request, 'news.html', response)

def isiNews(request,pk):
	news = News.objects.get(id=pk)
	comments = Comment.objects.all()

	response = {
		'news' : news,
		'comments': comments
	}
	return render(request, 'detailNews.html', response)

def getAllComment(request,pk):
	
	news= News.objects.get(id=int(pk))
	comment = Comment.objects.filter(berita=news)
	data=serializers.serialize("json",comment)
	return HttpResponse(data,content_type="text/json-comment-filtered")

def postComment(request,pk):
	if request.method == "POST":
		nama = request.POST.get('nama')
		komentar = request.POST.get('komentar')
		news_obj = News.objects.get(id=int(pk))

		comment = Comment.objects.create(nama=nama, komentar=komentar, berita=news_obj)
		comment.save()
		comments= Comment.objects.filter(berita=news_obj)
		comment_data= serializers.serialize("json",comments)
		return HttpResponse(comment_data,content_type="text/json-comment-filtered")



#@login_required(login_url='/login')
class NewsCreate(CreateView):
	template_name='covidnews/news_form.html'
	form_class= NewsForm
	#model = News
	#fields=['Judul','description','isi','Foto','Sumber']

