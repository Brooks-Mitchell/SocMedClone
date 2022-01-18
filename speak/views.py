from django.conf import settings
from django.http import Http404, HttpRequest, HttpResponse, JsonResponse, response
from django.shortcuts import render, redirect
import random
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .forms import SpeakForm
from .models import Speak
from .serializers import SpeakSerializer
from rest_framework.decorators import api_view, permission_classes, authentication_classes


def home_view(request, *args, **kwargs):
    return render(request, "pages/home.html", context={}, status=200)

@api_view(['POST'])
# @authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def speak_create_view(request, *args, **kwargs):
    serializer = SpeakSerializer(data=request.POST)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user) # serializer can take this here, vs the 3 lines of obj down in the form
        return Response(serializer.data, status=201)
    return Response({}, status=400)


@api_view(['GET'])
def speak_detail_view(request, speak_id, *args, **kwargs):
    qset = Speak.objects.filter(id=speak_id)
    if not qset.exists():
        return Response({}, status=404)
    obj = qset.first()
    serializer = SpeakSerializer(obj)
    return Response(serializer.data, status=200)

@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def speak_delete_view(request, speak_id, *args, **kwargs):
    qset = Speak.objects.filter(id=speak_id)
    if not qset.exists():
        return Response({}, status=404)
    qset = qset.filter(user=request.user)
    if not qset.exists():
        return Response({"message": "not allowed"}, status=401)
    obj = qset.first()
    obj.delete()
    return Response({"message": "deleted"}, status=200)


@api_view(['GET'])
def speak_list_view(request, *args, **kwargs):
    qset = Speak.objects.all()
    serializer = SpeakSerializer(qset, many=True)
    return Response(serializer.data, status=200)




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


def speak_list_view_pure_django(request, *args, **kwargs):
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

def speak_detail_view_pure_django(request, speak_id, *args, **kwargs):
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
