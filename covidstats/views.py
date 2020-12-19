from django.http import request, JsonResponse
from django.http.response import Http404
from django.shortcuts import render
from .models import KasusUpdated, KasusProvinsi

# Create your views here.
def covidstats(request):
    if request.method == "POST":
        try:
            if request.POST["post_type"] == "POST_PROV":
                if request.user.is_authenticated:
                    provinsi = KasusProvinsi.objects.get(nama_provinsi = request.POST["prov"].upper())
                    return JsonResponse(provinsi.data_json[-400:], safe=False)
                else:
                    provinsi = KasusProvinsi.objects.get(nama_provinsi = 'INDONESIA')
                    return JsonResponse(provinsi.data_json[-400:], safe=False)
        except KasusProvinsi.DoesNotExist as e:
            return JsonResponse(
                status = 404, 
                data = {'fail': True, 'reason': 'not-found', 'msg' : str(e)}
            )

    context = {}
    if KasusUpdated.objects.exists():
        context["kasus_updated"] = KasusUpdated.objects.all()[0]
    context['is_auth'] = request.user.is_authenticated

    return render(request, "covidstats/covidstats.html", context=context)