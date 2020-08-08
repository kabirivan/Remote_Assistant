from django.contrib import admin
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from WebPages import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.greeting, name='index'),
    path('chat_assis', views.chat, name='chat1'),
    path('chatuser', views.users, name='chat2'),
    path('login', views.login, name='login'),
    path('sing_up', views.login_screen, name='sing_up'),
    path('link', views.link, name='link'),
    path('prueba', views.prueba, name='prueba'),
    path('send_sms', views.send_sms, name='sms'),
]

urlpatterns += staticfiles_urlpatterns()
