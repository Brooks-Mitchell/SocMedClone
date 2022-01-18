from django.conf import settings
from django.http import Http404, HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
import random

from .forms import SpeakForm
from .models import Speak
from .serializers import SpeakSerializer


def home_view(request, *args, **kwargs):
    return render(request, "pages/home.html", context={}, status=200)


def speak_create_view(request, *args, **kwargs):
    serializer = SpeakSerializer(data=request.POST or None)
    if serializer.is_valid():
        obj = serializer.save(user=request.user) # serializer can take this here, vs the 3 lines of obj down in the form
        return JsonResponse(serializer.data, status=201)
    return JsonResponse({}, status=400)

def speak_create_view_pure_django(request, *args, **kwargs):
    user = request.user

    if not request.user.is_authenticated:
        user = None
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # work-around for deprecated "request.is_ajax"
            return JsonResponse({}, status=401)
        return redirect(settings.LOGIN_URL)

    # SpeakForm class can be initialized with data or not
    form = SpeakForm(request.POST or None)

    next_url = request.POST.get("next") or None
    
    # if form is valid then it will be saved to DB
    if form.is_valid():
        obj = form.save(commit=False) # per Stackoverflow "useful when you get most of your model data from a form, 
        # but you need to populate some null=False fields with non-form data.Saving with commit=False gets you a model object, then you can add your extra data and save it."
        
        obj.user = user

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # work-around for deprecated "request.is_ajax"
            return JsonResponse(obj.serialize(), status=201) # 201 == created items

        if next_url != None:
            return redirect(next_url)
        form = SpeakForm() # re-initialize a new black form
    if form.errors:
        if request.is_ajax():
            return JsonResponse(form.errors, status=400)
    return render(request, 'components/form.html', context={"form": form})


def speak_list_view(request, *args, **kwargs):
    """
    REST API VIEW
    Consume by JavaSctipt
    Return json data
    """
    qset = Speak.objects.all()
    speak_list = [x.serialize() for x in qset]
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
