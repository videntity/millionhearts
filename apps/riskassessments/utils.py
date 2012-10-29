#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=

from django.conf import settings
import sys, json, uuid
import pycurl

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

import uuid


from twilio.rest import TwilioRestClient
from datetime import datetime, date, timedelta
from time import gmtime, strftime, mktime
from ..intake.models import PatientProfile
import time

def send_sms_twilio(twilio_body, twilio_to,
                    twilio_from=settings.TWILIO_DEFAULT_FROM):
    client = TwilioRestClient(settings.TWILIO_SID, settings.TWILIO_AUTH_TOKEN)

    print settings.TWILIO_DEFAULT_FROM, "-->", twilio_to
    if twilio_to=="999-999-9999":
        # Dummy mobile number do not send to Twilio

        d = {'twilio_id':'dummy',
             'from': twilio_from,
             'to': twilio_to,
             'body': twilio_body
            }
    else:
        message = client.sms.messages.create(to=twilio_to,
                                     from_=twilio_from,
                                     body=twilio_body)
        d = {'twilio_id': message.name,
              'from_':message.from_,
              'to': message.to,
              'body': message.body}


    print "To:"+twilio_to
    print "From:"+twilio_from
    print "Message:"+twilio_body


    return d


def create_anonymous_patient_id():
    return str(uuid.uuid4()).replace('-', '').upper()[0:13]


def ArchimedesAssessmentAPI(post_dict):
    
    print "Archimendes : " #, post_dict


    body = StringIO()
    #outfile = "db/out.json"
    #f = open(outfile, "wb")
    URL = settings.ARCHIMEDES_API_URL #+ "?age=55"
    print URL

    #format query post dict
    querystr =""
    for k,v in post_dict.items():
        nv = "%s=%s&" % (k,v)
        querystr+=  nv
    querystr = str(querystr[:-1])
    #print querystr
    #print type( querystr)
       
    c = pycurl.Curl()
    c.setopt(c.SSL_VERIFYPEER, False) 
    c.setopt(pycurl.URL, URL)
    #c.setopt(c.HTTPPOST, "age=55&weight=200")
    c.setopt(c.POSTFIELDS, querystr)
    #c.setopt(c.WRITEDATA, f) 
    c.setopt(pycurl.HTTPHEADER, ["Accept:"])
    c.setopt(c.WRITEFUNCTION, body.write)
    c.perform()
    #f.close()
    body = body.getvalue()
    
    result = json.loads(body)
    result['code'] = code = c.getinfo(pycurl.HTTP_CODE)

    result = json.dumps(result, indent= 4)

    return result