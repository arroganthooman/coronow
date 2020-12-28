from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Feedback
from .forms import Form_Feedback
import json

# Create your views here.
def feedback(request):
    response = {'field' : Form_Feedback}
    return render(request, 'feedback.html', response)

def savefeedback(request):
    form = Form_Feedback(request.POST or None)
    if (form.is_valid and request.method == 'POST'):
        form.save()
        return HttpResponseRedirect('/feedback/')
    else:
        return HttpResponseRedirect('/feedback/')



@login_required(login_url='/login')
def listfeedback(request):
    response = {'feedbacks' : Feedback.objects.all(),
                'field' : Form_Feedback}
    return render(request, 'listfeedback.html', response)