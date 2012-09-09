"""
run "python manage.py test coupons>test_results/coupons_testresult.txt"

Author: Mark Scrimshire @ekivemark

"""

__author__ = 'mark'
from django.test import TestCase
from apps.accounts.models import User
from apps.intake.urls import *
from testutils import  Test_Start, Test_End, Test_Msg, test_for_401, test_for_200
import inspect
from settings_test import *

"""
Tests for the Hive.coupons app.

Run from root of hive app.
Run with "python manage.py test {app name}"
Example: python manage.py coupons intake >./test_results/coupons_testresult.txt

Generate the test data
python manage.py dumpdata coupons --indent=4 >./apps/coupons/fixtures/coupons_testdata.json

"""

# Add module specific test variables here

# End of Module specific test variables section


# SimpleTest for a working Test Harness
# @unittest.skip
class Coupons_SimpleTest(TestCase):
    """Background to this test harness
    and prove the test harness works
    """

    fixtures = ['apps/intake/fixtures/intake_test_data.json',
                'apps/services/fixtures/services_testdata.json',
                'apps/accounts/fixtures/accounts_test_data.json']

    def test_services_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        Test_Start("1+1=2")
        answer = self.assertEqual(1 + 1, 2)
        Test_Msg("hive.apps.coupons.tests.py")
        print "     Test Runtime: "+str(datetime.datetime.now())
        if answer == None:
            print "     Test Harness ready"
        else:
            print "     This Test Harness has a problem"

        Test_End("hive.apps.coupons.tests.py")
        return

class Coupons_Search_Name_TestCase(TestCase):
    """
    Search by Name in /coupons/search-by-name
    """
    fixtures =  ['apps/services/fixtures/services_testdata.json',
                 #'/apps/accounts/fixtures/accounts_test_data.json',
                 'apps/coupons/fixtures/accounts_test_data.json',
                 'apps/intake/fixtures/intake_inprocess.json']

    def test_search_invalid_tester(self):
        """
        Test with no tester permissions. expect 401 - not authorised
        """
        Test_Start()
        # We should search for this
        prn_info = False

        print PatientProfile
#        p = get_object_or_404(PatientProfile, patient_id=VALID_PATIENT_ID)
#        print p

        calling_test_function = inspect.getframeinfo(inspect.currentframe().f_back)[2]
        if prn_info!=False:
            print "calling:["+calling_test_function+"]"

        usrname = USERNAME_NOT_TEST
        passwd=PASSWORD_NOT_TEST
        output = []
        post_url = '/coupons/search-by-name'
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
#        p = get_object_or_404(PatientProfile, patient_id=VALID_PATIENT_ID)
#        print p

        prn_info = False

        usrname = USERNAME_FOR_TEST
        passwd=PASSWORD_FOR_TEST
        output = []
        post_url = '/coupons/search-by-name'
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
#        p = get_object_or_404(PatientProfile, patient_id=VALID_PATIENT_ID)
#        print p

        prn_info = False

        usrname = USERNAME_FOR_TEST
        passwd=PASSWORD_FOR_TEST
        output = []
        post_url = '/coupons/search-by-name'
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

class Assign_Coupons_TestCase(TestCase):
    """
    Test with Tester Permission and a valid patient.

    """

    fixtures =  ['apps/services/fixtures/services_testdata.json',
                 'apps/accounts/fixtures/accounts_test_data.json',
                 # 'apps/coupons/fixtures/accounts_test_data.json',
                 'apps/intake/fixtures/intake_inprocess.json',
                 'apps/coupons/fixtures/admin_account_permission.json']

    def test_user_accounts(self):
        Test_Start("Do we have the right accounts loaded?")
        u = User.objects.all()
        print u


        Test_End()

    def test_assign_coupons_successfully(self):
        Test_Start()
        # We should search for this
#        p = get_object_or_404(PatientProfile, patient_id=VALID_PATIENT_ID)
#        print p

        prn_info = False

        usrname = USERNAME_FOR_TEST
        passwd=PASSWORD_FOR_TEST
        output = []
        post_url = '/coupons/search-by-name'
        post_parameters = {'last_name':VALID_PATIENT_LASTNAME,
                           'first_name':VALID_PATIENT_FIRSTNAME}
        look_for_this = "Assign coupons to "+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME
        calling_test_function = inspect.getframeinfo(inspect.currentframe().f_back)[2]

        Access_Authorised = test_for_200(self, usrname, passwd, output, post_url,post_parameters, look_for_this, calling_test_function, prn_info )
        if prn_info!=False:
            print "Access Authorised:"
            print Access_Authorised

        if Access_Authorised == None:
            Test_Msg("We have a valid patient:"+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME)
        else:
            Test_Msg("Invalid Patient:"+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME)

        Test_Msg("We are ready to assign coupons to "+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME)

        # Setup for Assign Coupons screen
        start_coupon = 226
        coupon_count = 3


        # we need to construct the following string:
        # "Coupons ['226', '227', '228'] issued."
        # "Coupons [&#39;226&#39;, &#39;227&#39;, &#39;228&#39;] issued."

        post_url = '/coupons/issue-coupons/'+VALID_PATIENT_ID
        post_parameters = {'starting_coupon':str(start_coupon),
                           'number_of_coupons':str(coupon_count)}
        coupon_string = "Coupons ["
        for n in range(coupon_count):
            coupon_string = coupon_string + "&#39;"+ str((start_coupon)+n)+"&#39;"
            if n != (coupon_count-1):
                coupon_string = coupon_string + ", "
                if prn_info != False:
                    print "n:"+str(n)+" of "+str(coupon_count)

        coupon_string = coupon_string + "] issued."
        look_for_this = coupon_string

        if prn_info !=False:
            print "Expecting this string:"+look_for_this

        coupon_result = test_for_200(self, usrname, passwd, output, post_url,post_parameters, look_for_this, calling_test_function, prn_info )
        if prn_info!=False:
            print "Coupons_issued:"
            print coupon_result

        if coupon_result == None:
            Test_Msg("Successfully Issued Coupons for Valid Patient:"+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME)
            Test_Msg(look_for_this)
        else:
            Test_Msg("Failed to issue coupons for Valid Patient:"+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME)

        Test_End()

        return

    def test_assign_bad_coupon_range(self):
        """
        In this test we have to find the patient.
        Create some coupons and then try to issue a duplicate coupon.
        """
        Test_Start()
        # We should search for this
#        p = get_object_or_404(PatientProfile, patient_id=VALID_PATIENT_ID)
#        print p

        prn_info = False

        usrname = USERNAME_FOR_TEST
        passwd=PASSWORD_FOR_TEST
        output = []
        post_url = '/coupons/search-by-name'
        post_parameters = {'last_name':VALID_PATIENT_LASTNAME,
                           'first_name':VALID_PATIENT_FIRSTNAME}

        look_for_this = "Assign coupons to "+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME
        calling_test_function = inspect.getframeinfo(inspect.currentframe().f_back)[2]

        Access_Authorised = test_for_200(self, usrname, passwd, output, post_url,post_parameters, look_for_this, calling_test_function, prn_info )
        if prn_info!=False:
            print "Access Authorised:"
            print Access_Authorised

        if Access_Authorised == None:
            Test_Msg("We have a valid patient:"+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME)
        else:
            Test_Msg("Invalid Patient:"+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME)

        Test_Msg("We are ready to assign coupons to "+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME)

        # Setup for Assign Coupons screen
        start_coupon = 226
        coupon_count = 3

        # we need to construct the following string:
        # "Coupons ['226', '227', '228'] issued."
        # "Coupons [&#39;226&#39;, &#39;227&#39;, &#39;228&#39;] issued."

        post_url = '/coupons/issue-coupons/'+VALID_PATIENT_ID
        post_parameters = {'starting_coupon':str(start_coupon),
                           'number_of_coupons':str(coupon_count)}
        coupon_string = "Coupons ["
        for n in range(coupon_count):
            coupon_string = coupon_string + "&#39;"+ str((start_coupon)+n)+"&#39;"
            if n != (coupon_count-1):
                coupon_string = coupon_string + ", "
                if prn_info != False:
                    print "n:"+str(n)+" of "+str(coupon_count)

        coupon_string = coupon_string + "] issued."
        look_for_this = coupon_string

        if prn_info !=False:
            print "Expecting this string:"+look_for_this

        coupon_result = test_for_200(self, usrname, passwd, output, post_url,post_parameters, look_for_this, calling_test_function, prn_info )
        if prn_info!=False:
            print "Coupons_issued:"
            print coupon_result

        if coupon_result == None:
            Test_Msg("Successfully Issued Coupons for Valid Patient:"+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME)
            Test_Msg(look_for_this)
        else:
            Test_Msg("Failed to issue coupons for Valid Patient:"+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME)

        # now we need to try to assign a coupon that has already been issues
        # we should get an error like this:
        # "Coupons [&#39;Coupon # 227 had already been issued!&#39;] issued."

        Test_Msg("Trying to issue a duplicate coupon. We need to see an error")

        start_coupon = 227
        coupon_count = 3

        coupon_string = "Coupons [&#39;Coupon # "+str(start_coupon)+" had already been issued!&#39;] issued."
        post_parameters = {'starting_coupon':str(start_coupon),
                           'number_of_coupons':str(coupon_count)}

        look_for_this = coupon_string

        if prn_info !=False:
            print "Expecting this string:"+look_for_this

        coupon_result = test_for_200(self, usrname, passwd, output, post_url,post_parameters, look_for_this, calling_test_function, prn_info )
        if prn_info!=False:
            print "Coupons not issued:"
            print coupon_result

        if coupon_result == None:
            Test_Msg("Success: We failed to issue Coupons for Valid Patient:"+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME)
            Test_Msg(look_for_this)
        else:
            Test_Msg("Failed: We issued coupons for Valid Patient:"+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME)


        Test_End()

        return


