from django.urls import path, re_path
from django.urls.conf import include
from .views import covidNews,isiNews,NewsCreate,getAllComment,postComment
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('',covidNews, name="covidNews"),
    path('news/<pk>',isiNews,name='news'),
    path('addNews/',login_required(NewsCreate.as_view(),login_url='/login'),name='addnews'),
    path('getAllComment/<pk>',getAllComment,name="getAllComment"),
    path('postComment/<pk>',postComment,name="postComments")
]