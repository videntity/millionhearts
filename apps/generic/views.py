#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu


from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from models import FormName,ExtraFormContent
from ..utils import build_pretty_data_view
from ..intake.models import PatientProfile
from datetime import datetime, timedelta, date

def generic_view2(request, pat_id, data, name="No Name",
                 template="generic/generic-view.html",
                 signature_url_prefix="rendersigs",
                 toptext="", bottomtext=""):


    worker_signature="%s/worker/%s" % (signature_url_prefix, pat_id)
    patient_signature="%s/patient/%s" % (signature_url_prefix, pat_id)

    pp=PatientProfile.objects.get(patient_id=pat_id)

    return render_to_response(template,
                              RequestContext(request,
                                             {'name': name,
                                              'pat_id': pat_id,
                                              'toptext':toptext,
                                              'pp':pp,
                                              'data': data,
                                              'bottomtext':bottomtext,
                                              'worker_signature_url': worker_signature,
                                              'patient_signature_url': patient_signature
                                              }))



def generic_view(request, pat_id, basemodel, name="No Name",
                 template="generic/generic-view.html",
                 signature_url_prefix="rendersigs",
                 toptext="", bottomtext=""):

    pp=PatientProfile.objects.get(patient_id=pat_id)
    model=basemodel.objects.filter(patient=pp).latest()
    worker=model.worker.get_profile()
    worker_signature="%s/worker/%s" % (signature_url_prefix, pat_id)
    patient_signature="%s/patient/%s" % (signature_url_prefix, pat_id)
    
    
    
    model=model_to_dict(model, exclude=['id', 'worker',
                                        'patient','worker_signature',
                                        'patient_signature'])
    return render_to_response(template,
                              RequestContext(request,
                                             {'pp':pp,
                                              'worker': worker,
                                              'model': model,
                                              'name': name,
                                              'pat_id': pat_id,
                                              'toptext':toptext,
                                              'bottomtext':bottomtext,
                                              'worker_signature_url': worker_signature,
                                              'patient_signature_url': patient_signature
                                              }))



def generic_form_view(request, pat_id, baseform,
                  basemodel,
                  name="No Name", template="generic/generic-form.html",
                  success_redirect='client_home',
                  submit_button_text='OK', toptext="",
                  bottomtext="",
                  success_message=None,
                  form_dict={},
                  formname="",
                  create_new_days=None):


    patient_id = pat_id[0:8]

    if request.method == 'POST':

        #print "POST:generic_form_view"
        #print "patient_id:"+patient_id

        pat = PatientProfile.objects.get(patient_id=patient_id)

        try:
            instance = basemodel.objects.filter(patient=pat, worker=request.user).latest()

                
        except(basemodel.DoesNotExist):
            instance = basemodel(patient=pat, worker=request.user)

        form = baseform(request.POST, instance=instance)


        if form.is_valid():
            form.save()
            if success_message is not None:
                messages.success(request, success_message)
                print success_redirect

            return redirect(success_redirect, patient_id)

        #the form was invalid
        return render(request, template, locals())

    else:
        #if a get
        try:
            
            d = basemodel.objects.filter(patient__patient_id=patient_id).latest()
            if create_new_days:
                retake_elg_date = d.creation_date + timedelta(days = create_new_days)
                #this person is now allowed to retake this test so display like new
                if retake_elg_date <= date.today():
                    return render_to_response(template,
                                 {'name': name,
                                  'submit_button_text': submit_button_text,
                                  'form': baseform(initial=form_dict),
                                  'toptext': toptext,
                                  'bottomtext': bottomtext,
                                  'patient_id': patient_id,
                                  'formname': formname},
                                  context_instance = RequestContext(request))
            
            #just edit the latest
            form=baseform(instance=d)
            return render_to_response(template,
                             {'name': name,
                              'submit_button_text': submit_button_text,
                              'form': form,
                              'toptext': toptext,
                              'bottomtext': bottomtext,
                              'patient_id': patient_id,
                              'formname': formname},
                              context_instance = RequestContext(request))
        except(basemodel.DoesNotExist):
            return render_to_response(template,
                             {'name': name,
                              'submit_button_text': submit_button_text,
                              'form': baseform(initial=form_dict),
                              'toptext': toptext,
                              'bottomtext': bottomtext,
                              'patient_id': patient_id,
                              'formname': formname},
                              context_instance = RequestContext(request))
