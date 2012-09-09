"""
run "python manage.py test organizations>test_results/organizations_testresult.txt"

Author: Mark Scrimshire @ekivemark

"""

__author__ = 'mark'
from django.test import TestCase
from apps.accounts.models import User
from apps.organizations.models import Organization, Provider
from apps.intake.urls import *
from testutils import  Test_Start, Test_End, Test_Msg, test_for_401, test_for_200, test_for_200_with_get, check_permission, give_permission, remove_permission
from dateutils import date, datetime

import inspect
from settings_test import *

"""
Tests for the Hive.organizations app.

Run from root of hive app.
Run with "python manage.py test {app name}"
Example: python manage.py test organizations >./test_results/organizations_testresult.txt

Generate the test data
python manage.py dumpdata organizations --indent=4 >./apps/organizations/fixtures/testdata.json

"""
# Add module specific test variables here

# End of Module specific test variables section


# SimpleTest for a working Test Harness
# @unittest.skip
class Organizations_SimpleTest(TestCase):
    """Background to this test harness
    and prove the test harness works
    """

    fixtures =  ['apps/intake/fixtures/intake_test_data.json',
                 'apps/services/fixtures/services_testdata.json',
                 'apps/accounts/fixtures/accounts_test_data.json',
                 'apps/intake/fixtures/intake_inprocess.json',
                 'apps/grants/fixtures/grants_test_data.json',
                 'apps/organizations/fixtures/testdata.json']

    def test_organizations_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        Test_Start("1+1=2")
        answer = self.assertEqual(1 + 1, 2)
        Test_Msg("hive.apps.organizations.tests.py")
        print "     Test Runtime: "+str(datetime.today())
        if answer == None:
            print "     Test Harness ready"
        else:
            print "     This Test Harness has a problem"

        Test_End("hive.apps.organizations.tests.py")
        return

class Organizations_Invalid_Access_TestCase(TestCase):
    """
    Test that a non-tester gets blocked from accessing these pages.
    """
    fixtures =  ['apps/intake/fixtures/intake_test_data.json',
                 'apps/services/fixtures/services_testdata.json',
                 'apps/accounts/fixtures/accounts_test_data.json',
                 'apps/intake/fixtures/intake_inprocess.json',
                 'apps/grants/fixtures/grants_test_data.json',
                 'apps/organizations/fixtures/testdata.json']

    def test_no_login_access_(self):
        """
        Test that we get a 401 - Not Authorized
        """

        Test_Start()

        Test_Msg("Trying create organization")

        # debug print setting
        prn_info = False

        p = get_object_or_404(PatientProfile, patient_id=VALID_PATIENT_ID)
        if prn_info!=False:
            print p

        calling_test_function = inspect.getframeinfo(inspect.currentframe().f_back)[2]
        if prn_info!=False:
            print "calling:["+calling_test_function+"]"

        usrname = USERNAME_NO_ACCOUNT_TEST
        passwd = PASSWORD_NO_ACCOUNT_TEST
        output = []
        post_url = '/organizations/organization/search-by-name'
        post_parameters = {}

        look_for_this = "login-box"
        print check_permission(usrname)
        # print give_permission(usrname,permission_required)
        # print check_permission(usrname)

        Access_Authorised = test_for_200_with_get(self, usrname, passwd, output, post_url,post_parameters, look_for_this, calling_test_function, prn_info )
        if Access_Authorised == None:
            Test_Msg("Successful Access Test for no login:"+post_url)
        else:
            Test_Msg("Access Test Failed for no login:"+post_url)

        Test_Msg("Organization View")


        post_url = '/organizations/organization/view/1'

        Access_Authorised = test_for_200_with_get(self, usrname, passwd, output, post_url,post_parameters, look_for_this, calling_test_function, prn_info )
        if Access_Authorised == None:
            Test_Msg("Successful Access Test for no_login:"+post_url)
        else:
            Test_Msg("Access Test Failed for no_login:"+post_url)

        post_url = '/organizations/organization/create'

        Access_Authorised = test_for_200_with_get(self, usrname, passwd, output, post_url,post_parameters, look_for_this, calling_test_function, prn_info )
        if Access_Authorised == None:
            Test_Msg("Successful Access Test for no login:"+post_url)
        else:
            Test_Msg("Access Test Failed for no_login:"+post_url)

        Test_End()

        return

class Organizations_Access_TestCase(TestCase):
    """
    Use a valid access and check screens are accessible
    """

    fixtures =  ['apps/intake/fixtures/intake_test_data.json',
                 'apps/services/fixtures/services_testdata.json',
                 'apps/accounts/fixtures/accounts_test_data.json',
                 'apps/intake/fixtures/intake_inprocess.json',
                 'apps/grants/fixtures/grants_test_data.json',
                 'apps/organizations/fixtures/testdata.json']


    def test_search(self):
        """
        Do an Organization Search
        """

        Test_Start()

        Test_Msg("Trying search organization")

        # debug print setting
        prn_info = False

        p = get_object_or_404(PatientProfile, patient_id=VALID_PATIENT_ID)
        if prn_info!=False:
            print p

        calling_test_function = inspect.getframeinfo(inspect.currentframe().f_back)[2]
        if prn_info!=False:
            print "calling:["+calling_test_function+"]"

        usrname = USERNAME_FOR_TEST
        passwd = PASSWORD_FOR_TEST
        output = []
        post_url = '/organizations/organization/search-by-name'
        post_parameters = {'organization_type':"ANY"
        }

        look_for_this = "Matches For"
        print check_permission(usrname)
        # print give_permission(usrname,permission_required)
        # print check_permission(usrname)

        Access_Authorised = test_for_200(self, usrname, passwd, output, post_url,post_parameters, look_for_this, calling_test_function, prn_info )
        if Access_Authorised == None:
            Test_Msg("Successful search:"+post_url+" "+look_for_this)
        else:
            Test_Msg("Failed search:"+post_url+" "+look_for_this)



        Test_End()

        return

    def test_view(self):
        """
        Look at an organization record
        """

        Test_Start()

        Test_Msg("Trying organization view")

        # debug print setting
        prn_info = False

        p = get_object_or_404(PatientProfile, patient_id=VALID_PATIENT_ID)
        if prn_info!=False:
            print p

        get_record = 1
        o = get_object_or_404(Organization, pk=get_record)
        org_name = o.name
        if prn_info!=False:
            print o


        calling_test_function = inspect.getframeinfo(inspect.currentframe().f_back)[2]
        if prn_info!=False:
            print "calling:["+calling_test_function+"]"

        usrname = USERNAME_FOR_TEST
        passwd = PASSWORD_FOR_TEST
        output = []
        post_url = '/organizations/organization/view/'+str(get_record)
        post_parameters = {}

        look_for_this = org_name
        print check_permission(usrname)
        # print give_permission(usrname,permission_required)
        # print check_permission(usrname)

        Access_Authorised = test_for_200_with_get(self, usrname, passwd, output, post_url,post_parameters, look_for_this, calling_test_function, prn_info )
        if Access_Authorised == None:
            Test_Msg("Successful search:"+post_url+" "+look_for_this)
        else:
            Test_Msg("Failed search:"+post_url+" "+look_for_this)



        Test_End()

        return

    def test_create(self):
        """
        Create an organization record
        """

        Test_Start()

        Test_Msg("Trying Create organization")

        # debug print setting
        prn_info = False

        today = datetime.today().strftime("%Y-%m-%d")
        print today

        p = get_object_or_404(PatientProfile, patient_id=VALID_PATIENT_ID)
        if prn_info!=False:
            print p

        get_record = 1
        o = get_object_or_404(Organization, pk=get_record)
        org_name = o.name
        if prn_info!=False:
            print o


        calling_test_function = inspect.getframeinfo(inspect.currentframe().f_back)[2]
        if prn_info!=False:
            print "calling:["+calling_test_function+"]"

        usrname = USERNAME_FOR_TEST
        passwd = PASSWORD_FOR_TEST
        output = []
        post_url = '/organizations/organization/create'
        post_parameters = {
            'name'          :"Fictional Place",
            'slug'          :"Made up name",
            'org_type'      :"FREE-CLINIC",
            'address1'      :"123 No St",
            'city'          :"Washington",
            'state'         :"DC",
            'zip'           :"20001",
            'note'          :"Made up record - safe to delete",
            'creation_date' :today,
            }

        look_for_this = "A new organization record was created"
        print check_permission(usrname)
        # print give_permission(usrname,permission_required)
        # print check_permission(usrname)

        Access_Authorised = test_for_200(self, usrname, passwd, output, post_url,post_parameters, look_for_this, calling_test_function, prn_info )
        if Access_Authorised == None:
            Test_Msg("Successful create:"+post_url+" "+look_for_this)
        else:
            Test_Msg("Failed create:"+post_url+" "+look_for_this)



        Test_End()

        return

class Organizations_Invalid_Access_TestCase(TestCase):
    """
    Test that a non-tester gets blocked from accessing these pages.
    """
    fixtures =  ['apps/intake/fixtures/intake_test_data.json',
                 'apps/services/fixtures/services_testdata.json',
                 'apps/accounts/fixtures/accounts_test_data.json',
                 'apps/intake/fixtures/intake_inprocess.json',
                 'apps/grants/fixtures/grants_test_data.json',
                 'apps/organizations/fixtures/testdata.json']

    def test_no_login_access_(self):
        """
        Test that we get a 401 - Not Authorized
        """

        Test_Start()

        Test_Msg("Trying create organization")

        # debug print setting
        prn_info = False

        p = get_object_or_404(PatientProfile, patient_id=VALID_PATIENT_ID)
        if prn_info!=False:
            print p

        calling_test_function = inspect.getframeinfo(inspect.currentframe().f_back)[2]
        if prn_info!=False:
            print "calling:["+calling_test_function+"]"

        usrname = USERNAME_NO_ACCOUNT_TEST
        passwd = PASSWORD_NO_ACCOUNT_TEST
        output = []
        post_url = '/organizations/organization/search-by-name'
        post_parameters = {}

        look_for_this = "login-box"
        print check_permission(usrname)
        # print give_permission(usrname,permission_required)
        # print check_permission(usrname)

        Access_Authorised = test_for_200_with_get(self, usrname, passwd, output, post_url,post_parameters, look_for_this, calling_test_function, prn_info )
        if Access_Authorised == None:
            Test_Msg("Successful Access Test for no login:"+post_url)
        else:
            Test_Msg("Access Test Failed for no login:"+post_url)

        Test_Msg("Organization View")


        post_url = '/organizations/organization/view/1'

        Access_Authorised = test_for_200_with_get(self, usrname, passwd, output, post_url,post_parameters, look_for_this, calling_test_function, prn_info )
        if Access_Authorised == None:
            Test_Msg("Successful Access Test for no_login:"+post_url)
        else:
            Test_Msg("Access Test Failed for no_login:"+post_url)

        post_url = '/organizations/organization/create'

        Access_Authorised = test_for_200_with_get(self, usrname, passwd, output, post_url,post_parameters, look_for_this, calling_test_function, prn_info )
        if Access_Authorised == None:
            Test_Msg("Successful Access Test for no login:"+post_url)
        else:
            Test_Msg("Access Test Failed for no_login:"+post_url)

        Test_End()

        return

class Organizations_Provider_Access_TestCase(TestCase):
    """
    Use a valid access and check screens are accessible
    """

    fixtures =  ['apps/intake/fixtures/intake_test_data.json',
                 'apps/services/fixtures/services_testdata.json',
                 'apps/accounts/fixtures/accounts_test_data.json',
                 'apps/intake/fixtures/intake_inprocess.json',
                 'apps/grants/fixtures/grants_test_data.json',
                 'apps/organizations/fixtures/testdata.json']


    def test_provider_search(self):
        """
        Do a Provider Search
        """

        Test_Start()

        Test_Msg("Trying search provider")

        # debug print setting
        prn_info = False

        p = get_object_or_404(PatientProfile, patient_id=VALID_PATIENT_ID)
        if prn_info!=False:
            print p

        calling_test_function = inspect.getframeinfo(inspect.currentframe().f_back)[2]
        if prn_info!=False:
            print "calling:["+calling_test_function+"]"

        usrname = USERNAME_FOR_TEST
        passwd = PASSWORD_FOR_TEST
        output = []
        post_url = '/organizations/provider/search-by-name'
        post_parameters = {'last_name':""
        }

        look_for_this = "Match"
        print check_permission(usrname)
        # print give_permission(usrname,permission_required)
        # print check_permission(usrname)

        Access_Authorised = test_for_200(self, usrname, passwd, output, post_url,post_parameters, look_for_this, calling_test_function, prn_info )
        if Access_Authorised == None:
            Test_Msg("Successful search:"+post_url+" "+look_for_this)
        else:
            Test_Msg("Failed search:"+post_url+" "+look_for_this)



        Test_End()

        return

    def test_provider_view(self):
        """
        Look at a provider record
        """

        Test_Start()

        Test_Msg("Trying provider view")

        # debug print setting
        prn_info = False

        p = get_object_or_404(PatientProfile, patient_id=VALID_PATIENT_ID)
        if prn_info!=False:
            print p

        get_record = 1
        o = get_object_or_404(Provider, pk=get_record)
        provider_name = o.last_name
        if prn_info!=False:
            print o


        calling_test_function = inspect.getframeinfo(inspect.currentframe().f_back)[2]
        if prn_info!=False:
            print "calling:["+calling_test_function+"]"

        usrname = USERNAME_FOR_TEST
        passwd = PASSWORD_FOR_TEST
        output = []
        post_url = '/organizations/provider/view/'+str(get_record)
        post_parameters = {}

        look_for_this = provider_name
        print check_permission(usrname)
        # print give_permission(usrname,permission_required)
        # print check_permission(usrname)

        Access_Authorised = test_for_200_with_get(self, usrname, passwd, output, post_url,post_parameters, look_for_this, calling_test_function, prn_info )
        if Access_Authorised == None:
            Test_Msg("Successful search:"+post_url+" "+look_for_this)
        else:
            Test_Msg("Failed search:"+post_url+" "+look_for_this)



        Test_End()

        return



    def test_create(self):
        """
        Create an organization record
        """

        Test_Start()

        Test_Msg("Trying Create Provider")

        # debug print setting
        prn_info = False

        today = datetime.today().strftime("%Y-%m-%d")
        print today

        p = get_object_or_404(PatientProfile, patient_id=VALID_PATIENT_ID)
        if prn_info!=False:
            print p

        get_record = 1
        o = get_object_or_404(Provider, pk=get_record)
        provider_name = o.last_name
        if prn_info!=False:
            print o


        calling_test_function = inspect.getframeinfo(inspect.currentframe().f_back)[2]
        if prn_info!=False:
            print "calling:["+calling_test_function+"]"

        usrname = USERNAME_FOR_TEST
        passwd = PASSWORD_FOR_TEST
        output = []
        post_url = '/organizations/provider/create'
        post_parameters = {
            'first_name'    :"Hawkeye",
            'last_name'     :"Pierce",
            'slug'          :"Made up name",
            'organization'  :"4",
            'address1'      :"4077 No St",
            'city'          :"Washington",
            'state'         :"DC",
            'zip'           :"20001",
            'note'          :"Made up record - safe to delete",
            'creation_date' :today,
            }

        look_for_this = "A new provider record was created"
        print check_permission(usrname)
        # print give_permission(usrname,permission_required)
        # print check_permission(usrname)

        Access_Authorised = test_for_200(self, usrname, passwd, output, post_url,post_parameters, look_for_this, calling_test_function, prn_info )
        if Access_Authorised == None:
            Test_Msg("Successful create:"+post_url+" "+look_for_this)
        else:
            Test_Msg("Failed create:"+post_url+" "+look_for_this)



        Test_End()

        return

class Organizations_Provider_Invalid_Access_TestCase(TestCase):
    """
    Test that a non-tester gets blocked from accessing these pages.
    """
    fixtures =  ['apps/intake/fixtures/intake_test_data.json',
                 'apps/services/fixtures/services_testdata.json',
                 'apps/accounts/fixtures/accounts_test_data.json',
                 'apps/intake/fixtures/intake_inprocess.json',
                 'apps/grants/fixtures/grants_test_data.json',
                 'apps/organizations/fixtures/testdata.json']

    def test_provider_no_login_access_(self):
        """
        Test that we get a 401 - Not Authorized
        """

        Test_Start()

        Test_Msg("Trying search provider")

        # debug print setting
        prn_info = False

        p = get_object_or_404(PatientProfile, patient_id=VALID_PATIENT_ID)
        if prn_info!=False:
            print p

        calling_test_function = inspect.getframeinfo(inspect.currentframe().f_back)[2]
        if prn_info!=False:
            print "calling:["+calling_test_function+"]"

        usrname = USERNAME_NO_ACCOUNT_TEST
        passwd = PASSWORD_NO_ACCOUNT_TEST
        output = []
        post_url = '/organizations/provider/search-by-name'
        post_parameters = {}

        look_for_this = "login-box"
        print check_permission(usrname)
        # print give_permission(usrname,permission_required)
        # print check_permission(usrname)

        Access_Authorised = test_for_200_with_get(self, usrname, passwd, output, post_url,post_parameters, look_for_this, calling_test_function, prn_info )
        if Access_Authorised == None:
            Test_Msg("Successful Access Test for no login:"+post_url)
        else:
            Test_Msg("Access Test Failed for no login:"+post_url)

        Test_Msg("Provider View")


        post_url = '/organizations/provider/view/1'

        Access_Authorised = test_for_200_with_get(self, usrname, passwd, output, post_url,post_parameters, look_for_this, calling_test_function, prn_info )
        if Access_Authorised == None:
            Test_Msg("Successful Access Test for no_login:"+post_url)
        else:
            Test_Msg("Access Test Failed for no_login:"+post_url)

        post_url = '/organizations/provider/create'

        Access_Authorised = test_for_200_with_get(self, usrname, passwd, output, post_url,post_parameters, look_for_this, calling_test_function, prn_info )
        if Access_Authorised == None:
            Test_Msg("Successful Access Test for no login:"+post_url)
        else:
            Test_Msg("Access Test Failed for no_login:"+post_url)

        Test_End()

        return

