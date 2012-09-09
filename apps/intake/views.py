#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
import re
from django.contrib import messages
from django.db.utils import IntegrityError
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from forms import *
from models import PatientProfile, Visit, Locator
from django.core.urlresolvers import reverse
from django.core import serializers
from utils import create_patient_id
import datetime
from ..accounts.models import UserProfile
from ..accounts.decorators import access_required
from ..rendersigs.views import url_model_map
import formcopytext
from django.forms.models import model_to_dict
from ..utils import build_pretty_data_view




@login_required
@access_required("tester")
def search_by_name(request):
    search_title = "Intake Find Patient"
    link_ref = "/patient-navigation/patient/"
    if request.method == 'POST':
    
        form = PatientSearchForm(request.POST)

        if form.is_valid():  
            data = form.cleaned_data
            first_name = data['first_name']
            last_name = data['last_name']
            
            #so do a filter
            pps = PatientProfile.objects.all()
            #print first_name, last_name
            if last_name:
                pps = pps.filter(last_name__icontains=last_name)
            
            if first_name:
                pps = pps.filter(first_name__icontains=first_name)

            return render_to_response('intake/search-by-name.html', 
                             {'form': PatientSearchForm(),
                              'results': pps,
                              'result_count': pps.count(),
                              'first_name' : first_name,
                              'last_name' : last_name,
                              'link_ref'  : link_ref,
                              'search_title': search_title,
                             },
                             context_instance = RequestContext(request))
            
        #form is invalid    
        return render_to_response('intake/search-by-name.html', 
                             {'form': form,
                              'link_ref' : link_ref,
                              'search_title': search_title,
                              },
                              context_instance = RequestContext(request))
    
    #request is a GET (not a POST)    
    return render_to_response('intake/search-by-name.html', 
                             {'form': PatientSearchForm(),
                              'search' : "false",
                              'link_ref' :link_ref,
                              'search_title':search_title,
                              },
                            context_instance = RequestContext(request))




@login_required
@access_required("tester")
def search_by_name_generic(request, template_name='intake/search-by-name.html', link_ref="/testing/", search_title="Intake Find Patient"):
    if request.method == 'POST':
    
        form = PatientSearchForm(request.POST)
        
        if form.is_valid():  
            data = form.cleaned_data
            first_name = data['first_name']
            last_name = data['last_name']
            
            #so do a filter
            pps = PatientProfile.objects.all()
            #print first_name, last_name
            if last_name:
                pps = pps.filter(last_name__icontains=last_name)
            
            if first_name:
                pps = pps.filter(first_name__icontains=first_name)

            return render_to_response(template_name, 
                             {'form': PatientSearchForm(),
                              'results': pps,
                              'result_count': pps.count(),
                              'first_name' : first_name,
                              'last_name' : last_name,
                              'link_ref' : link_ref,
                              'search_title': search_title,
                             },
                             context_instance = RequestContext(request))
            
        #form is invalid    
        return render_to_response(template_name, 
                             {'form': form,
                              'link_ref': link_ref,
                              'search_title': search_title,
                              },
                              context_instance = RequestContext(request))
    
    #request is a GET (not a POST)    
    return render_to_response(template_name, 
                             {'form': PatientSearchForm(),
                              'search' : "false",
                              'link_ref': link_ref,
                              'search_title': search_title,
                              },
                            context_instance = RequestContext(request))





@login_required
@access_required("tester")
def search_by_ssn(request):
    if request.method == 'POST':
    
        form = Last4SocialSearchForm(request.POST)
        
        if form.is_valid():  
            data = form.cleaned_data
            last_4_ssn = data['last_4_ssn']
            
            #so do a filter
            pps = PatientProfile.objects.all()
            if last_4_ssn:
                pps = pps.filter(last_4_ssn__iexact=last_4_ssn)
            
            return render_to_response('intake/search-by-ssn.html', 
                             {'form': Last4SocialSearchForm(),
                              'results': pps,
                              'result_count': pps.count(),
                              'last_4_ssn' : last_4_ssn,
                              'link_ref': "/patient-navigation/patient/",
                            },
                            context_instance = RequestContext(request))
            
        #form is invalid    
        return render_to_response('intake/search-by-ssn.html', 
                             {'form': form},
                              context_instance = RequestContext(request))
    
    #request is a GET (not a POST)    
    return render_to_response('intake/search-by-ssn.html', 
                             {'form': Last4SocialSearchForm(),
                              'search' : "false",
                             },
                              context_instance = RequestContext(request))


@login_required
@access_required("tester")
def patient_lookup(request, pat_id=None):
    p = get_object_or_404(PatientProfile, patient_id=pat_id)
    # return HttpResponseRedirect(reverse('client_home', args=(p.patient_id,)))
    return HttpResponseRedirect(reverse('/testing/'+pat_id, args=(p.patient_id,)))


@login_required
@access_required("tester")
def locator(request, pat_id):
    pp = get_object_or_404(PatientProfile, patient_id=pat_id)
    up = get_object_or_404(UserProfile, user=request.user)    
        
    if request.method == 'POST':
        try:
            el=Locator.objects.get(patient=pp)
            form = LocatorForm(request.POST, request.FILES, instance=el)
            
        except Locator.DoesNotExist:
            form = LocatorForm(request.POST, request.FILES)
            
        if form.is_valid():
            newlocator=form.save(commit=False)
            newlocator.worker=request.user
            newlocator.patient=pp
            newlocator.save()
                
            # return HttpResponseRedirect(reverse('client_home',args=(pp.patient_id,)))
            messages.success(request, "Successfully created/updated a Locator")
            return HttpResponseRedirect(reverse('patient_dashboard',args=(pp.patient_id,)))

        else:
            return render_to_response('intake/locator.html',
                              RequestContext(request,
                                    {'form': form,
                                    'toptext':formcopytext.locator_form_top,
                                    'bottomtext':formcopytext.locator_form_bottom,
                                    }))
    
    try:
        d=Locator.objects.get(patient=pp)
        form=LocatorForm(instance=d)
    
    except Locator.DoesNotExist:
        form=LocatorForm()

    
    return render_to_response('intake/locator.html',
                              RequestContext(request,
                                    {'form': form,
                                    'toptext':formcopytext.locator_form_top,
                                    'bottomtext':formcopytext.locator_form_bottom,
                                    }))



@login_required
@access_required("tester")
def view_locator(request, pat_id):
    signature_url_prefix=url_model_map[Locator]

    # print "Patient_ID:"+pat_id
    pp = get_object_or_404(PatientProfile, patient_id=pat_id)

    # print "patient profile:"
    # print pp
    # print "Locator:"

    locator = get_object_or_404(Locator, patient=pp)

    # print locator

    lf=LocatorForm(instance=locator)
    data=build_pretty_data_view(form_instance=lf, model_object=locator,
                            exclude=('worker_signature', 'patient_signature'),
                            append=('worker','patient'))
    
    
    worker=locator.worker.get_profile()
    worker_signature="%s/worker/%s" % (signature_url_prefix, pat_id)
    patient_signature="%s/patient/%s" % (signature_url_prefix, pat_id)
    modeldict=model_to_dict(locator, exclude=['id', 'worker',
                                        'patient','worker_signature',
                                        'patient_signature'])
    
    return render_to_response('intake/view-locator.html',
                              RequestContext(request,
                                             {'pp':pp,
                                              'data':data,
                                              'worker': worker,
                                              'modeldict':  modeldict,
                                              'photo': locator.photo,
                                              'name':   "Locator",
                                              'pat_id':  pat_id,
                                              'toptext': formcopytext.locator_form_top,
                                              'bottomtext':formcopytext.locator_form_bottom,
                                              'worker_signature_url': worker_signature,
                                              'patient_signature_url': patient_signature
                                              }))



@login_required
@access_required("tester")
def inprocess_list(request):
    ipp=PatientProfile.objects.filter(creation_date=datetime.date.today())
    return render_to_response('intake/in-process.html', {'ipp':ipp},
                              RequestContext(request))



@login_required
@access_required("tester")
def quick_intake(request):
    
    up = get_object_or_404(UserProfile, user=request.user)
    
    if request.method == 'POST':
        
        form = QuickIntakeForm(request.POST)
        
        if form.is_valid():  
            data = form.cleaned_data
            newpatient=form.save(commit=False)
            newpatient.worker=request.user
            newpatient.location=up.location
            newpatient.save()
            messages.success(request, "Successfully added a new member")
            if newpatient.health_insurance_provider in ("NONE", "SELF", "UNKNOWN"):
                messages.info(request, "This member may be eligible for public health assistance such as Medicaid.")
                                                         
            return HttpResponseRedirect(reverse('patient_dashboard',
                                                args=(newpatient.patient_id,)))
                
        else:
            messages.error(request, "There are errors on the form.")
            return render_to_response('intake/intake.html',
                              RequestContext(request,
                                             {'form': form,}))
    else:
        return render_to_response('intake/intake.html', 
                             {'form': QuickIntakeForm()},
                              context_instance = RequestContext(request))
    
    
@login_required
@access_required("tester")
def quick_referral_intake(request):
    
    up = get_object_or_404(UserProfile, user=request.user)
    
    if request.method == 'POST':
        
        form = QuickReferralIntakeForm(request.POST)
        
        if form.is_valid():  
            data = form.cleaned_data
            newpatient=form.save(commit=False)
            newpatient.worker=request.user
            newpatient.location=up.location
            newpatient.save()
            messages.success(request, "Successfully added a new member")
            if newpatient.health_insurance_provider in ("NONE", "SELF", "UNKNOWN"):
                messages.info(request, "This member may be eligible for public health assistance such as Medicaid.")
                                                         
            return HttpResponseRedirect(reverse('patient_dashboard',
                                                args=(newpatient.patient_id,)))
                
        else:
            messages.error(request, "There are errors on the form.")
            return render_to_response('intake/intake.html',
                              RequestContext(request,
                                             {'form': form,}))
    else:
        return render_to_response('intake/intake.html', 
                             {'form': QuickReferralIntakeForm()},
                              context_instance = RequestContext(request))



@login_required
@access_required("tester")
def initial_intake(request):
    
    up = get_object_or_404(UserProfile, user=request.user)
    
    if request.method == 'POST':

        form = IntakeForm(request.POST)
        
        if form.is_valid():  
            data = form.cleaned_data
            newpatient=form.save(commit=False)
            newpatient.worker=request.user
            newpatient.location=up.location
            newpatient.save()
            messages.success(request, "Successfully added a new member")
            if newpatient.health_insurance_provider in ("NONE", "SELF", "UNKNOWN"):
                messages.info(request, "This member may be eligible for public health assistance such as Medicaid.")
                                                         
            return HttpResponseRedirect(reverse('patient_dashboard',
                                                args=(newpatient.patient_id,)))
                
        else:
            messages.error(request, "There are errors on the form.")
            return render_to_response('intake/intake.html',
                              RequestContext(request,
                                             {'form': form,}))
    else:
        return render_to_response('intake/intake.html', 
                             {'form': IntakeForm()},
                              context_instance = RequestContext(request))
        




@login_required
@access_required("tester")
def markvisit(request, pat_id):
    
    pp = get_object_or_404(PatientProfile, patient_id=pat_id)
    
    if request.method == 'POST':

        form = MarkVisitForm(request.POST, instance=pp)
        
        if form.is_valid():  
            visit = form.save(commit=False)
            visit.date = datetime.date.today()
            visit.worker = request.user
            visit.save()
            messages.success(request, "Successfully marked as visiting today.")
            
            return HttpResponseRedirect(reverse('patient_dashboard',
                                                args=(pp.patient_id,)))
                
        else:
            messages.error(request, "Please fix the errors on the form.")
            return render_to_response('intake/mark-visit.html',
                              RequestContext(request,
                                             {'form': form,}))
    else:
        return render_to_response('intake/mark-visit.html', 
                             {'form': MarkVisitForm()},
                              context_instance = RequestContext(request))




@login_required
@access_required("tester")
def edit_intake(request, pat_id):
    
    pp = get_object_or_404(PatientProfile, patient_id=pat_id)
    
    if request.method == 'POST':

        form = EditIntakeForm(request.POST, instance=pp)
        
        if form.is_valid():  
            form.save()
            messages.success(request, "Successfully updated an existing member.")
            
            if pp.health_insurance_provider in ("NONE", "SELF", "UNKNOWN"):
                messages.info(request, "This member may be eligible for public health assistance such as Medicaid.")
            return HttpResponseRedirect(reverse('patient_dashboard',
                                                args=(pp.patient_id,)))
                
        else:
            messages.error(request, "Please fix the errors on the form.")
            return render_to_response('intake/edit-intake.html',
                              RequestContext(request,
                                             {'form': form,}))
    else:
        return render_to_response('intake/edit-intake.html', 
                             {'form': EditIntakeForm(instance=pp)},
                              context_instance = RequestContext(request))
