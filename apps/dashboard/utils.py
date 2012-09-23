#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=

import sys, json

def fetch_risks(achimedes_risk_assessment):
    
    ra = json.loads(achimedes_risk_assessment)
    
    resp_dict = {
        'cvdrisk'         : ra["Risk"][0],
        'cvdrisk_upper'   : ra["Risk"][1],
        'cvdrisk_lower'   : ra["Risk"][2],
    }

    return resp_dict