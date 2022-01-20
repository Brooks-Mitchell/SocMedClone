"""SayIt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from speak.views import (home_view, 
    speak_detail_view, 
    speak_list_view, 
    speak_create_view, 
    speak_delete_view, 
    speak_action_view,
    )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view),
    path('speak/<int:speak_id>', speak_detail_view),
    path('speak', speak_list_view),
    path('create-speak', speak_create_view),
    path('api/speak/<int:speak_id>/delete', speak_delete_view),
    path('api/speak/action', speak_action_view),

    
]
