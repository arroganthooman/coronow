from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Feedback
from .forms import Form_Feedback
import json
from django.core import serializers

# Create your views here.
def feedback(request):
    response = {'field' : Form_Feedback}
    return render(request, 'feedback.html', response)

def savefeedback(request):
    form = Form_Feedback(request.POST or None)
    if (form.is_valid and request.method == 'POST'):
        post_nama = request.POST.get('nama')
        post_email = request.POST.get('email')
        post_isi = request.POST.get('isi')
        data = {}

        feedback = Feedback(nama=post_nama, email=post_email, isi=post_isi)
        feedback.save()

        data['nama'] = feedback.nama
        data['email'] = feedback.email
        data['isi'] = feedback.isi

        return JsonResponse(data, safe=False)
    else:
        data = {'gaada' : 'gabisa'}
        return JsonResponse(data, safe=False)

@login_required(login_url='/login')
def listfeedback(request):
    return render(request, 'listfeedback.html')

def perantara(request):
    return render(request, 'listfeedback.html')