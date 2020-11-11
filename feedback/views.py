from django.shortcuts import render
from .models import Feedback
from .forms import Form_Feedback

# Create your views here.
def feedback(request):
    response = {'field' : Form_Feedback}
    return render(request, 'feedback.html', response)