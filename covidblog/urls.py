
from django.urls import path, re_path
from django.urls.conf import include
from .views import covidBlog

urlpatterns = [
    path('',covidBlog, name="covidBlog")
]