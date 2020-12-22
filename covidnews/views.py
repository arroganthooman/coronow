from django.shortcuts import render,redirect
from .models import Comment, News
from django.views.generic.edit import CreateView
from .forms import NewsForm
from django.contrib.auth.decorators import login_required


# Create your views here.
def covidNews(request):
	news = News.objects.all()
	response = {
		'news': news,
	}
	return render(request, 'news.html', response)

def isiNews(request,pk):
	if request.method == "POST":
		nama = request.POST.get("nama")
		komentar = request.POST.get("komentar")
		news = News.objects.get(id=pk)
		if len(nama)<=30 and len(komentar)<=100:
			comment = Comment.objects.create(nama=nama, komentar=komentar, berita=news)
			return redirect(f'/covidnews/news/{pk}#{comment.id}')

	news = News.objects.get(id=pk)
	comments = Comment.objects.all()

	response = {
		'news' : news,
		'comments': comments
	}
	return render(request, 'detailNews.html', response)

#@login_required(login_url='/login')
class NewsCreate(CreateView):
	template_name='covidnews/news_form.html'
	form_class= NewsForm
	#model = News
	#fields=['Judul','description','isi','Foto','Sumber']

