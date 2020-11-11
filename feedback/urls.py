from django.urls import include, path
from .views import feedback, savefeedback

urlpatterns = [
    path('', feedback, name='feedback'),
    path('savefeedback/', savefeedback),
]