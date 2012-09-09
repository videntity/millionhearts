#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

from django.conf import settings
import os, uuid


def create_anonymous_patient_id():
    return str(uuid.uuid4()).replace('-', '').upper()[0:13]


def create_patient_id(first_name, last_name, last_4_ssn):
    last_4_ssn=str(last_4_ssn)
    if len(first_name)<2 or len(last_name)<2:
        return ""
    patient_id ="%s%s%s%s%s" % (first_name[0].upper(),
                                first_name[-1].upper(),
                                last_name[0].upper(),
                                last_name[-1].upper(),
                                last_4_ssn[0:4])
    if patient_id[0:4].isalpha():
        if patient_id[4:8].isnumeric():
            return patient_id
    return ""



def update_filename(instance, filename):
    path = "patient-avatars/"
    format = instance.patient.patient_id + "-" + filename
    return os.path.join(path, format)


#def handle_uploaded_avatar(f, patient_id):
#
#    dest_dir=os.path.join(settings.MEDIA_ROOT, settings.PATIENT_AVATAR_DIR)
#
#    dest_path=os.path.join(dest_dir, f.name)
#    destination = open(dest_path, 'wb+')
#    for chunk in f.chunks():
#        destination.write(chunk)
#    destination.close()


