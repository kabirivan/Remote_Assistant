
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

load_dotenv()
twilio_account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
twilio_api_key_sid = os.environ.get('TWILIO_API_KEY_SID')
twilio_api_key_secret = os.environ.get('TWILIO_API_KEY_SECRET')
print(twilio_account_sid)
#app = django(__name__)

@csrf_exempt
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
    index_ext = loader.get_template('index.html')
    # a dictionary is necessary with loader template
    doc = index_ext.render({})
    return HttpResponse(doc)

@csrf_exempt
def chat(request):

    print("si entro CHAT ASSIST")
    chat_ext = loader.get_template('chat.html')
    ctx = {}
    doc = chat_ext.render(ctx)
    return HttpResponse(doc)

@csrf_exempt
def users(request):

    print("si entro CHAT USER")
    chatuser_ext = loader.get_template('chat_user.html')
    ctx = {}
    doc = chatuser_ext.render(ctx)
    return HttpResponse(doc)
