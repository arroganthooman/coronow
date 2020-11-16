from django.urls import path, re_path
from django.urls.conf import include
from .views import covidNews,isiNews

urlpatterns = [
    path('',covidNews, name="covidNews"),
    path('news/<pk>',isiNews,name='news')
]