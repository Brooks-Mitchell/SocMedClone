from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
import random

from .forms import SpeakForm
from .models import Speak

def home_view(request, *args, **kwargs):
    return render(request, "pages/home.html", context={}, status=200)

def speak_create_view(request, *args, **kwargs):

    # SpeakForm class can be initialized with data or not
    form = SpeakForm(request.POST or None)
    
    # if form is valid then it will be saved to DB
    if form.is_valid():
        obj = form.save(commit=False) # per Stackoverflow "useful when you get most of your model data from a form, 
        # but you need to populate some null=False fields with non-form data.Saving with commit=False gets you a model object, then you can add your extra data and save it."

        obj.save()
        form = SpeakForm() # re-initialize a new black form
    return render(request, 'components/form.html', context={"form": form})


def speak_list_view(request, *args, **kwargs):
    """
    REST API VIEW
    Consume by JavaSctipt
    Return json data
    """
    qset = Speak.objects.all()
    speak_list = [{"id": x.id, "content": x.content, "likes": random.randint(0, 1000)} for x in qset]
    data = {
        "isUser": False,
        "response": speak_list
    }
    return JsonResponse(data)

def speak_detail_view(request, speak_id, *args, **kwargs):
    """
    REST API VIEW
    Consume by JavaSctipt
    Return json data
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
