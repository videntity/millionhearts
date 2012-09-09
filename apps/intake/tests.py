"""
run "python manage.py test intake"

Author: Mark Scrimshire @ekivemark

"""
from django.test import TestCase
from django.test.client import Client
from datetime import date,timedelta, datetime
from apps.accounts.models import User
from apps.intake.urls import *
from testutils import login_to_hive,Test_Start, Test_End, Test_Msg, test_for_401, test_for_200, test_for_200_with_get, test_for_404_with_get
import inspect
from settings_test import *
# moving settings for testing to settings_test

"""
Tests for the Hive.intake app.

Run from root of hive app.
Run with "python manage.py test {app name}"
Example: python manage.py test intake >./test_results/intake_testresult.txt

Generate the test data
python manage.py dumpdata intake --indent=4 >./apps/intake/fixtures/intake_testdata.json

"""
# Add module specific test variables here

# End of Module specific test variables section


# SimpleTest for a working Test Harness
# @unittest.skip
class intake_SimpleTest(TestCase):
    """Background to this test harness
    and prove the test harness works
    """

    fixtures = ['apps/intake/fixtures/intake_test_data.json',
                'apps/services/fixtures/services_testdata.json',
                'apps/accounts/fixtures/accounts_test_data.json',
                'apps/grants/fixtures/grants_test_data.json']

    def test_home_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        Test_Start("1+1=2")
        answer = self.assertEqual(1 + 1, 2)
        Test_Msg("hive.apps.intake.tests.py")
        print "     Test Runtime: "+str(datetime.datetime.now())
        if answer == None:
            print "     Test Harness ready"
        else:
            print "     This Test Harness has a problem"

        Test_End("hive.apps.intake.tests.py")
        return


class Test_intake_ValidTester(TestCase):
    """ Can we get a tester user logged in
    """

    fixtures = ['apps/intake/fixtures/intake_test_data.json',
                'apps/services/fixtures/services_testdata.json',
                'apps/accounts/fixtures/accounts_test_data.json',
                'apps/grants/fixtures/grants_test_data.json']

    def setUp_Test_For_Valid_Tester(self):
        Test_Start()
        Test_Msg("TestForValidUser-setUp - calling login_to_hive")
        setup_access = login_to_hive(USERNAME_FOR_TEST,
            PASSWORD_FOR_TEST,SMSCODE_FOR_TEST)
        Test_Msg("Login to Hive returned:"+str(setup_access)+" \n      for User:"+USERNAME_FOR_TEST)

        Test_End()
        return

    def test_intake_base_page_for_tester(self):
        """
        Testing for login on home page by tester account
        """
        Test_Start()
        self.client = Client()
        self.client.login(username=USERNAME_FOR_TEST,password=PASSWORD_FOR_TEST)
        attempt_login = login_to_hive(USERNAME_FOR_TEST,
            PASSWORD_FOR_TEST,SMSCODE_FOR_TEST)
        print "login result:"+str(attempt_login)
        Test_Msg("Login to Hive returned:"+str(attempt_login)+" \n     for User:"+USERNAME_FOR_TEST)

        response = self.client.get('/',follow=True)
        self.assertEqual(response.status_code, 200)

        user_account = User.objects.get(username=USERNAME_FOR_TEST)
        who_is_logged_in = 'Welcome ' + user_account.first_name+" "+user_account.last_name

        # print response
        result = self.assertContains(response,who_is_logged_in)
        if result==None:
            print "result:"+str(result)+" Login Succeeded"
        else:
            print "result:"+str(result)+" Login Failed"
        Test_End()
        return

    def test_intake_base_page_for_non_tester(self):
        """
        Testing for login on home page for non tester account
        """
        Test_Start()
        self.client = Client()
        self.client.login(username=USERNAME_NOT_TEST,password=PASSWORD_NOT_TEST)
        attempt_login = login_to_hive(USERNAME_NOT_TEST,
            PASSWORD_NOT_TEST,SMSCODE_NOT_TEST)
        print "login result:"+str(attempt_login)
        Test_Msg("Login to Hive returned:"+str(attempt_login)+" \n     for User:"+USERNAME_NOT_TEST)

        response = self.client.get('/',follow=True)
        self.assertEqual(response.status_code, 200)

        user_account = User.objects.get(username=USERNAME_NOT_TEST)
        who_is_logged_in = 'Welcome ' + user_account.first_name+" "+user_account.last_name

        # print response
        result = self.assertContains(response,who_is_logged_in)
        if result==None:
            print "result:"+str(result)+" Login Succeeded"
        else:
            print "result:"+str(result)+" Login Failed"
        Test_End()
        return

# Locator
    # intake_locator_TestCase(TestCase):
    # Failed Access Without Testers Permission
    # Access With Testers Permission and
    #   Use valid pat_id
    #   Use invalid pat_id

    # Completed 12/27/2011

# Initial_Intake
    # Access Without Testers Permission
    # Access With Testers Permission

    # Completed 12/27/2011

# Search By Name
    # Access Without Testers Permission
    # Access With Testers Permission
        # Use valid name
        # Use invalid name

    # Completed 12/28/2011

# Search By SSN
    # Access Without Testers Permission
    # Access With Testers Permission
        # Use valid last 4 of ssn
        # Use invalid last 4 of ssn
        # test for error with alpha
        # test for error with less than 4 digits
        # test for error with more than 4 digits
        # test for 4 digits

    # Completed 12/29/2011

# View_Locator
    # Access Without Testers Permission
    # Access With Testers Permission
        # Use valid pat_id
        # Use invalid pat_id

    # Completed 12/30/2011

# Worker_Signature
    # Access Without Testers Permission
    # Access With Testers Permission
        # Use valid pat_id
        # Use invalid pat_id

    # Global s2i not defined error

# Patient_Signature
    # Access Without Testers Permission
    # Access With Testers Permission
        # Use valid pat_id
        # Use invalid pat_id

    # Global s2i not defined error

# In_process_List
    # Access Without Testers Permission
    # Access With Testers Permission

    # Completed 12/31/2011

class intake_locator_TestCase(TestCase):
    """ Search for a patient by their Patient ID via intake_locator
    """

    fixtures = ['apps/intake/fixtures/intake_test_data.json',
                'apps/services/fixtures/services_testdata.json',
                'apps/accounts/fixtures/accounts_test_data.json',
                'apps/grants/fixtures/grants_test_data.json']

    def test_get_record_for_valid_pat_id_with_non_tester(self):
        """ GET completed should return a response
            Non Tester should not have access
        """
        Test_Start()

        prn_info = False

        # We should search for this
        p = get_object_or_404(PatientProfile, patient_id=VALID_PATIENT_ID)

        if prn_info!=False:
            print p

        self.client = Client()
        self.client.login(username=USERNAME_NOT_TEST,password=PASSWORD_NOT_TEST)
        attempt_login = login_to_hive(USERNAME_NOT_TEST,PASSWORD_NOT_TEST,SMSCODE_NOT_TEST)
        print "login result:"+str(attempt_login)
        print "get /intake/locator/"+VALID_PATIENT_ID
        response = self.client.get('/intake/locator/'+VALID_PATIENT_ID,follow=True)
        got_code = self.assertEqual(response.status_code, 401)

        # print response.content
        # check response details
        print "%s = %s" % (response.status_code,'401')
        Look_For_What = PERMISSION_DENIED
        print response.content

        Test_End()
        return

    def test_get_record_for_valid_pat_id_with_tester(self):
        """ GET completed should return a response
            Tester should have access
        """
        Test_Start()

        prn_info = False

        # We should search for this
        p = get_object_or_404(PatientProfile, patient_id=VALID_PATIENT_ID)

        if prn_info!=False:
            print p

        self.client = Client()
        self.client.login(username=USERNAME_FOR_TEST,password=PASSWORD_FOR_TEST)
        attempt_login = login_to_hive(USERNAME_FOR_TEST,
            PASSWORD_FOR_TEST,SMSCODE_FOR_TEST)
        print "login result:"+str(attempt_login)
        print "get /intake/locator/"+VALID_PATIENT_ID
        response = self.client.get('/intake/locator/'+VALID_PATIENT_ID,follow=True)
        got_code = self.assertEqual(response.status_code, 200)


        # print response.content
        # check response details
        print "%s = %s" % (response.status_code,'200')
        print "checking for VALID_PATIENT_ID in /intake/locator/"+VALID_PATIENT_ID
        Look_For_What = "(" + VALID_PATIENT_ID + ")"
        print "Checked for "+Look_For_What
        try:
            result = self.assertContains(response,Look_For_What)
            # result = "skipped"
            print "None is good: Outcome =" + str(result)
        except:
            print "No match in Page /intake/locator/"+VALID_PATIENT_ID
            print response.content
        Test_End()
        return

    def test_get_record_for_invalid_pat_id_with_tester(self):
        """ GET completed should return a response
            Tester should have access but with an invalid pat_id
        """
        Test_Start()

        prn_info = False
        # We should search for this
        p = get_object_or_404(PatientProfile, patient_id=VALID_PATIENT_ID)

        if prn_info!=False:
            print p

        self.client = Client()
        self.client.login(username=USERNAME_FOR_TEST,password=PASSWORD_FOR_TEST)
        attempt_login = login_to_hive(USERNAME_FOR_TEST,
            PASSWORD_FOR_TEST,SMSCODE_FOR_TEST)
        print "login result:"+str(attempt_login)
        print "get /intake/locator/"+INVALID_PATIENT_ID
        response = self.client.get('/intake/locator/'+INVALID_PATIENT_ID,follow=True)
        got_code = self.assertEqual(response.status_code, 404)


        # print response.content
        # check response details
        print "%s = %s" % (response.status_code,'404')
        Test_Msg("Checked for INVALID_PATIENT_ID in\n     /intake/locator/"+INVALID_PATIENT_ID+"\n     and got Expected 404")

        Test_End()
        return



class initial_intake_test(TestCase):
    """
    initial_intake_test
    """

    fixtures = ['apps/intake/fixtures/intake_test_data.json',
                'apps/services/fixtures/services_testdata.json',
                'apps/accounts/fixtures/accounts_test_data.json',
                'apps/grants/fixtures/grants_test_data.json']


    def iit_setUp(self):
        # Every test needs a client.
        Test_Start("Setting up client for ultra_simple_test")
        self.client = Client()
        # setup_access = login_to_hive(USERNAME_FOR_TEST,
        #    PASSWORD_FOR_TEST,SMSCODE_FOR_TEST)

        response = self.client.post('/accounts/smscode/',
                                    {'username': USERNAME_FOR_TEST,
                                     'password': PASSWORD_FOR_TEST,
                                     'smscode':SMSCODE_FOR_TEST},
                                     follow=True)
        access = self.client.login(username=USERNAME_FOR_TEST,
                                    password=PASSWORD_FOR_TEST)
        print access
        print response.status_code
        if response.status_code == '302':
            print "returned status_code:302"
            print "testing for - Welcome" + USERNAME_FOR_TEST
            test_for_access = 'Welcome ' + USERNAME_FOR_TEST
            evaluator = self.client.get('/',follow=True)
            print "evaluator:"
            print evaluator
            eval_result = evaluator.assertContains(evaluator.content,
                            test_for_access)
            print "eval_result:"
            print eval_result
            if eval_result == True:
                print eval_result
                setup_access=True
            else:
                setup_access=False
        else:
            setup_access=False

        Test_Msg("login attempt:"+str(setup_access))

        Test_End()
        return

    def test_initial_intake_with_non_tester(self):
        """
        Test for Non Tester Permission in Intake App
        Expect a failure - Not Authorized
        """
        Test_Start()

        prn_info = False

        # Issue a GET request.
        access = self.client.login(username=USERNAME_NOT_TEST,password=PASSWORD_NOT_TEST)
        # print access
        response = self.client.get('/intake/create',follow=True)

        if prn_info!=False:
            print response.content
            print "checking for code 401"
        # Check that the response is 401.

        got_code = self.assertEqual(response.status_code, 401)

        # print response.content
        # check response details
        print "%s = %s" % (response.status_code,'401')
        Look_For_What = PERMISSION_DENIED
        print response.content
        Test_Msg("Successful Test")
        Test_End()

        return

    def test_quick_intake_with_non_tester(self):
        """
        Test quickintake is blocked to non-testers
        """

        Test_Start("Testing Quick Intake - With Non-Tester")

        prn_info = False

        # We should search for this
        p = get_object_or_404(PatientProfile, patient_id=VALID_PATIENT_ID)
        if prn_info!=False:
            print p

        calling_test_function = inspect.getframeinfo(inspect.currentframe().f_back)[2]

        if prn_info!=False:
            print "calling:["+calling_test_function+"]"

        usrname = USERNAME_NOT_TEST
        passwd=PASSWORD_NOT_TEST
        output = []
        post_url = '/intake/quickintake'
        post_parameters = {}

        Access_Authorised = test_for_401(self, usrname, passwd, output, post_url,post_parameters, calling_test_function, prn_info )
        if Access_Authorised == None:
            Test_Msg("Successful Test for 401")
        else:
            Test_Msg("Test Failed for 401")

        Test_End()


        return

    def test_initial_intake_with_tester(self):
        """
        Test for Tester Permission in Intake App
        Expect Success
        """
        Test_Start()

        prn_info = False

        # Issue a GET request.
        access = self.client.login(username=USERNAME_FOR_TEST,password=PASSWORD_FOR_TEST)
        # print access
        response = self.client.get('/intake/create',follow=True)

        # print response.content
        # check response details
        print "%s = %s" % (response.status_code,'200')
        Test_Msg("Checking for Initial Intake Form in /intake/create")
        Look_For_What = "Initial Intake"

        try:
            result = self.assertContains(response,Look_For_What)
            # result = "skipped"
            Test_Msg( "None is good: Outcome =" + str(result)+"\n     Successful Test")
        except:
            print "No match in Page /intake/create"
            print response.content
        Test_End()

        return

    def test_quick_intake_with_tester(self):
        """
        Test the Quick intake form with a valid Tester Id
        """

        Test_Start("Testing Quick Intake - With Non-Tester")

        prn_info = False

        # We should search for this
        p = get_object_or_404(PatientProfile, patient_id=VALID_PATIENT_ID)
        if prn_info!=False:
            print p

        calling_test_function = inspect.getframeinfo(inspect.currentframe().f_back)[2]

        if prn_info!=False:
            print "calling:["+calling_test_function+"]"

        usrname = USERNAME_FOR_TEST
        passwd=PASSWORD_FOR_TEST
        output = []
        post_url = '/intake/quickintake'
        post_parameters = {
                           'first_name':VALID_INPROCESS_FIRSTNAME,
                           'last_name':VALID_INPROCESS_LASTNAME,
                           'last_4_ssn':VALID_INPROCESS_LAST_4_SSN,
                           'reciept_privacy_practices': "",
                           'patient_signature':PATIENT_SIGNATURE,
                           }
        look_for = "There are errors"

        result = test_for_200(self, usrname, passwd, output, post_url,post_parameters, look_for, calling_test_function, prn_info )

        if result == None:
            Test_Msg("Successful Test for Error trapping "+post_url)
        else:
            Test_Msg("Test Failed for Error trapping"+post_url)

        post_parameters = {
                           'first_name':VALID_INPROCESS_FIRSTNAME,
                           'last_name':VALID_INPROCESS_LASTNAME,
                           'last_4_ssn':VALID_INPROCESS_LAST_4_SSN,
                           'reciept_privacy_practices': True,
                           'patient_signature':PATIENT_SIGNATURE,
                           }

        prn_info = False

        look_for = "Successfully added a new member"

        result = test_for_200(self, usrname, passwd, output, post_url,post_parameters, look_for, calling_test_function, prn_info )

        if result == None:
            Test_Msg("Successful Test for Quick Intake "+post_url +" - "+VALID_INPROCESS_FIRSTNAME+" "+VALID_INPROCESS_LASTNAME+" ("+VALID_INPROCESS_LAST_4_SSN+")")
        else:
            Test_Msg("Test Failed for Quick Intake"+post_url +" - "+VALID_INPROCESS_FIRSTNAME+" "+VALID_INPROCESS_LASTNAME+" ("+VALID_INPROCESS_LAST_4_SSN+")")


        Test_End()


        return



class Search_By_Name_TestCase(TestCase):
    """
    Search By Name
    Failed Search with Non Tester Permission
    Successful Search with Tester Permission and valid search name
    Failed Search with Tester Permission and invalid search name
    """

    fixtures = ['apps/intake/fixtures/intake_test_data.json',
                'apps/services/fixtures/services_testdata.json',
                'apps/accounts/fixtures/accounts_test_data.json',
                'apps/grants/fixtures/grants_test_data.json']


    def test_search_by_name_with_non_tester(self):
        """
        Failed search with Non Tester Permission
        """

        Test_Start()

        prn_info = False

        # We should search for this
        p = get_object_or_404(PatientProfile, patient_id=VALID_PATIENT_ID)

        if prn_info!=False:
            print p
        # Issue a GET request.
        access = self.client.login(username=USERNAME_NOT_TEST,password=PASSWORD_NOT_TEST)
        # print access
        response = self.client.get('/intake/search-by-name',{'first_name':VALID_PATIENT_FIRSTNAME,'last_name':VALID_PATIENT_LASTNAME},follow=True)
        # print response.content
        # print "checking for code 401"
        # Check that the response is 401.

        got_code = self.assertEqual(response.status_code, 401)

        # print response.content
        # check response details
        print "%s = %s" % (response.status_code,'401')
        Look_For_What = PERMISSION_DENIED
        print response.content
        Test_Msg("Successful Test")

        Test_End()
        return

    def test_search_by_name_with_tester_and_valid_name(self):
        """
        Successful Search with Tester Permission and Valid Search Name
        """
        Test_Start()

        prn_info = False

        # We should search for this
        p = get_object_or_404(PatientProfile, patient_id=VALID_PATIENT_ID)

        if prn_info!=False:
            print p

        # Issue a GET request.
        access = self.client.login(username=USERNAME_FOR_TEST,password=PASSWORD_FOR_TEST)

        if prn_info!=False:
            print access

        response = self.client.post('/intake/search-by-name',{'first_name':VALID_PATIENT_FIRSTNAME,'last_name':VALID_PATIENT_LASTNAME},follow=True)


        # print response.content
        # check response details
        print "%s = %s" % (response.status_code,'200')
        Test_Msg("Checking for Valid Patient Search By Name:"+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME)
        Look_For_What = VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME
        result = None
        try:
            result = self.assertContains(response,Look_For_What)
            # result = "skipped"
            Test_Msg( "None is good: Outcome =" + str(result)+"\n     Successful Test")
        except result != None:
            print "No match in Page /intake/search-by-name"
            print response.content
        Test_End()
        return

    def test_search_by_name_with_tester_and_invalid_name(self):
        """
        Failed Search with Tester Permission and Invalid Search Name
        """
        Test_Start()

        prn_info = False

        # We are not searching for this
        p = get_object_or_404(PatientProfile, patient_id=VALID_PATIENT_ID)

        if prn_info!=False:
            print p


        # Issue a GET request.
        access = self.client.login(username=USERNAME_FOR_TEST,password=PASSWORD_FOR_TEST)

        if prn_info!=False:
            print access

        response = self.client.post('/intake/search-by-name',{'first_name':INVALID_PATIENT_FIRSTNAME,'last_name':INVALID_PATIENT_LASTNAME},follow=True)

        if prn_info!=False:
            print response.content
            # check response details

        print "%s = %s" % (response.status_code,'200')
        Test_Msg("Checking for Invalid Patient Search By Name:"+INVALID_PATIENT_FIRSTNAME+" "+INVALID_PATIENT_LASTNAME)
        Look_For_What = "0 Matches For "
        result = None
        try:
            result = self.assertContains(response,Look_For_What)
            # result = "skipped"
            Test_Msg( "None is good: Outcome =" + str(result)+"\n     Successful Test")
        except result != None:
            print "No match in Page /intake/search-by-name"
            print response.content
        Test_End()
        return


# Write some test documentation
class Prelim_to_test(TestCase):
    """Background to this test harness
    """

    fixtures = ['apps/intake/fixtures/intake_test_data.json',
                'apps/services/fixtures/services_testdata.json',
                'apps/accounts/fixtures/accounts_test_data.json',
                'apps/grants/fixtures/grants_test_data.json']

    def Inform_Prelim_to_Test(self):
        """Record some information about this test harness
        """
        self.client=Client()
        Test_Start("python manage.py test intake")
        Test_Msg("hive.apps.intake.tests.py")
        print "    Test Runtime: "+str(datetime.datetime.now())
        answer = self.assertEqual(12,1)
        if answer == None:
            print "Test Harness ready"
        else:
            print "This Test Harness has a problem"
        Test_End("hive.apps.intake.tests.py")
        return

class Search_by_ssn_TestCase(TestCase):
    """
    Search using last 4 digits of SSN
    """
    # Search By SSN
        # Access Without Testers Permission
        # Access With Testers Permission
            # Use valid last 4 of ssn
                # test for 4 digits
            # Use invalid last 4 of ssn
                # test for error with alpha
                # test for error with less than 4 digits
                # test for error with more than 4 digits

    fixtures = ['apps/intake/fixtures/intake_test_data.json',
                'apps/services/fixtures/services_testdata.json',
                'apps/accounts/fixtures/accounts_test_data.json',
                'apps/grants/fixtures/grants_test_data.json']

    def test_search_by_SSN_with_non_tester(self):
        """
        Failed search with Non Tester Permission
        """
        Test_Start()

        prn_info = False

        # We should search for this
        p = get_object_or_404(PatientProfile, patient_id=VALID_PATIENT_ID)

        if prn_info!=False:
            print p

        # Issue a GET request.
        access = self.client.login(username=USERNAME_NOT_TEST,password=PASSWORD_NOT_TEST)

        if prn_info!=False:
            print access

        response = self.client.post('/intake/search-by-ssn',{'last_4_ssn':VALID_LAST_4_SSN},follow=True)

        if prn_info!=False:
            print response.content
            print "checking for code 401"
            # Check that the response is 401.

        got_code = self.assertEqual(response.status_code, 401)

        # print response.content
        # check response details
        print "%s = %s" % (response.status_code,'401')
        Look_For_What = PERMISSION_DENIED
        print response.content
        Test_Msg("Successful Test")

        Test_End()

        return

    def test_search_by_SSN_with_non_Tester_401(self):
        """
        Failed search with Non Tester Permission
        Using call to testutils.test_for_401(usrname, passwd, output, post_url,post_parameters )
        """

        Test_Start()

        prn_info = False

        # We should search for this
        p = get_object_or_404(PatientProfile, patient_id=VALID_PATIENT_ID)
        if prn_info!=False:
            print p

        calling_test_function = inspect.getframeinfo(inspect.currentframe().f_back)[2]

        if prn_info!=False:
            print "calling:["+calling_test_function+"]"

        usrname = USERNAME_NOT_TEST
        passwd=PASSWORD_NOT_TEST
        output = []
        post_url = '/intake/search-by-ssn'
        post_parameters = {'last_4_ssn':VALID_LAST_4_SSN}

        Access_Authorised = test_for_401(self, usrname, passwd, output, post_url,post_parameters, calling_test_function, prn_info )
        if Access_Authorised == None:
            Test_Msg("Successful Test for 401")
        else:
            Test_Msg("Test Failed for 401")

        Test_End()

        return



    def test_search_by_SSN_with_tester_and_valid_name(self):
        """
        Successful Search with Tester Permission and Valid Search SSN
        """
        Test_Start()

        prn_info = False

        # We should search for this
        p = get_object_or_404(PatientProfile, patient_id=VALID_PATIENT_ID)

        if prn_info!=False:
            print p


        # Issue a GET request.
        access = self.client.login(username=USERNAME_FOR_TEST,password=PASSWORD_FOR_TEST)

        if prn_info!=False:
            print access

        response = self.client.post('/intake/search-by-ssn',{'last_4_ssn':VALID_LAST_4_SSN,},follow=True)

        if prn_info!=False:
            print response.content
            # check response details

        print "%s = %s" % (response.status_code,'200')

        Test_Msg("Checking for Valid Patient Search By SSN:"+VALID_LAST_4_SSN)

        Look_For_What = VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME
        result = None
        try:
            result = self.assertContains(response,Look_For_What)
            # result = "skipped"
            Test_Msg( "None is good: Outcome =" + str(result)+"\n     Successful Test")
        except result != None:
            print "No match in Page /intake/search-by-SSN"
            print response.content
        Test_End()

        return

    def test_search_by_SSN_with_tester_and_invalid_ssn(self):
        """
        Successful Search with Tester Permission and Valid Search SSN
        Using testutils.test_for_200(self, usrname, passwd, output, post_url,post_parameters, looked_for, called_by )
        """
        Test_Start()

        prn_info = False

        # We should search for this
        p = get_object_or_404(PatientProfile, patient_id=VALID_PATIENT_ID)

        if prn_info!=False:
            print p

        usrname = USERNAME_FOR_TEST
        passwd=PASSWORD_FOR_TEST
        output = []
        post_url = '/intake/search-by-ssn'
        post_parameters = {'last_4_ssn':INVALID_LAST_4_SSN}
        look_for_this = " 0 Matches For "
        calling_test_function = inspect.getframeinfo(inspect.currentframe().f_back)[2]
        print "calling:["+calling_test_function+"]"

        Access_Authorised = test_for_200(self, usrname, passwd, output, post_url,post_parameters, look_for_this, calling_test_function, prn_info )
        if Access_Authorised == None:
            Test_Msg("Successful Test for 200")
        else:
            Test_Msg("Test Failed for 200")

        Test_End()

        return

    def test_search_by_SSN_with_bad_format(self):
        """
        Successful access with Tester Permission.
        Testing Bad Number formats (only 4 digits are valid)
        Test1 = 'abcd'
        Test2 = '9'
        Test3 = '99'
        Test4 = '999'
        Test5 = '99999'
        """

        prn_info = False

        usrname = USERNAME_FOR_TEST
        passwd=PASSWORD_FOR_TEST
        output = []
        post_url = '/intake/search-by-ssn'
        calling_test_function = inspect.getframeinfo(inspect.currentframe().f_back)[2]
        # print "calling:["+calling_test_function+"]"

        Test_Start("Testing for invalid inputs")
        Test_input = ['abcd','9','99','999','99999']
        Test_answer = ['Enter a whole number',
                       'You must supply exactly 4 digits',
                       'You must supply exactly 4 digits',
                       'You must supply exactly 4 digits',
                       'You must supply exactly 4 digits']

        for i in range(0,5):
            Test_Msg(str(i)+":Testing "+ Test_input[i]+" for "+Test_answer[i])
            post_parameters = {'last_4_ssn':Test_input[i]}
            look_for_this = Test_answer[i]

            Access_Authorised = test_for_200(self, usrname, passwd, output, post_url,post_parameters, look_for_this, calling_test_function, prn_info )
            if Access_Authorised == None:
                Test_Msg("Successful Test for ("+Test_input[i]+") "+Test_answer[i])
            else:
                Test_Msg("Test Failed for ("+Test_input[i]+") "+Test_answer[i])


        Test_End("End of invalid input tests")

        return

class View_Locator_TestCase(TestCase):
    """
    Access View Locator using Tester Account
    """
    fixtures = ['apps/intake/fixtures/intake_test_data.json',
                'apps/intake/fixtures/intake_inprocess.json',
                'apps/services/fixtures/services_testdata.json',
                'apps/accounts/fixtures/accounts_test_data.json',
                'apps/grants/fixtures/grants_test_data.json']

    def test_view_locator_with_valid_pat_id(self):
        """
        Access with Valid Tester Permissions and Valid pat_id
        """
        Test_Start()

        prn_info = False

        # We should search for this
        p = get_object_or_404(PatientProfile, patient_id=VALID_PATIENT_ID)

        if prn_info!=False:
            print p

        usrname = USERNAME_FOR_TEST
        passwd = PASSWORD_FOR_TEST
        output = []
        post_url = '/intake/view-locator/'+VALID_PATIENT_ID
        post_parameters = {}
        # post_parameters = {'pat_id':VALID_PATIENT_ID}
        look_for_this = VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME+" ("+VALID_PATIENT_ID+")"
        calling_test_function = inspect.getframeinfo(inspect.currentframe().f_back)[2]
        # print "calling:["+calling_test_function+"]"

        if prn_info!=False:
            print "URL:" + post_url
            print "Searching for:" + look_for_this

        Access_Authorised = test_for_200_with_get(self, usrname, passwd, output, post_url,post_parameters, look_for_this, calling_test_function, prn_info )
        if Access_Authorised == None:
            Test_Msg("Successful Test for Valid Pat_Id:"+VALID_PATIENT_ID)
        else:
            Test_Msg("Test Failed for Valid Pat_Id:"+VALID_PATIENT_ID)

        Test_End()

        return

    def test_view_locator_with_invalid_pat_id(self):
        """
        Access with Valid Tester Permissions and Valid pat_id
        """
        Test_Start()

        prn_info = False

        # We should search for this
        p = get_object_or_404(PatientProfile, patient_id=VALID_PATIENT_ID)
        if prn_info!=False:
            print p

        usrname = USERNAME_FOR_TEST
        passwd=PASSWORD_FOR_TEST
        output = []
        post_url = '/intake/view-locator/'+INVALID_PATIENT_ID
        post_parameters = {'pat_id':INVALID_PATIENT_ID}
        look_for_this = INVALID_PATIENT_FIRSTNAME+" "+INVALID_PATIENT_LASTNAME+" ("+INVALID_PATIENT_ID+")"
        calling_test_function = inspect.getframeinfo(inspect.currentframe().f_back)[2]
        # print "calling:["+calling_test_function+"]"

        Access_Authorised = test_for_404_with_get(self, usrname, passwd, output, post_url,post_parameters, look_for_this, calling_test_function, prn_info )
        if Access_Authorised == None:
            Test_Msg("Successful Test for Invalid Pat_Id:"+INVALID_PATIENT_ID)
        else:
            Test_Msg("Test Failed for Invalid Pat_Id:"+INVALID_PATIENT_ID)

        Test_End()

        return

class Inprocess_List_TestCase(TestCase):
    """
    Test the inprocess List
    Test with Tester and non-tester permission

    inprocess-list has heading "Select an In-process Patient"
    Use record: Ian Nitial (INNL8765)
    """

    fixtures = ['apps/intake/fixtures/intake_test_data.json',
                'apps/services/fixtures/services_testdata.json',
                'apps/accounts/fixtures/accounts_test_data.json',
                'apps/grants/fixtures/grants_test_data.json']


    def test_inprocess_list_with_nontester(self):
        """
        Use Non-Tester permission - we should get a 401 - not authorised
        """
        Test_Start()

        prn_info = False

        # We should search for this
        p = get_object_or_404(PatientProfile, patient_id=VALID_PATIENT_ID)
        ip_patient = p

        print p
        print ip_patient.creation_date
        print date.today()
        print date.today()
        ip_patient.creation_date=date.today()
        print ip_patient.creation_date
        ip_patient.save()
        print ip_patient.creation_date

        calling_test_function = inspect.getframeinfo(inspect.currentframe().f_back)[2]
        print "calling:["+calling_test_function+"]"
        usrname = USERNAME_NOT_TEST
        passwd=PASSWORD_NOT_TEST
        output = []
        post_url = '/today'
        post_parameters = {}

        Access_Authorised = test_for_401(self, usrname, passwd, output, post_url,post_parameters, calling_test_function, prn_info )
        if Access_Authorised == None:
            Test_Msg("Successful Test for 401:"+post_url)
        else:
            Test_Msg("Test Failed for 401:"+post_url)

        Test_End()
        return

    def test_quick_referral_intake_with_nontester(self):
        """
        Use Non-Tester permission - we should get a 401 - not authorised
        """
        Test_Start()

        prn_info = False

        # We should search for this
        p = get_object_or_404(PatientProfile, patient_id=VALID_PATIENT_ID)
        ip_patient = p

        print p
        print ip_patient.creation_date
        print date.today()
        print date.today()
        ip_patient.creation_date=date.today()
        print ip_patient.creation_date
        ip_patient.save()
        print ip_patient.creation_date

        calling_test_function = inspect.getframeinfo(inspect.currentframe().f_back)[2]
        print "calling:["+calling_test_function+"]"
        usrname = USERNAME_NOT_TEST
        passwd=PASSWORD_NOT_TEST
        output = []
        post_url = '/intake/quickreferralintake'
        post_parameters = {}

        Access_Authorised = test_for_401(self, usrname, passwd, output, post_url,post_parameters, calling_test_function, prn_info )
        if Access_Authorised == None:
            Test_Msg("Successful Test for 401:"+post_url)
        else:
            Test_Msg("Test Failed for 401:"+post_url)

        Test_End()
        return

    def test_mark_visit_with_non_tester(self):
        """
        Use Non-Tester permission - we should get a 401 - not authorised
        """
        Test_Start()

        prn_info = False

        # We should search for this
        p = get_object_or_404(PatientProfile, patient_id=VALID_PATIENT_ID)
        ip_patient = p

        print p
        print ip_patient.creation_date
        print date.today()
        print date.today()
        ip_patient.creation_date=date.today()
        print ip_patient.creation_date
        ip_patient.save()
        print ip_patient.creation_date

        calling_test_function = inspect.getframeinfo(inspect.currentframe().f_back)[2]
        print "calling:["+calling_test_function+"]"
        usrname = USERNAME_NOT_TEST
        passwd=PASSWORD_NOT_TEST
        output = []
        post_url = '/intake/markvisit/'+VALID_PATIENT_ID
        post_parameters = {}

        Access_Authorised = test_for_401(self, usrname, passwd, output, post_url,post_parameters, calling_test_function, prn_info )
        if Access_Authorised == None:
            Test_Msg("Successful Test for 401:"+post_url)
        else:
            Test_Msg("Test Failed for 401:"+post_url)

        Test_End()
        return



class Initial_Intake_then_Inprocess_TestCase(TestCase):
    """
    Create an Initial Intake record then select using in-process list
    """

    fixtures = ['apps/intake/fixtures/intake_test_data.json',
                'apps/services/fixtures/services_testdata.json',
                'apps/accounts/fixtures/accounts_test_data.json',
                'apps/grants/fixtures/grants_test_data.json']

    def test_initial_intake_form(self):
        """
        Complete the Initial Intake Form with Tester Permission
        """

        Test_Start()

        prn_info = False

        # We should search for this
        p = get_object_or_404(PatientProfile, patient_id=VALID_PATIENT_ID)

        if prn_info!=False:
            print p


        usrname = USERNAME_FOR_TEST
        passwd=PASSWORD_FOR_TEST
        output = []
        post_url = '/intake/create'
        post_parameters = {'redeem_coupon':'12345',
                           'first_name':VALID_INPROCESS_FIRSTNAME,
                           'last_name':VALID_INPROCESS_LASTNAME,
                           'nick_name':'Initial',
                           'last_4_ssn':VALID_INPROCESS_LAST_4_SSN,
                           'address1':'Behind the dumpster',
                           'address2':'Branch Ave SE',
                           'city':'Washington',
                           'state':'DC',
                           'zip':'20007',
                           'county':'PG County',
                           'ward':'6',
                           'gender':'TRANSGENDER-MALE-TO-FEMALE',
                           'veteran_status': 'False',
                           'race_no_answer':'0',
                           'race_black':'0',
                           'race_white':'0',
                           'race_american_indian':'0',
                           'race_native_hawaiian_or_pac_islander':'0',
                           'race_asian':'0',
                           'race_alaskan_native':'0',
                           'race_other':'0',
                           'ethnicity':'0',
                           'health_insurance_provider':'PUBLIC-ASSIST',
                           'date_of_birth_month':'1',
                           'date_of_birth_day':'20',
                           'date_of_birth_year':'1940',
                           'home_phone_number':'999-999-9999',
                           'mobile_phone_number':'999-999-9999',
                           'patient_signature':PATIENT_SIGNATURE,
                           'reciept_privacy_practices': ""
                           }
        # look_for_this = VALID_INPROCESS_FIRSTNAME+" "+VALID_INPROCESS_LASTNAME+" ("+VALID_INPROCESS_PATIENT_ID+")"
        look_for_this = "There are errors"
        calling_test_function = inspect.getframeinfo(inspect.currentframe().f_back)[2]
        if prn_info!=False:
            print "calling:["+calling_test_function+"]"

        result = test_for_200(self, usrname, passwd, output, post_url,post_parameters, look_for_this, calling_test_function, prn_info )
        if result == None:
            Test_Msg("Successful Test for 200 - Error Trapping:"+VALID_INPROCESS_PATIENT_ID)
        else:
            Test_Msg("Test Failed for 200 - Error Trapping:"+VALID_INPROCESS_PATIENT_ID)

        post_parameters['reciept_privacy_practices'] = True

        print post_parameters
        look_for_this = "Successfully added a new member"

        prn_info= False

        result = test_for_200(self, usrname, passwd, output, post_url,post_parameters, look_for_this, calling_test_function, prn_info )
        if result == None:
            Test_Msg("Successful Test for 200 - Added New Member:"+VALID_INPROCESS_PATIENT_ID)
        else:
            Test_Msg("Test Failed for 200 - Added New Member:"+VALID_INPROCESS_PATIENT_ID)


        Test_Msg("Entering Phase 2 - Inprocess list")

        post_url = '/today/'
        post_parameters = {}
        look_for_this = VALID_INPROCESS_FIRSTNAME+" "+VALID_INPROCESS_LASTNAME+" ("+VALID_INPROCESS_PATIENT_ID+")"

        result = test_for_200(self, usrname, passwd, output, post_url,post_parameters, look_for_this, calling_test_function, prn_info )
        if result == None:
            Test_Msg("Successful - InProcess listed:"+VALID_INPROCESS_PATIENT_ID+ " in "+post_url)
        else:
            Test_Msg("Test Failed - No inprocess List for:"+VALID_INPROCESS_PATIENT_ID+ " in "+post_url)


        Test_End()

        return

    def test_quick_referral_intake_form(self):
        """
        Complete the Initial Quick Referral Intake Form with Tester Permission
        """

        Test_Start()

        prn_info = False

        # We should search for this
        p = get_object_or_404(PatientProfile, patient_id=VALID_PATIENT_ID)

        if prn_info!=False:
            print p


        usrname = USERNAME_FOR_TEST
        passwd=PASSWORD_FOR_TEST
        output = []
        post_url = '/intake/quickreferralintake'
        post_parameters = {
                           'first_name':VALID_INPROCESS_FIRSTNAME,
                           'last_name':VALID_INPROCESS_LASTNAME,
                           }
        # look_for_this = VALID_INPROCESS_FIRSTNAME+" "+VALID_INPROCESS_LASTNAME+" ("+VALID_INPROCESS_PATIENT_ID+")"
        look_for_this = "There are errors"

        calling_test_function = inspect.getframeinfo(inspect.currentframe().f_back)[2]
        if prn_info!=False:
            print "calling:["+calling_test_function+"]"

        result = test_for_200(self, usrname, passwd, output, post_url,post_parameters, look_for_this, calling_test_function, prn_info )
        if result == None:
            Test_Msg("Successful Test for 200 - Error Trapping:"+VALID_INPROCESS_PATIENT_ID)
        else:
            Test_Msg("Test Failed for 200 - Error Trapping:"+VALID_INPROCESS_PATIENT_ID)

        post_parameters['last_4_ssn'] = VALID_INPROCESS_LAST_4_SSN

        print post_parameters
        look_for_this = "Successfully added a new member"

        prn_info= False

        result = test_for_200(self, usrname, passwd, output, post_url,post_parameters, look_for_this, calling_test_function, prn_info )
        if result == None:
            Test_Msg("Successful Test for 200 - Added New Member:"+VALID_INPROCESS_PATIENT_ID)
        else:
            Test_Msg("Test Failed for 200 - Added New Member:"+VALID_INPROCESS_PATIENT_ID)


        Test_End()

        return

    def test_mark_visit_form(self):
        """
        Complete the MarkVisit Form with Tester Permission
        """

        Test_Start()

        prn_info = False

        # We should search for this
        p = get_object_or_404(PatientProfile, patient_id=VALID_PATIENT_ID)

        if prn_info!=False:
            print p


        usrname = USERNAME_FOR_TEST
        passwd=PASSWORD_FOR_TEST
        output = []
        post_url = '/intake/markvisit/'+VALID_PATIENT_ID
        post_parameters = {

                          }
        look_for_this = "Please fix the errors on the form"

        calling_test_function = inspect.getframeinfo(inspect.currentframe().f_back)[2]
        if prn_info!=False:
            print "calling:["+calling_test_function+"]"

        result = test_for_200(self, usrname, passwd, output, post_url,post_parameters, look_for_this, calling_test_function, prn_info )
        if result == None:
            Test_Msg("Successful Test for 200 - Error Trapping:"+VALID_PATIENT_ID)
        else:
            Test_Msg("Test Failed for 200 - Error Trapping:"+VALID_PATIENT_ID)

        post_parameters['creation_date'] = date.today()

        print post_parameters
        look_for_this = "Successfully marked as visiting today"

        prn_info= False

        result = test_for_200(self, usrname, passwd, output, post_url,post_parameters, look_for_this, calling_test_function, prn_info )
        if result == None:
            Test_Msg("Successful Test for 200 - Added New Member:"+VALID_PATIENT_ID)
        else:
            Test_Msg("Test Failed for 200 - Added New Member:"+VALID_PATIENT_ID)


        Test_End()

        return

