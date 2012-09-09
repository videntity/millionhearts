#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
import re
from django.contrib import messages
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from ..utils import build_pretty_data_view
from models import *
from forms import *
import json


@login_required
def organization_search_by_name(request):
    if request.method == 'POST':
    
        form = OrganizationSearchForm(request.POST)
        
        if form.is_valid():  
            data = form.cleaned_data
            name = data['name']
            organization_type = data['organization_type']
            pps = Organization.objects.all()
            if name:
                pps = pps.filter(name__icontains=name)

            if organization_type!="ANY":
                pps = pps.filter(org_type=organization_type)

            return render_to_response('organizations/organization/search-by-name.html', 
                             {'form': OrganizationSearchForm(),
                              'results': pps,
                              'result_count': pps.count(),
                              'name' : name,
                              'o_type' : organization_type},
                             context_instance = RequestContext(request))
            
        #form is invalid    
        return render_to_response('organizations/organization/search-by-name.html', 
                             {'form': form},
                              context_instance = RequestContext(request))
    
    #request is a GET (not a POST)    
    return render_to_response('organizations/organization/search-by-name.html', 
                             {'form': OrganizationSearchForm(),
                              'search' : "false",},
                              context_instance = RequestContext(request))
                   



@login_required
def organization_view(request, pk):
    org = get_object_or_404(Organization, pk=pk)
    orgform=OrganizationForm(instance=org)
    data=build_pretty_data_view(form_instance=orgform, model_object=org,
                            exclude=('accepts_insurance', 'services'))
    return render_to_response('organizations/organization/view.html',
                              RequestContext(request,
                                             {'pk':pk,
                                              'data':data,
                                              'name':   "Organization View",
                                              'toptext': "",
                                              'accepts_insurance': org.accepts_insurance,
                                              'services': org.services,
                                              'bottomtext':"", }))

@login_required
def organization_create(request):
    if request.method == 'POST':
        form = OrganizationForm(request.POST)           
        if form.is_valid():
            form.save()
            messages.success(request,'A new organization record was created.')    
            return HttpResponseRedirect(reverse('tools'))
        else:
            messages.error(request,'There were errors on the form. Please correct the errors below.') 
            return render_to_response('organizations/organization/create.html',
                              RequestContext(request,
                                    {'form': form,
                                    'toptext':'toptext',
                                    'bottomtext':'bottomtext',
                                    }))

    return render_to_response('organizations/organization/create.html',
                              RequestContext(request,
                                    {'form': OrganizationForm(),
                                    'toptext':'toptext',
                                    'bottomtext':'bottomtext',
                                    }))

@login_required
def provider_search_by_name(request):
    if request.method == 'POST':
    
        form = ProviderSearchForm(request.POST)
        
        if form.is_valid():  
            data = form.cleaned_data
            first_name = data['first_name']
            last_name = data['last_name']
            pps = Provider.objects.all()
            if first_name:
                pps = pps.filter(first_name__icontains=first_name)

            if last_name:
                pps = pps.filter(last_name__icontains=last_name)

            return render_to_response('organizations/provider/search-by-name.html', 
                             {'form': ProviderSearchForm(),
                              'results': pps,
                              'result_count': pps.count(),
                              'first_name' : first_name,
                              'last_name' : last_name,},
                             context_instance = RequestContext(request))
            
        #form is invalid    
        return render_to_response('organizations/provider/search-by-name.html', 
                             {'form': form},
                              context_instance = RequestContext(request))
    
    #request is a GET (not a POST)    
    return render_to_response('organizations/provider/search-by-name.html', 
                             {'form': ProviderSearchForm(),
                              'search' : "false",},
                              context_instance = RequestContext(request))


@login_required
def provider_create(request):
         
    if request.method == 'POST':
        form = ProviderForm(request.POST)           
        if form.is_valid():
            form.save()
            messages.success(request,'A new provider record was created.')    
            return HttpResponseRedirect(reverse('tools'))
        else:
            messages.error(request,'There were errors on the form. Please correct the errors below.') 
            return render_to_response('organizations/provider/create.html',
                              RequestContext(request,
                                    {'form': form,
                                    'toptext':'toptext',
                                    'bottomtext':'bottomtext',
                                    }))

    return render_to_response('organizations/provider/create.html',
                              RequestContext(request,
                                    {'form': ProviderForm(),
                                    'toptext':'toptext',
                                    'bottomtext':'bottomtext',
                                    }))


@login_required
def provider_view(request, pk):
    pro = get_object_or_404(Provider, pk=pk)
    proform=ProviderForm(instance=pro)
    data=build_pretty_data_view(form_instance=proform, model_object=pro)
    return render_to_response('organizations/provider/view.html',
                              RequestContext(request,
                                             {'pk':pk,
                                              'data':data,
                                              'name': "View Provider",
                                              'toptext': "",
                                              'bottomtext':"", }))
    
    
    
@login_required
def patient_care_team_create(request, pat_id):
    patient = get_object_or_404(PatientProfile, patient_id=pat_id)
     
    #Create or edit?
    try:
        pct = PatientCareTeam.objects.get(patient=patient)
        edit=True
    except(PatientCareTeam.DoesNotExist):
        edit=False
        
    if request.method == 'POST':
        
        if edit:
            form = PatientCareTeamForm(request.POST, instance=pct)
        else:
            form = PatientCareTeamForm(request.POST)
        
        
        if form.is_valid():
            form.save()
            messages.success(request,'A patient care team record was created/updated.')    
            return HttpResponseRedirect(reverse('patient_dashboard', args=(pat_id,)))
        else:
            messages.error(request,'There were errors on the form. Please correct the errors below.') 
            return render_to_response('organizations/patient-care-team/create.html',
                              RequestContext(request,
                                    {'form': form,
                                    'toptext':'toptext',
                                    'bottomtext':'bottomtext',
                                    'page':1,
                                    'page_next':1,
                                    }))
    
    if edit:
        #return bound form
        return render_to_response('organizations/patient-care-team/create.html',
                              RequestContext(request,
                                    {'form': PatientCareTeamForm(instance=pct),
                                    'toptext':'toptext',
                                    'bottomtext':'bottomtext',
                                    'page':1,
                                    'page_next':1,
                                    }))  
    else:
        #new so create blank form
        return render_to_response('organizations/patient-care-team/create.html',
                              RequestContext(request,
                                    {'form': PatientCareTeamForm(initial={'patient': patient}),
                                    'toptext':'toptext',
                                    'bottomtext':'bottomtext',
                                    'page':1,
                                    'page_next':1,
                                    }))


@login_required
def patient_care_team_view(request, pat_id):
    p = get_object_or_404(PatientCareTeam, patient__patient_id=pat_id)
    pf=PatientCareTeamForm(instance=p)
    data=build_pretty_data_view(form_instance=pf, model_object=p,
                                exclude=('providers','organizations','users',))
    return render_to_response('organizations/patient-care-team/view.html',
                              RequestContext(request,
                                             {'patient_id':pat_id,
                                              'data':data,
                                              'providers': p.providers,
                                              'organizations':p.organizations,
                                              'users':p.users,
                                              'name': "Patient Care Team",
                                              'toptext': "",
                                              'bottomtext':"",
                                              'page':1,
                                              'page_next':1,}))
    
    


def load_providers(request):
    providers = Provider.objects.all().delete()
    json_data=open("./apps/organizations/dcproviders.json").read()

    data = json.loads(json_data)
    
    
    for k, v in data.items():
        p=Provider.objects.create(npi=k, first_name=v['first_name'],
                                         last_name=v['last_name'],
                                         fax_number=v['fax'],
                                         address1=v['address'],
                                         state=v['state'],
                                         code=v['code'],
                                         description= v['description'],
                                         zip = v['zip'],
                                         url = v['url'],       
                                         individual = v['individual'],
                                         group = v['group'], 
                                         taxclass = v['taxclass'],
                                         speciality=v['speciality'],)
    
    return HttpResponse('OK')
    
    