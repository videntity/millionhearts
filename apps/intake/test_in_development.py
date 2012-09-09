__author__ = 'mark'
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.utils import unittest
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from datetime import date, datetime
from apps.intake.models import MasterPID, PatientProfile
from apps.intake.urls import *

"""
Tests for the Hive.intake app.

Run with "manage.py test".  Example:
Example: python manage.py test auth intake --settings=test.settings
.dev

Generate the test data
python manage.py dumpdata intake --settings=test.settings.dev --indent=4 >./apps/intake/fixtures/testdata.json
"""

# User full name = Harvey Ive
USERNAME_FOR_TEST='harvey'
PASSWORD_FOR_TEST='password'
VALID_LAST_4_SSN="1234"
VALID_PATIENT_ID="ARFT1234"



class intake_locator_TestCase(TestCase):
    """ Search for a patient by their Patient ID
    """
    def setup(self):
        self.client=Client()
        self.client.login(username=USERNAME_FOR_TEST, password=PASSWORD_FOR_TEST)
        self.client.get=reverse('/intake/locator/',
            kwargs={'pat_id': VALID_PATIENT_ID})



    def test_get_record_for_valid_pat_id(self):
        """ GET completed should return a response
        """
        response = self.client.get('intake/locator', kwargs={'pat_id': VALID_PATIENT_ID} )
        # check response details
        self.assertContains(response,VALID_PATIENT_ID,)


class search_by_ssn_TestCase(TestCase):
    """
    Search for a Patient by SSN (last 4 digits)
    """
    def setup(self):
        self.client=Client()
        self.client.login(username=USERNAME_FOR_TEST, password=PASSWORD_FOR_TEST)
        self.dict = {}
        self.client.get=reverse('/intake/search-by-ssn/',
                {'last_4_ssn': VALID_LAST_4_SSN})

    def test_get_result_for_search_by_ssn(self):
        """GET completed should contain response"""
        response = self.client.get('/search-by-ssn/',
                {'last_4_ssn': VALID_LAST_4_SSN})
        # Check some response details
        self.assertContains(response, "Matches For")

class TestForValidUser(TestCase):
    """
    >>> from django.utils import unittest
    >>> from django.test import TestCase
    >>> from django.test import Client, RequestFactory
    >>> c = Client()
    >>> c.login(username='harvey',password='password')
    True
    >>> response = c.post('/accounts/smscode/', {'username': 'harvey','password': 'password','smscode':'9999'})
    999-999-9999
    9999
    >>> response.status_code
    302
    >>> redirect = c.get('/')
    >>> redirect.content
    '<!doctype html>\n<html class="no-js" lang="en">\n<head>\n    <meta charset="utf-8">\n    \n\t\n\n    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">\n<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\n<meta name="description" content="HIVE - Health Management System"/>\n<title>HIVE - Health Management System</title>\n<meta name="author" content="Alan Viars">\n<link href="/static/img/layout/favicon.ico" rel="shortcut icon" />\n\n<link rel="stylesheet" href="/static/js/lib/vendor/jquery-ui/jquery-ui-1.8.13.custom.css">\n<link rel="stylesheet" href="/static/js/lib/vendor/signature-pad/jquery.signaturepad.css">\n<link rel="stylesheet" href="/static/stylesheets/screen.css">\n<link rel="stylesheet" href="/static/stylesheets/print.css" media="print" />\n\n\n<!--[if lt IE 9]><script src="/static/js/lib/vendor/signature-pad/flashcanvas.js"></script><![endif]-->\n<script src="/static/js/lib/vendor/jquery/jquery-1.7.min.js" type="text/javascript"></script>\n<script src="/static/js/lib/vendor/jquery-ui/jquery-ui-1.8.13.custom.min.js" type="text/javascript"></script>\n\n\n\n\n\n\n    \n    \n</head>\n\n<body class="home-active">\n\n\n<div id="main">\n\n    <div id="top-nav-wrapper">\n\n    <p class="info-bar time-wrapper hidden"></p>\n\n\n    <div class="top-nav">\n\n        <div class="logo">HIVE</div>\n    \n        <div class="user-nav no-print">\n            \n\n                Welcome harvey\n                &nbsp;|&nbsp;\n                <a href="/accounts/logout">logout</a>\n                &nbsp;|&nbsp;\n                <a href="/location/create">change location</a></span>\n                <div class="location">\n                    <span>Good Hope Rd. &amp; 16th St SE  DC, 20004 (Ward:8)</span>\n                </div>\n            \n        <br/>\n\n        </div>\n\n        \n            <ul class="nav no-print">\n                <li><a href="/" class="nav-home-tab">Home</a></li>\n                <li><a href="/inprocess-list" class="nav-today-tab">Today</a></li>\n                <li><a href="/outreach/" class="nav-outreach-tab">Outreach</a></li>\n                <li><a href="/survey" class="nav-survey-tab">Survey Follow-Up</a></li>\n                <li><a href="/patient-tracker" class="nav-patient-tab">Patient Tracker</a></li>\n                <li><a href="/reports/" class="nav-reports-tab">Reports</a></li>\n                <li><a href="/grants" class="nav-grants-tab">Grants</a></li>\n                <li><a href="/tools" class="nav-tools-tab">Tools</a></li>\n            </ul>\n        \n    </div>\n\n</div>\n\n\n<div id="sub-nav-wrapper" class="no-print">\n    <div class="sub-nav">\n\n        <ul class="subnav-survey">\n            <li><a href="/gpra-sixmonfu/splash">GPRA 6 Month Follow-Up</a></li>\n            <li><a href="/noms-threemonfu/splash">NOMS 3 Month Follow-Up</a></li>\n        </ul>\n\n        <ul class="subnav-outreach">\n            <li><a href="/outreach/daily-outreach-summary">Daily Outreach Summary</a></li>\n            <li><a href="/intake/create">Initial Intake</a></li>\n        </ul>\n\n        <ul class="subnav-grants">\n            <li><a href="/grants/stats">Grant Statistics</a></li>\n        </ul>\n        \n        <ul class="subnav-reports">\n            <li><a href="/reports/">HIV Report Generator</a></li>\n        </ul>\n    </div>\n</div>\n\n\n\n    \n\n    <div id="content" class="no-print-border">\n        \n\n\n\t\t\n\n<div class="header-box">\n    <h1>Welcome To HIVE</h1>\n</div>\n\n<div class="content-box">\n    <div class="task-group">\n\n        <h2>Select A Task</h2>\n        <ul class="link-list">\n            <li><a href="/intake/create">Initial Intake</a></li>\n            <li><a href="/intake/search-by-name">Member Search Name</a></li>\n            <li><a href="/intake/search-by-ssn">Member Search SSN</a></li>\n        </ul>\n\n    </div>\n</div>\n          \n\n\n\t\t\n\t\t\n    </div>\n\n    <div id="footer">\n    <p>\n        &copy; 2011 &ndash; Developed By <a href="https://videntity.com">Videntity Systems Inc.</a> for the Community Education Group<br/>\n        All rights reserved.\n    </p>\n</div>\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n    \n</div>\n\n\n\n\n\n\n\n</body>\n</html>'
    """

class intake_locator_TestCase(TestCase):
    """ Search for a patient by their Patient ID
    """
    def setup(self):
        Test_Start("intake_locator_TestCase")
        self.client=Client()
        access = self.client.login(username=USERNAME_FOR_TEST,
            password=PASSWORD_FOR_TEST)
        print access
        Test_End()

    def test_get_record_for_valid_pat_id(self):
        """ GET completed should return a response
        """
        Test_Start()



        self.client = Client()
        self.client.login(username=USERNAME_FOR_TEST,password=PASSWORD_FOR_TEST)
        attempt_login = login_to_hive(USERNAME_FOR_TEST,
            PASSWORD_FOR_TEST,SMSCODE_FOR_TEST)
        print "login result:"+str(attempt_login)
        print "get /intake/locator/"+VALID_PATIENT_ID
        response = self.client.get('/intake/locator/ARFT1234',follow=True)
        # got_code = self.assertEqual(response.status_code, 200)


        print response.content
        # check response details
        print "%s = %s" % (response.status_code,'200')
        print "checking for VALID_PATIENT_ID in /intake/locator/"+VALID_PATIENT_ID
        outcome = self.assertContains(response.content,
            VALID_PATIENT_ID)
        # outcome = "skipped"
        print "None is good: Outcome =" + str(outcome)
        Test_End()
