"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test locsetup".
"""
__author__ = 'mark'

from django.test import TestCase
from testutils import  Test_Start, Test_End, Test_Msg, test_for_200, test_for_200_with_get
import inspect
from datetime import date, datetime
from settings_test import *
# moving settings for testing to settings_test

"""
Tests for the Hive.locsetup app.

Run from root of hive app.
Run with "python manage.py test {app name}"
Example: python manage.py test locsetup >./test_results/locsetup_testresult.txt

Generate the test data
python manage.py dumpdata locsetup >
./apps/locsetup/fixtures/locsetup_testdata.json

"""
# Add module specific test variables here

# End of Module specific test variables section


class Locsetup_SimpleTest(TestCase):
    """Background to this test harness
       and prove the test harness works
    """

    # fixtures = ['accounts_test_data.json']

    def test_basic_addition_locsetup(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        Test_Start("1+1=2")
        answer = self.assertEqual(1 + 1, 2)
        Test_Msg("hive.apps.locsetup.tests.py")
        print "     Test Runtime: "+str(datetime.now())
        if answer == None:
            print "     Test Harness ready"
        else:
            print "     This Test Harness has a problem"
        Test_End("hive.apps.locsetup.tests.py")

        return

class Locsetup_Create_Setup_TestCase(TestCase):
    """"
    Test with no login, then with valid login
    Create a Location, select it, test for it on home page
    """

    fixtures = ['apps/intake/fixtures/intake_test_data.json',
                'apps/services/fixtures/services_testdata.json',
                'apps/accounts/fixtures/accounts_test_data.json',
                'apps/grants/fixtures/grants_test_data.json']

    def test_location_access_with_no_login(self):
        """
        Try to access /location/create without login - should get a 401 - Not Authorized
        """

        Test_Start()

        prn_info = False

        usrname = USERNAME_NO_ACCOUNT_TEST
        passwd = PASSWORD_NO_ACCOUNT_TEST
        output = []
        post_url = '/location/create'
        post_parameters = {}
        look_for_this = "login-box"
        called_by = inspect.getframeinfo(inspect.currentframe().f_back)[2]

        result = test_for_200_with_get(self, usrname, passwd, output, post_url,post_parameters, look_for_this, called_by, prn_info )
        if result==None:
            Test_Msg("     Successful Test - Access Failed - Not Logged in")
        else:
            Test_Msg("     Failed, got "+str(result)+" instead")

        Test_End()

        return

    def test_location_create_with_login(self):
        """
        Access with valid login account.
        Create a new location.
        Check for return to home page.
        """
        Test_Start()

        prn_info = False

        usrname = USERNAME_FOR_TEST
        passwd = PASSWORD_FOR_TEST
        output = []
        post_url = '/location/create'
        post_parameters = {'address1':'9876 Branch Ave SE',
                           'city':'Washington',
                           'state':'DC',
                           'zip':'20003',
                           'submit':'Save',
                           'ward':'6'
                           }

        # look_for_this = "9876 Branch Ave SE  DC, 20003 (Ward:6)"
        #            <span>9876 Branch Ave SE  DC, 20003 (Ward:6)</span>

        look_for_this = HOME_PAGE_TITLE_TEXT
        called_by = inspect.getframeinfo(inspect.currentframe().f_back)[2]


        result = test_for_200(self, usrname, passwd, output, post_url,post_parameters, look_for_this, called_by, prn_info )
        if result==None:
            Test_Msg("     Successful Test - Location Created: "+look_for_this)
        else:
            Test_Msg("     Failed, got "+str(result)+" instead")

        # now recheck the create page to see if location was added.
        post_parameters = {}
        look_for_this = "9876 Branch Ave SE  DC, 20003 (Ward:6)"

        result = test_for_200_with_get(self, usrname, passwd, output, post_url,post_parameters, look_for_this, called_by, prn_info )
        if result==None:
            Test_Msg("     Successful Test - Location Created: "+look_for_this)
        else:
            Test_Msg("     Failed, got "+str(result)+" instead")


        # Select a location
        post_url = '/location/select'
        post_parameters = {'locations':'2',
                           'submit':'Update',
                           'action':'/location/select'
                           }
        look_for_this = "<span>Sumner Rd. &amp; Martin Luther King Jr. Ave  SE  DC, 20004 (Ward:8)</span>"


        Test_Msg("Testing for Location Select:" + look_for_this)

        result2 = test_for_200(self,usrname,passwd,output,post_url,post_parameters,look_for_this, called_by, prn_info)
        if result2==None:
            Test_Msg("     Successful Test - selected:"+look_for_this)
        else:
            Test_Msg("     Failed, got "+str(result2)+" instead")

        Test_Msg()

        if prn_info!=False:
            print "List of Locations:"
            print LocationSetup.objects.all()

        return