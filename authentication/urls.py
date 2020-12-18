from django.urls import path, re_path
from django.urls.conf import include
from .views import login, register, logging_out


urlpatterns = [
    path('',login, name="login"),
    path('register/', register, name="register"),
    path('logout/', logging_out, name="logout")
]


