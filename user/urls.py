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
from django.urls import path
from django.conf.urls import include
from django.views.generic import TemplateView

from . import views

app_name = 'user'

urlpatterns = [
    # Homepage (and logging out, which redirects to homepage)
    path('', views.home, name='home'),
    path('logout', views.logout_view, name='logout'),

    # The User Homepage - essentially the Main Menu
    path('user/', views.get_user, name='main'),

    # Updating the current user's bio (fakeurl is just used to redirect back to the profile after profile creation)
    path('create/', views.getProfileForm, name='newprofile'),
    path('fakeurl/', views.get_profile, name='newprofileform'),
    path('fakeurl2/',views.clear_filter, name='clearfilter'),

    # View other profiles (by id, all of them, or via the roommate searching feature)
    path('<int:prof_id>/', views.getDetail, name='details'),
    #path('list/', views.ProfileIndexView.as_view(), name='profilelist'),
    path('search/', views.profileSearch, name='search'),

    # Submits action of swiping right or left
    path('action/', views.action, name='action'),

    # Matching URLs - viewing matches and sending messages to users
    path('matches/', views.get_matches, name='matches'),
    path('chat/<str:uname>/', views.startMessage, name='chat'),
    path('chat/<str:uname>/send', views.sendMessage, name='sendmessage'),
    path('chat/<str:uname>/<int:prev_msg_id>/send', views.replyMessage, name='replymessage'),
    path('inbox/', views.get_inbox, name='inbox'),
    path('viewMessage/<int:msg_id>', views.viewMessage, name='viewmessage'),
    path('updateMapboxAddress/<int:msg_id>', views.updateMapboxAddress, name='updatemapboxaddress')
]
