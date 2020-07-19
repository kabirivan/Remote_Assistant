import os
from dotenv import load_dotenv
#from django import request, abort
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant
from django.http import HttpResponse
from django.template  import Template, Context, loader
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
import json
from twilio.twiml.voice_response import Dial, VoiceResponse, Gather
from twilio.rest import Client
from django.shortcuts import render
from django.http import JsonResponse
from .models import Friend

load_dotenv()
twilio_account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
twilio_api_key_sid = os.environ.get('TWILIO_API_KEY_SID')
twilio_api_key_secret = os.environ.get('TWILIO_API_KEY_SECRET')

# Create your views here.
def create_post(request):
    posts = Friend.objects.all()
    response_data = {}

    if request.POST.get('action') == 'post':
        title = request.POST.get('title')
        description = request.POST.get('description')

        response_data['title'] = title
        response_data['description'] = description

        Friend.objects.create(
            title = title,
            description = description,
            )
        return JsonResponse(response_data)

    return render(request, 'create_post.html', {'posts':posts}) 

@csrf_exempt            #In order to use POST method
def login(request):
    print("ok")
    r_json = json.loads(request.body)
    username = r_json['username']
    print(username)
    
    token = AccessToken(twilio_account_sid, twilio_api_key_sid,
                        twilio_api_key_secret, identity=username)
    token.add_grant(VideoGrant(room='My Room'))

    return JsonResponse({'token': token.to_jwt().decode(), 'errorMsg':'errorMsg'})

def greeting(request):
    index_ext = loader.get_template('html/index.html')
    # a dictionary is necessary with loader template
    doc = index_ext.render({})
    return HttpResponse(doc)
    
@csrf_exempt
def login_screen(request):
    index_ext = loader.get_template('html/login.html')
    # a dictionary is necessary with loader template
    doc = index_ext.render({})
    return HttpResponse(doc)

def prueba(request):
    index_ext = loader.get_template('html/prueba.html')
    # a dictionary is necessary with loader template
    doc = index_ext.render({})
    return HttpResponse(doc)

@csrf_exempt
def chat(request):

    chat_ext = loader.get_template('html/chat.html')
    ctx = {}
    doc = chat_ext.render(ctx)
    return HttpResponse(doc)

@csrf_exempt
def users(request):
    chatuser_ext = loader.get_template('html/chat_user.html')
    ctx = {}
    doc = chatuser_ext.render(ctx)
    return HttpResponse(doc)

@csrf_exempt
def photo(request):
    if request.is_ajax():
        message = "Yes, AJAX!"
    else:
        message = "Not Ajax"
    print(message)
    return HttpResponse(message)

@csrf_exempt
def link(request):
    print("You are in the function link")
    return HttpResponse()

