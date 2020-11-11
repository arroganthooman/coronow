from django.urls import include, path
from .views import feedback

urlpatterns = [
    path('', feedback, name='feedback'),
]