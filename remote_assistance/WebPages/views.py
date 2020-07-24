import os
from dotenv import load_dotenv
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant
from django.http import HttpResponse
from django.template  import Template, Context, loader
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
import json
from twilio.rest import Client
from django.shortcuts import render
from django.http import JsonResponse

load_dotenv()
twilio_account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
twilio_api_key_sid = os.environ.get('TWILIO_API_KEY_SID')
twilio_api_key_secret = os.environ.get('TWILIO_API_KEY_SECRET')
twilio_auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
twilio_phone_number = os.environ.get('TWILIO_PHONE_NUMBER')
# Create your views here.

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

@csrf_exempt            #In order to use POST method
def send_sms(request):
    print("ok sms")
    r_json = json.loads(request.body)
    number = r_json['phoneNumber']
    url = r_json['url']
    client = Client(twilio_account_sid, twilio_auth_token)
    client.messages.create(
                from_=twilio_phone_number,
                to=number,
                body='Link para tener una llamada con el asesor:' + url)
    return JsonResponse({'response': 'ok', 'errorMsg':'errorMsg'})

@csrf_exempt 
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
def link(request):
    print("You are in the function link")
    return HttpResponse()