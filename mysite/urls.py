"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from django.shortcuts import redirect

from django.conf.urls.static import static 
from django.conf import settings 

from user import views

app_name = 'main'

def redirect_base(request):
    return redirect('user/')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user.urls', namespace='user')),
    path('accounts/', include('allauth.urls')),
    #path('',redirect_base)
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


"""/***
*  REFERENCES
*  Title: crash-course-CRM
*  Author: Dennis Ivy
*  Date: 05/02/2021
*  Code version: v17
*  URL: https://github.com/divanov11/crash-course-CRM/blob/part-17-Image-Upload/crm1_v17_image_upload/crm1/settings.py
*  Software License: <license software is released under>
*
***/"""