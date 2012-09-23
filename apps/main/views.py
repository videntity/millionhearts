from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from apps.dashboard.views import patient_dashboard

def home(request):
    if not str(request.user)=="AnonymousUser":
        patient_profile = request.user.get_profile()
        return patient_dashboard(request, patient_profile.patient_id) 
    context = {}
    print settings.STATIC_ROOT 
    return render_to_response('index.html', RequestContext(request, context,))
