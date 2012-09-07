from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext

def home(request):
    context = {}
    print settings.STATIC_ROOT 
    return render_to_response('index.html', RequestContext(request, context,))
