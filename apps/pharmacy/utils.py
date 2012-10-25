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



def GoogleGeoCode(geocode_addr_str):

    URL ="http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false" % (geocode_addr_str)
    URL=str(URL)
    body = StringIO()
    outfile = "out.json"
    f = open(outfile, "wb")
    c = pycurl.Curl()
    c.setopt(c.SSL_VERIFYPEER, False) 
    c.setopt(pycurl.URL, URL)
    c.setopt(c.WRITEDATA, f) 
    c.setopt(pycurl.HTTPHEADER, ["Accept:"])
    c.setopt(c.WRITEFUNCTION, body.write)
    c.perform()
    f.close()
    body = body.getvalue()
    
    #result = json.loads(body)
    #result['code'] = code = c.getinfo(pycurl.HTTP_CODE)

    #result = json.dumps(result, indent= 4)

    return body


def SureScriptsPharmacy(google_geocode_json):
    result = json.loads(google_geocode_json)    
    lat = result['results'][0]['geometry']['location']['lat']
    lng = result['results'][0]['geometry']['location']['lng']
    
    URL ="%s?apikey=%s&lat=%s&lon=%s&radius=10&maxResults=10" % (settings.SURESCRIPTS_API_URL,
                                        settings.SURESCRIPTS_API_TOKEN, lat,lng)
    URL=str(URL)
    body = StringIO()
    outfile = "out.json"
    f = open(outfile, "wb")
    c = pycurl.Curl()
    c.setopt(c.SSL_VERIFYPEER, False) 
    c.setopt(pycurl.URL, URL)
    c.setopt(c.WRITEDATA, f) 
    c.setopt(pycurl.HTTPHEADER, ["Accept:"])
    c.setopt(c.WRITEFUNCTION, body.write)
    c.perform()
    f.close()
    body = body.getvalue()
    
    #result = json.loads(body)
    #result['code'] = code = c.getinfo(pycurl.HTTP_CODE)

    #result = json.dumps(result, indent= 4)

    return body
    