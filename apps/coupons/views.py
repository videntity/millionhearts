#vim: ai ts=4 sts=4 et sw=4
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import messages
from ..intake.models import PatientProfile
from django.forms.models import model_to_dict
from django.core.urlresolvers import reverse
import datetime
from ..accounts.decorators import access_required
from utils import save_new_coupon_range
from forms import CouponRangeForm
from ..intake.models import Coupon
from ..intake.forms import PatientSearchForm


@login_required
@access_required("tester")
def search_by_name(request):
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
    
            
            
            #add messages about our results.
            result_count = pps.count()
            
            
            if (result_count == 0):
                result_string = "%s results found." % (result_count)
            elif (result_count == 1):
                result_string = "%s result found." % (result_count)
            else:
                result_string = "%s results found" % (result_count)
            return render_to_response('coupons/search-by-name.html', 
                             {'form': PatientSearchForm(),
                              'results': pps,
                              'fst_name': first_name,
                              'lst_name': last_name,
                              'result_count': result_string},
                              context_instance = RequestContext(request))
            
        #form is invalid    
        return render_to_response('coupons/search-by-name.html', 
                             {'form': form},
                              context_instance = RequestContext(request))
    
    #request is a GET (not a POST)    
    return render_to_response('coupons/search-by-name.html', 
                             {'form': PatientSearchForm()},
                                context_instance = RequestContext(request))





@login_required
@access_required("admin")
def issue_coupons(request, pat_id):       
    pp = get_object_or_404(PatientProfile, patient_id=pat_id)
    current_coupons=Coupon.objects.filter(member_issued=pp)
    if request.method == 'POST':
        form = CouponRangeForm(request.POST)
        if form.is_valid():
            coupon_range=save_new_coupon_range(member_issued=pp,
                        worker=request.user,
                        starting_coupon=form.cleaned_data['starting_coupon'],
                        number_of_coupons=form.cleaned_data['number_of_coupons'])
            message="Coupons %s issued." % (coupon_range)
            messages.success(request, message)
            return HttpResponseRedirect(reverse('home'))
        
        else:
            return render_to_response('coupons/coupons-issued.html',
                        {
                         'form': form,
                         'current_coupons': current_coupons,
                        },
                        RequestContext(request))
        
    else:

        return render_to_response('coupons/coupons-issued.html',
                                {
                                'form': CouponRangeForm(),
                                'current_coupons': current_coupons,
                                },
                            RequestContext(request))# Create your views here.
