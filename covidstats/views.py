from django.http import request, JsonResponse
from django.http.response import Http404
from django.shortcuts import render
from .models import KasusUpdated, KasusProvinsi

# Create your views here.
def covidstats(request):
    if request.method == "POST":
        try:
            if request.POST["post_type"] == "POST_PROV":
                provinsi = KasusProvinsi.objects.find(nama_provinsi = request.POST["prov"].upper())[0]
                return JsonResponse(provinsi.data_json, safe=False)
        except KasusProvinsi.DoesNotExist as e:
            return JsonResponse(
                status = 404, 
                data = {'not-found': True, 'msg' : str(e)}
            )

    context = {}
    if KasusUpdated.objects.exists():
        context["kasus_updated"] = KasusUpdated.objects.all()[0]

    return render(request, "covidstats/covidstats.html", context=context)