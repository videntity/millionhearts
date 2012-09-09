"""
run "python manage.py test services >test_results/services_testresult.txt"

Author: Mark Scrimshire @ekivemark

"""


from datetime import date,datetime
from django.shortcuts import  get_object_or_404
from django.test import TestCase
from testutils import  Test_Start, Test_End, Test_Msg, test_for_401, test_for_200, test_for_200_with_get
import inspect

from apps.services.models import ServiceOrg, Referral
from apps.intake.models import PatientProfile
from settings_test import *


"""
Tests for the Hive.services app.

Run from root of hive app.
Run with "python manage.py test {app name}"
Example: python manage.py test services >./test_results/services_testresult.txt

Generate the test data
python manage.py dumpdata services --indent=4 >./apps/services/fixtures/services_testdata.json

"""
# Add module specific test variables here

# End of Module specific test variables section



# SimpleTest for a working Test Harness
# @unittest.skip
class Services_SimpleTest(TestCase):
    """Background to this test harness
    and prove the test harness works
    """

    fixtures =  ['apps/intake/fixtures/intake_test_data.json',
                 'apps/services/fixtures/services_testdata.json',
                 'apps/accounts/fixtures/accounts_test_data.json',
                 'apps/intake/fixtures/intake_inprocess.json',
                 'apps/grants/fixtures/grants_test_data.json',
                 'apps/organizations/fixtures/testdata.json'
                 ]

    def test_services_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        Test_Start("1+1=2")
        answer = self.assertEqual(1 + 1, 2)
        Test_Msg("hive.apps.services.tests.py")
        print "     Test Runtime: "+str(datetime.now())
        if answer == None:
            print "     Test Harness ready"
        else:
            print "     This Test Harness has a problem"
        Test_End("hive.apps.services.tests.py")
        return

class Services_Search_Name_TestCase(TestCase):
    """
    Search by Name in /services/search-by-name
    """
    fixtures =  ['apps/intake/fixtures/intake_test_data.json',
                 'apps/services/fixtures/services_testdata.json',
                 'apps/accounts/fixtures/accounts_test_data.json',
                 'apps/intake/fixtures/intake_inprocess.json',
                 'apps/grants/fixtures/grants_test_data.json',
                 'apps/organizations/fixtures/testdata.json'
                 ]

    def test_search_invalid_tester(self):
        """
        Test with no tester permissions. expect 401 - not authorised
        """
        Test_Start()
        # We should search for this

        prn_info = False

        p = get_object_or_404(PatientProfile, patient_id=VALID_PATIENT_ID)
        print p

        calling_test_function = inspect.getframeinfo(inspect.currentframe().f_back)[2]
        if prn_info!=False:
            print "calling:["+calling_test_function+"]"

        usrname = USERNAME_NOT_TEST
        passwd=PASSWORD_NOT_TEST
        output = []
        post_url = '/services/search-by-name'
        post_parameters = {}

        Access_Authorised = test_for_401(self, usrname, passwd, output, post_url,post_parameters, calling_test_function, prn_info )
        if Access_Authorised == None:
            Test_Msg("Successful Test for 401")
        else:
            Test_Msg("Test Failed for 401")

        Test_End()

        return

    def test_search_valid_tester_bad_name(self):
        """
        Test with Tester Permission but with a name that is not found
        """
        Test_Start()
        # We should search for this
        p = get_object_or_404(PatientProfile, patient_id=VALID_PATIENT_ID)
        print p

        prn_info = False

        usrname = USERNAME_FOR_TEST
        passwd=PASSWORD_FOR_TEST
        output = []
        post_url = '/services/search-by-name'
        post_parameters = {'last_name':INVALID_PATIENT_LASTNAME,
                           'first_name':INVALID_PATIENT_FIRSTNAME}
        look_for_this = INVALID_PATIENT_FIRSTNAME+" "+INVALID_PATIENT_LASTNAME
        calling_test_function = inspect.getframeinfo(inspect.currentframe().f_back)[2]

        Access_Authorised = test_for_200(self, usrname, passwd, output, post_url,post_parameters, look_for_this, calling_test_function, prn_info )
        if prn_info!=False:
            print "Access Authorised:"
            print Access_Authorised

        if Access_Authorised == None:
            Test_Msg("Successful Test for Invalid Patient:"+INVALID_PATIENT_FIRSTNAME+" "+INVALID_PATIENT_LASTNAME)
        else:
            Test_Msg("Test Failed for Invalid Patient:"+INVALID_PATIENT_FIRSTNAME+" "+INVALID_PATIENT_LASTNAME)

        Test_End()


        return

    def test_search_valid_tester_good_name(self):
        """
        Test with Tester Permission and a good name
        """
        Test_Start()
        # We should search for this
        p = get_object_or_404(PatientProfile, patient_id=VALID_PATIENT_ID)
        print p

        prn_info = False

        usrname = USERNAME_FOR_TEST
        passwd=PASSWORD_FOR_TEST
        output = []
        post_url = '/services/search-by-name'
        post_parameters = {'last_name':VALID_PATIENT_LASTNAME,
                           'first_name':VALID_PATIENT_FIRSTNAME}
        look_for_this = VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME
        calling_test_function = inspect.getframeinfo(inspect.currentframe().f_back)[2]

        Access_Authorised = test_for_200(self, usrname, passwd, output, post_url,post_parameters, look_for_this, calling_test_function, prn_info )
        if prn_info!=False:
            print "Access Authorised:"
            print Access_Authorised

        if Access_Authorised == None:
            Test_Msg("Successful Test for Valid Patient:"+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME)
        else:
            Test_Msg("Test Failed for Valid Patient:"+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME)

        Test_End()

        return

class Services_Referral_TestCase(TestCase):
    """
    Referral create and View
    """

    fixtures =  ['apps/intake/fixtures/intake_test_data.json',
                 'apps/services/fixtures/services_testdata.json',
                 'apps/accounts/fixtures/accounts_test_data.json',
                 'apps/intake/fixtures/intake_inprocess.json',
                 'apps/grants/fixtures/grants_test_data.json',
                 'apps/organizations/fixtures/testdata.json'
                 ]

    def test_create_then_view_referral(self):
        """
        Create a Referral then View it
        """
        Test_Start()
        # We should search for this
        p = get_object_or_404(PatientProfile, patient_id=VALID_PATIENT_ID)
        print p

        prn_info = True

        usrname = USERNAME_FOR_TEST
        passwd=PASSWORD_FOR_TEST
        output = []
        post_url = '/services/search-by-name'
        post_parameters = {'last_name':VALID_PATIENT_LASTNAME,
                           'first_name':VALID_PATIENT_FIRSTNAME}
        look_for_this = VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME
        calling_test_function = inspect.getframeinfo(inspect.currentframe().f_back)[2]

        Access_Authorised = test_for_200(self, usrname, passwd, output, post_url,post_parameters, look_for_this, calling_test_function, prn_info )
        if prn_info!=False:
            print "Access Authorised:"
            print Access_Authorised

        if Access_Authorised == None:
            Test_Msg("Step 1 Worked - Valid Patient:"+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME)
        else:
            Test_Msg("Step 1 Failed - Valid Patient:"+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME)

        output = []
        post_url = '/services/referral/create/'+VALID_PATIENT_ID
        post_parameters = {
                           "referral_type":"primary-care",
                           "link_type":"NEW",
                           "organization":"4",
                           "ok_to_mail":"",
                           "okay_to_call":"",
                           "okay_to_leave_message":"",
                           "note":"",
                           "creation_date_month": datetime.today().strftime("%m"),
                           "creation_date_day": datetime.today().strftime("%d"),
                           "creation_date_year":datetime.today().strftime("%Y"),

                          }

        Test_Msg("failing due to mis match between referral type and organization")
        look_for_this = "does not provide primary-care"

        Access_Authorised = test_for_200(self, usrname, passwd, output, post_url,post_parameters, look_for_this, calling_test_function, prn_info )
        if prn_info!=False:
            print "Access Authorised:"
            print Access_Authorised




        if Access_Authorised == None:
            Test_Msg("Step 2 Worked - Valid Patient:"+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME)
        else:
            Test_Msg("Step 2 Failed - Valid Patient:"+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME)

        post_parameters = {
                            "referral_type":"food",
                            "link_type":"NEW",
                            "organization":"6",
                            "ok_to_mail":"",
                            "okay_to_call":"",
                            "okay_to_leave_message":"",
                            "note":"",
                            "creation_date_month": datetime.today().strftime("%m"),
                            "creation_date_day": datetime.today().strftime("%d"),
                            "creation_date_year":datetime.today().strftime("%Y"),
                            'worker_signature':WORKER_SIGNATURE,
                           }

        look_for_this = "New referral created successfully"

        Access_Authorised = test_for_200(self, usrname, passwd, output, post_url,post_parameters, look_for_this, calling_test_function, prn_info )
        if prn_info!=False:
            print "Access Authorised:"
            print Access_Authorised

        if Access_Authorised == None:
            Test_Msg("Step 3 Worked - Valid Patient:"+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME)
        else:
            Test_Msg("Step 3 Failed - Valid Patient:"+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME)


        Test_End()
        Test_Start()
        # browse past referrals
        prn_info = False

        referral_item = Referral.objects.get(pk=1)
        date_of = referral_item.creation_date
        if prn_info!=False:
            print referral_item
            print date_of

        post_url = '/services/referral/browse-past/'+VALID_PATIENT_ID

        add_more1 = str(ServiceOrg.objects.get(pk=1))
        add_more2 = " on "
        add_more3 = str(date_of)
        add_more4 = " by "+usrname

        add_more0 = VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME+" ("+VALID_PATIENT_ID+") was referred to "
        look_for_this = add_more0

        if prn_info!=False:
            print look_for_this

        Access_Authorised = test_for_200_with_get(self, usrname, passwd, output, post_url,post_parameters, look_for_this, calling_test_function, prn_info )
        if prn_info!=False:
            print "Access Authorised:"
            print Access_Authorised

        if Access_Authorised == None:
            Test_Msg("Step 4 Worked - Valid Referral:"+look_for_this)
        else:
            Test_Msg("Step 4 Failed - Valid Referral:"+look_for_this)

        post_url = '/services/referral/view/1'
        post_parameters = {}
        look_for_this = "Referral View: <em>"+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME+" ("+VALID_PATIENT_ID+")"

        Access_Authorised = test_for_200_with_get(self, usrname, passwd, output, post_url,post_parameters, look_for_this, calling_test_function, prn_info )
        if prn_info!=False:
            print "Access Authorised:"
            print Access_Authorised

        if Access_Authorised == None:
            Test_Msg("Step 5 Worked - Valid Patient/Referral:"+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME)
        else:
            Test_Msg("Step 5 Failed - Valid Patient/Referral:"+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME)

        Test_End()


        ##################################
class Services_Linkage_TestCase(TestCase):
    """
    Linkage create and View
    """

    fixtures =  ['apps/intake/fixtures/intake_test_data.json',
                 'apps/services/fixtures/services_testdata.json',
                 'apps/accounts/fixtures/accounts_test_data.json',
                 'apps/intake/fixtures/intake_inprocess.json',
                 'apps/grants/fixtures/grants_test_data.json',
                 'apps/organizations/fixtures/testdata.json'
                 ]

    def test_create_then_view_linkage(self):
        """
        Create a Linkage then View it
        """
        Test_Start()
        # We should search for this
        p = get_object_or_404(PatientProfile, patient_id=VALID_PATIENT_ID)
        print p

        prn_info = False

        usrname = USERNAME_FOR_TEST
        passwd=PASSWORD_FOR_TEST
        output = []
        post_url = '/services/search-by-name'
        post_parameters = {'last_name':VALID_PATIENT_LASTNAME,
                           'first_name':VALID_PATIENT_FIRSTNAME}
        look_for_this = VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME
        calling_test_function = inspect.getframeinfo(inspect.currentframe().f_back)[2]

        Access_Authorised = test_for_200(self, usrname, passwd, output, post_url,post_parameters, look_for_this, calling_test_function, prn_info )
        if prn_info!=False:
            print "Access Authorised:"
            print Access_Authorised

        if Access_Authorised == None:
            Test_Msg("Step 1 Worked - Valid Patient:"+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME)
        else:
            Test_Msg("Step 1 Failed - Valid Patient:"+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME)

        output = []
        post_url = '/services/linkage/create/'+VALID_PATIENT_ID
        post_parameters = {'service':'1',
                           'referral_type':'CLOTHING',
                           'creation_date_month':'1',
                           'creation_date_day':'5',
                           'creation_date_year':'2012',
                           'note':'Creating linkage for '+VALID_PATIENT_ID,
                           'mode_of_transportation':'AUTOMOBILE',
                           'date_of_linkage':str(date.today()),
                           'worker_signature':WORKER_SIGNATURE,
                           'patient_signature':PATIENT_SIGNATURE}


        look_for_this = "field is required"

        Access_Authorised = test_for_200(self, usrname, passwd, output, post_url,post_parameters, look_for_this, calling_test_function, prn_info )
        if prn_info!=False:
            print "Access Authorised:"
            print Access_Authorised

        if Access_Authorised == None:
            Test_Msg("Step 2 Worked - Valid Patient:"+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME)
        else:
            Test_Msg("Step 2 Failed - Valid Patient:"+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME)

        post_parameters = {'service':'1',
                           'referral_type':'CLOTHING',
                           'ok_to_mail':True,
                           'creation_date_month':'1',
                           'creation_date_day':'5',
                           'creation_date_year':'2012',
                           'note':'Creating linkage for '+VALID_PATIENT_ID,
                           'mode_of_transportation':'AUTOMOBILE',
                           'date_of_linkage':str(date.today()),
                           'worker_signature':WORKER_SIGNATURE,
                           'patient_signature':PATIENT_SIGNATURE}

        Access_Authorised = test_for_200(self, usrname, passwd, output, post_url,post_parameters, look_for_this, calling_test_function, prn_info )
        if prn_info!=False:
            print "Access Authorised:"
            print Access_Authorised

        if Access_Authorised == None:
            Test_Msg("Step 3 Worked - Valid Patient:"+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME)
        else:
            Test_Msg("Step 3 Failed - Valid Patient:"+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME)

        # browse past referrals
        prn_info = False

        referral_item = Referral.objects.get(pk=1)
        date_of = referral_item.creation_date
        if prn_info!=False:
            print referral_item
            print date_of

        post_url = '/services/linkage/browse-past/'+VALID_PATIENT_ID

        add_more1 = str(ServiceOrg.objects.get(pk=1))
        add_more2 = " on "
        add_more3 = str(date_of)
        add_more4 = " by "+usrname

        add_more0 = VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME+" ("+VALID_PATIENT_ID+") was linked to "
        look_for_this = add_more0

        if prn_info!=False:
            print look_for_this

        Access_Authorised = test_for_200(self, usrname, passwd, output, post_url,post_parameters, look_for_this, calling_test_function, prn_info )
        if prn_info!=False:
            print "Access Authorised:"
            print Access_Authorised

        if Access_Authorised == None:
            Test_Msg("Step 4 Worked - Valid Linkage:"+look_for_this)
        else:
            Test_Msg("Step 4 Failed - Valid Linkage:"+look_for_this)

        post_url = '/services/linkage/view/1'
        post_parameters = {}
        look_for_this = "Linkage View: <em>"+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME+" ("+VALID_PATIENT_ID+")"

        Access_Authorised = test_for_200(self, usrname, passwd, output, post_url,post_parameters, look_for_this, calling_test_function, prn_info )
        if prn_info!=False:
            print "Access Authorised:"
            print Access_Authorised

        if Access_Authorised == None:
            Test_Msg("Step 5 Worked - Valid Patient/Linkage:"+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME)
        else:
            Test_Msg("Step 5 Failed - Valid Patient/Linkage:"+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME)

        Test_End()
