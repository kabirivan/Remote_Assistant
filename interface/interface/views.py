from django.http import HttpResponse
from django.template  import Template, Context

def greeting(request):

    index_ext = open("C:/Users/Jazmin Rodriguez/Dropbox/Chauchitas Jona/Remote_Assistant/interface/templates/index.html")
    tmp = Template(index_ext.read())
    index_ext.close()
    ctx = Context()
    doc = tmp.render(ctx)
    return HttpResponse(doc)


def chat(request):
    
    index_ext = open("C:/Users/Jazmin Rodriguez/Dropbox/Chauchitas Jona/Remote_Assistant/interface/templates/chat1.html")
    tmp = Template(index_ext.read())
    index_ext.close()
    ctx = Context()
    doc = tmp.render(ctx)
    return HttpResponse(doc)