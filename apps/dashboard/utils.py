#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=

import sys, json

def fetch_risks(achimedes_risk_assessment):
    
    ra = json.loads(achimedes_risk_assessment)
    
    resp_dict = {
        'ratingForAge'    : ra["Risk"][0]['ratingForAge'],
        'rating'          : ra["Risk"][0]['rating'],
        'cvdrisk_upper_age' : ra["Risk"][1]['ratingForAge'],
        'cvdrisk_lower_age' : ra["Risk"][2]['ratingForAge'],
        }
    if ra["Risk"][1]['ratingForAge'] and ra["Risk"][2]['ratingForAge']:
        resp_dict['cvdrisk_age'] =  (float(ra["Risk"][1]['ratingForAge']) + \
                                   float(ra["Risk"][2]['ratingForAge']))/2
    else:
        resp_dict['cvdrisk_age'] = ""
    
    return resp_dict