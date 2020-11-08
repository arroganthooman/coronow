from django.urls import path, re_path
from django.urls.conf import include
from .views import covidBlog, isiBlog

urlpatterns = [
    path('',covidBlog, name="covidBlog"),
    path('blog/<str:pk>', isiBlog, name="blog")
]