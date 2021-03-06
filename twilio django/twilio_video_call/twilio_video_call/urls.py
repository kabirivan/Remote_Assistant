"""twilio_video_call URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from ajax_conn import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.greeting, name='index'),
    path('chat_assis', views.chat, name='chat1'),
    path('chat_user', views.users, name='chat2'),
    path('photo', views.photo, name='photo'),
    path('login', views.login, name='login'),
    path('sing_up', views.login_screen, name='sing_up'),
    path('link', views.link, name='link'),
    path('prueba', views.prueba, name='prueba'),
]

urlpatterns += staticfiles_urlpatterns()