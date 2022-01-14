from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse

from .models import Speak

def home_view(request, *args, **kwargs):
    return render(request, "pages/home.html", context={}, status=200)

def speak_detail_view(request, speak_id, *args, **kwargs):
    """
    REST API VIEW
    Consume by JavaSctipt
    Rrtuern json data
    """
    data = {
        "id" : speak_id,
       
        # "image_path" : obj.image.url
    }
    status = 200
    try:
        obj = Speak.objects.get(id=speak_id)
        data['content'] = obj.content
    except:
        data['message'] = "Not found"
        status = 404
    return JsonResponse(data, status=status)