#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.conf import settings
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from ..intake.models import PatientProfile
from models import Referral, Linkage, LinkageFollowUp
from ..utils import build_pretty_data_view
from ..accounts.decorators import access_required
from forms import *
from ..intake.forms import PatientSearchForm
from ..rendersigs.views import url_model_map


@login_required
@access_required("tester")
def services_search_by_name(request):
    
    if request.method == 'POST':
        form = PatientSearchForm(request.POST)
        
        if form.is_valid():  
            data = form.cleaned_data
            first_name = data['first_name']
            last_name = data['last_name']
            
            #so do a filter
            pps = PatientProfile.objects.all()
            if last_name:
                pps = pps.filter(last_name__icontains=last_name)
            
            if first_name:
                pps = pps.filter(first_name__icontains=first_name)
                
            #add messages about our results.
            result_count = pps.count()
                    
            if (result_count == 0):
                result_string = "%s results found." % (result_count)
            elif (result_count == 1):
                result_string = "%s result found." % (result_count)
            else:
                result_string = "%s results found" % (result_count)
            return render_to_response('services/search-by-name.html', 
                             {'form': PatientSearchForm(),
                              'results': pps,
                              'fst_name': first_name,
                              'lst_name': last_name,
                              'result_count': result_string},
                              context_instance = RequestContext(request))
            
        #form is invalid    
        else:
            return render_to_response('services/search-by-name.html', 
                             {'form': form},
                              context_instance = RequestContext(request))

    #request is a GET (not a POST)    
    return render_to_response('services/search-by-name.html', 
                         {'form': PatientSearchForm(),
                          'search':"false",
                          },
                            context_instance = RequestContext(request))


@login_required
@access_required("tester")
def browse_past_referrals(request, pat_id):
    
    p=get_object_or_404(PatientProfile, patient_id=pat_id)
    referrals =  Referral.objects.filter(patient=p)   
    
    return render_to_response('services/referral/browse-past-referrals.html', 
                             {'referrals': referrals,},
                             context_instance = RequestContext(request))


@login_required
@access_required("tester")
def browse_past_linkages(request, pat_id):
    
    p=get_object_or_404(PatientProfile, patient_id=pat_id)
    linkages =  Linkage.objects.filter(patient=p)   
    
    return render_to_response('services/linkage/browse-past-linkages.html', 
                             {'linkages': linkages,},
                             context_instance = RequestContext(request))




@login_required
@access_required("tester")
def linkage_followup_browse(request, pk):
    linkage =  Linkage.objects.get(pk=pk)
    linkage_follow_ups = LinkageFollowUp.objects.filter(linkage=linkage)
    
    return render_to_response('services/linkage/browse-followup-linkages.html', 
                             {'linkage': linkage,
                                'linkage_follow_ups': linkage_follow_ups,},
                             context_instance = RequestContext(request))

@login_required
@access_required("tester")
def linkage_followup_view(request, pk):
    
    linkage_follow_up = get_object_or_404(LinkageFollowUp, pk=pk)
   
    lf=LinkageFollowUpForm(instance=linkage_follow_up)
    data=build_pretty_data_view(form_instance = lf,
                            model_object = linkage_follow_up,
                            append=('worker','linkage'))
        
    return render_to_response('services/linkage/followup-view.html',
                              RequestContext(request,
                                             {'pp':linkage_follow_up.linkage.patient,
                                              'worker':linkage_follow_up.worker,
                                              'pk':pk,
                                              'data':data,
                                              'name': "Linkage Follow Up",
                                              'toptext': "",
                                              'bottomtext':"",
                                              }))
    
    
    
    
    
    

@login_required
@access_required("tester")
def linkage_followup_create(request, pk):
    linkage = get_object_or_404(Linkage, pk=pk)  
        
    if request.method == 'POST':
        form = LinkageFollowUpForm(request.POST)           
        if form.is_valid():
            newfollowup=form.save(commit=False)
            newfollowup.linkage=linkage
            newfollowup.worker=request.user
            newfollowup.save()
            messages.success(request,'New linkage followup created successfully.')    
            return HttpResponseRedirect(reverse('patient_dashboard',
                                                args=(linkage.patient.patient_id,)))
        else:
            return render_to_response('services/linkage/followup-create.html',
                              RequestContext(request,
                                    {'form': form,
                                     'linkage':linkage,
                                    'toptext':'toptext',
                                    'bottomtext':'bottomtext',
                                    }))

    return render_to_response('services/linkage/followup-create.html',
                              RequestContext(request,
                                    {'form': LinkageFollowUpForm(),
                                      'linkage':linkage,
                                    'toptext':'toptext',
                                    'bottomtext':'bottomtext',
                                    }))

@login_required
@access_required("tester")    
def referral_view(request, pk):    
    signature_url_prefix=url_model_map[Referral]
    referral = get_object_or_404(Referral, pk=pk)
    rf=ReferralForm(instance=referral)
    data=build_pretty_data_view(form_instance=rf, model_object=referral,
                            exclude=('worker_signature', 'patient_signature'),
                            append=('worker','patient'))
    
    worker_signature="%s/worker/%s/%s" % (signature_url_prefix,
                                          referral.worker, pk)
    patient_signature="%s/patient/%s/%s" % (signature_url_prefix,
                                            referral.patient.patient_id, pk)
    
    return render_to_response('services/view.html',
                              RequestContext(request,
                                             {'pp':referral.patient,
                                              'worker':referral.worker,
                                              'pk':pk,
                                              'data':data,
                                              'name':   "Referral View",
                                              'toptext': "",
                                              'bottomtext':"",
                                              'worker_signature_url': worker_signature,
                                              'patient_signature_url': patient_signature
                                              }))
    



@login_required
@access_required("tester")    
def linkage_view(request, pk):    
    signature_url_prefix=url_model_map[Linkage]
    
    linkage = get_object_or_404(Linkage, pk=pk)
   
    lf=LinkageForm(instance=linkage)
    data=build_pretty_data_view(form_instance=lf, model_object=linkage,
                            exclude=('worker_signature', 'patient_signature'),
                            append=('worker','patient'))
    
    worker_signature="%s/worker/%s/%s" % (signature_url_prefix,
                                       linkage.worker, pk)
    patient_signature="%s/patient/%s/%s" % (signature_url_prefix,
                                         linkage.patient.patient_id,
                                         pk)
    
    return render_to_response('services/view.html',
                              RequestContext(request,
                                             {'pp':linkage.patient,
                                              'worker':linkage.worker,
                                              'pk':pk,
                                              'data':data,
                                              'name':   "Linkage View",
                                              'toptext': "",
                                              'bottomtext':"",
                                              'worker_signature_url': worker_signature,
                                              'patient_signature_url': patient_signature
                                              }))
    





@login_required
@access_required("tester")
def referral_create(request, pat_id):
    pp = get_object_or_404(PatientProfile, patient_id=pat_id)  
        
    if request.method == 'POST':
        form = ReferralForm(request.POST)           
        if form.is_valid():
            newreferral=form.save(commit=False)
            newreferral.patient=pp
            newreferral.worker=request.user
            newreferral.save()
            messages.success(request,'New referral created successfully.')    
            return HttpResponseRedirect(reverse('patient_dashboard',
                                                args=(pat_id,)))
        else:
            return render_to_response('services/referral/create.html',
                              RequestContext(request,
                                    {'form': form,
                                    'toptext':'toptext',
                                    'bottomtext':'bottomtext',
                                    }))

    return render_to_response('services/referral/create.html',
                              RequestContext(request,
                                    {'form': ReferralForm(),
                                    'toptext':'toptext',
                                    'bottomtext':'bottomtext',
                                    }))
    
    
@login_required
@access_required("tester")
def linkage_create(request, pat_id):
    pp = get_object_or_404(PatientProfile, patient_id=pat_id)  
        
    if request.method == 'POST':
        form = LinkageForm(request.POST)           
        if form.is_valid():
            newlinkage=form.save(commit=False)
            newlinkage.patient=pp
            newlinkage.worker=request.user
            newlinkage.save()
            messages.success(request,'New linkage created successfully.')    
            return HttpResponseRedirect(reverse('patient_dashboard',
                                                args=(pat_id,)))
        else:
            messages.error(request,'There were errors on the form. Please correct the errors below.') 
            return render_to_response('services/linkage/create.html',
                              RequestContext(request,
                                    {'form': form,
                                    'toptext':'toptext',
                                    'bottomtext':'bottomtext',
                                    }))

    return render_to_response('services/linkage/create.html',
                              RequestContext(request,
                                    {'form': LinkageForm(),
                                    'toptext':'toptext',
                                    'bottomtext':'bottomtext',
                                    }))
    
@login_required
@access_required("tester")
def select_referral_type(request, pat_id):
    pp = get_object_or_404(PatientProfile, patient_id=pat_id)  
    if request.method == 'POST':
        form = SelectReferralTypeForm(request.POST)           
        if form.is_valid():
            data = form.cleaned_data
            print data['referral_type']
            return render_to_response('services/linkage/create.html',
                              RequestContext(request,
                                    {'form': LinkageForm2(data['referral_type']),
                                    'toptext':'toptext',
                                    'bottomtext':'bottomtext',
                                    }))
        else:
            return render_to_response('services/linkage/select-referral-type.html',
                              RequestContext(request,
                                    {'form': form,
                                    'toptext':'toptext',
                                    'bottomtext':'bottomtext',
                                    }))

    return render_to_response('services/linkage/select-referral-type.html',
                              RequestContext(request,
                                    {'form': SelectReferralTypeForm(),
                                    'toptext':'toptext',
                                    'bottomtext':'bottomtext',
                                    }))