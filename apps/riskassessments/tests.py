"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test hivtest".

Replace this with more appropriate tests for your application.
"""
from django.shortcuts import  get_object_or_404
from django.test import TestCase
from apps.intake.models import PatientProfile
from apps.hivtest.models import HIVGroupedConsent
from testutils import  Test_Start, Test_End, Test_Msg, test_for_401, test_for_200, test_for_200_with_get
import inspect
from datetime import  datetime
from settings_test import *
# line above imports standard test framework variables.

"""
Tests for the Hive.hivtest app.

Run from root of hive app.
Run with "python manage.py test hivtest"
Example: python manage.py test hivtest >./test_results/hivtest_testresult.txt

Generate the test data
python manage.py dumpdata hivtest >
./apps/hivtest/fixtures/hivtest_testdata.json

"""

# Add module specific test variables here

# End of Module specific test variables section

class SimpleTest(TestCase):
    """
    Background to this test harness
    and prove the test harness works
    """

    # fixtures = ['apps/intake/fixtures/intake_test_data.json',
    #             'apps/accounts/fixtures/accounts_test_data.json']

    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        Test_Start("1+1=2")
        answer = self.assertEqual(1 + 1, 2)
        Test_Msg("hive.apps.hivtest.tests.py")
        print "     Test Runtime: "+str(datetime.now())
        if answer == None:
            print "     Test Harness ready"
        else:
            print "     This Test Harness has a problem"
        Test_End("hive.apps.hivtest.tests.py")
        return


class ViewGC_TestCase(TestCase):
    """ Test the View Group Consent Display
    """
    fixtures = ['apps/intake/fixtures/intake_test_data.json',
                'apps/accounts/fixtures/accounts_test_data.json']

    def test_vgc_invalid_tester(self):
        """ Use Non-Tester permission - to return a 401 - not authorised
        """
        Test_Start()

        prn_info = False

        # We should search for this
        p = get_object_or_404(PatientProfile, patient_id=VALID_PATIENT_ID)
        print p
        # print HIVGroupedConsent.objects.all()

        calling_test_function = inspect.getframeinfo(inspect.currentframe().f_back)[2]
        # print "calling:["+calling_test_function+"]"
        usrname = USERNAME_NOT_TEST
        passwd=PASSWORD_NOT_TEST
        output = []
        post_url = '/hivtest/view/grouped-consent/'+VALID_PATIENT_ID
        post_parameters = {}

        Access_Authorised = test_for_401(self, usrname, passwd, output, post_url,post_parameters, calling_test_function, prn_info )
        if Access_Authorised == None:
            Test_Msg("Successful Test for 401")
        else:
            Test_Msg("Test Failed for 401")

        Test_End()
        return

    def test_vgc_valid_tester(self):
        """
        Use Tester Permission. We should get the view HIV Grouped Consent returned with the Pat_id
        that was loaded via fixture: intake_test_data.json
        """
        fixtures = []
        Test_Start()

        prn_info = False

        # We should search for this
        p = get_object_or_404(PatientProfile, patient_id=VALID_PATIENT_ID)
        print p

        usrname = USERNAME_FOR_TEST
        passwd=PASSWORD_FOR_TEST
        output = []
        post_url = '/hivtest/grouped-consent/'+VALID_PATIENT_ID
        calling_test_function = inspect.getframeinfo(inspect.currentframe().f_back)[2]
        # print "calling:["+calling_test_function+"]"

        Test_Start("Testing for valid inputs")

        Test_Msg("Testing ")
        post_parameters = {'reason':"REQUESTING-HIV-TEST",
                   'creation_date_month':'1',
                   'creation_date_day':'2',
                   'creation_date_year':'2012',
                   'self_or_read_to':'READ-SELF',
                   'patient_signature':[{"lx":62,"ly":28,"mx":62,"my":27},{"lx":63,"ly":27,"mx":62,"my":28},{"lx":66,"ly":26,"mx":63,"my":27},{"lx":71,"ly":24,"mx":66,"my":26},{"lx":75,"ly":22,"mx":71,"my":24},{"lx":80,"ly":20,"mx":75,"my":22},{"lx":83,"ly":19,"mx":80,"my":20},{"lx":85,"ly":18,"mx":83,"my":19},{"lx":86,"ly":17,"mx":85,"my":18},{"lx":87,"ly":17,"mx":86,"my":17},{"lx":87,"ly":18,"mx":87,"my":17},{"lx":87,"ly":20,"mx":87,"my":18},{"lx":87,"ly":22,"mx":87,"my":20},{"lx":88,"ly":24,"mx":87,"my":22},{"lx":88,"ly":26,"mx":88,"my":24},{"lx":88,"ly":27,"mx":88,"my":26},{"lx":88,"ly":28,"mx":88,"my":27},{"lx":89,"ly":29,"mx":88,"my":28},{"lx":90,"ly":29,"mx":89,"my":29},{"lx":91,"ly":29,"mx":90,"my":29},{"lx":92,"ly":29,"mx":91,"my":29},{"lx":94,"ly":29,"mx":92,"my":29},{"lx":96,"ly":29,"mx":94,"my":29},{"lx":97,"ly":29,"mx":96,"my":29},{"lx":98,"ly":29,"mx":97,"my":29},{"lx":99,"ly":28,"mx":98,"my":29},{"lx":99,"ly":27,"mx":99,"my":28},{"lx":100,"ly":26,"mx":99,"my":27},{"lx":100,"ly":25,"mx":100,"my":26},{"lx":100,"ly":24,"mx":100,"my":25},{"lx":101,"ly":24,"mx":100,"my":24},{"lx":102,"ly":23,"mx":101,"my":24}],
                   'worker_signature':[{"lx":62,"ly":28,"mx":62,"my":27},{"lx":63,"ly":27,"mx":62,"my":28},{"lx":66,"ly":26,"mx":63,"my":27},{"lx":71,"ly":24,"mx":66,"my":26},{"lx":75,"ly":22,"mx":71,"my":24},{"lx":80,"ly":20,"mx":75,"my":22},{"lx":83,"ly":19,"mx":80,"my":20},{"lx":85,"ly":18,"mx":83,"my":19},{"lx":86,"ly":17,"mx":85,"my":18},{"lx":87,"ly":17,"mx":86,"my":17},{"lx":87,"ly":18,"mx":87,"my":17},{"lx":87,"ly":20,"mx":87,"my":18},{"lx":87,"ly":22,"mx":87,"my":20},{"lx":88,"ly":24,"mx":87,"my":22},{"lx":88,"ly":26,"mx":88,"my":24},{"lx":88,"ly":27,"mx":88,"my":26},{"lx":88,"ly":28,"mx":88,"my":27},{"lx":89,"ly":29,"mx":88,"my":28},{"lx":90,"ly":29,"mx":89,"my":29},{"lx":91,"ly":29,"mx":90,"my":29},{"lx":92,"ly":29,"mx":91,"my":29},{"lx":94,"ly":29,"mx":92,"my":29},{"lx":96,"ly":29,"mx":94,"my":29},{"lx":97,"ly":29,"mx":96,"my":29},{"lx":98,"ly":29,"mx":97,"my":29},{"lx":99,"ly":28,"mx":98,"my":29},{"lx":99,"ly":27,"mx":99,"my":28},{"lx":100,"ly":26,"mx":99,"my":27},{"lx":100,"ly":25,"mx":100,"my":26},{"lx":100,"ly":24,"mx":100,"my":25},{"lx":101,"ly":24,"mx":100,"my":24},{"lx":102,"ly":23,"mx":101,"my":24}],
                   }
        # look_for_this = "Visit Count:"
        # look_for_this = VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME+" ("+VALID_PATIENT_ID+")"
        look_for_this = '<a href="/hivtest/grouped-consent/'+VALID_PATIENT_ID+'">HIV Grouped Consent </a>'

        # look_for_this = '<td><a href="/hivtest/grouped-consent/'+VALID_PATIENT_ID+'">HIV Grouped Consent </a></td><td>Complete</td><td><a href="/hivtest/grouped-consent/'+VALID_PATIENT_ID+'">Redo</a>|<a href="/hivtest/view/grouped-consent/'+VALID_PATIENT_ID+'">View</a></td>'

        Access_Authorised = test_for_200(self, usrname, passwd, output, post_url,post_parameters, look_for_this, calling_test_function, prn_info )
        if Access_Authorised == None:
            Test_Msg("Successful Test for ("+VALID_PATIENT_ID+") "+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME)
            Test_Msg("Looked for:"+look_for_this)
        else:
            Test_Msg("Test Failed for ("+VALID_PATIENT_ID+") "+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME)


        print HIVGroupedConsent.objects.all()

        prn_info = True

        usrname = USERNAME_FOR_TEST
        passwd=PASSWORD_FOR_TEST
        output = []
        post_url = '/hivtest/view/grouped-consent/'+VALID_PATIENT_ID
        post_parameters = {}
        look_for_this = GROUPED_CONSENT_VALID_TEXT+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME+" ("+VALID_PATIENT_ID+")"
        calling_test_function = inspect.getframeinfo(inspect.currentframe().f_back)[2]
        # print "calling:["+calling_test_function+"]"

        Access_Authorised = test_for_200_with_get(self, usrname, passwd, output, post_url,post_parameters, look_for_this, calling_test_function, prn_info )
        if Access_Authorised == None:
            Test_Msg("Successful Test for Valid Pat_Id:"+VALID_PATIENT_ID)
        else:
            Test_Msg("Test Failed for Valid Pat_Id:"+VALID_PATIENT_ID)

        Test_End()

        return


class Grouped_Consent_TestCase(TestCase):
    """
    Test for access to Grouped Consent
        Access with Non-Tester Permission = 401
        Access with Tester Permission = 200
            What validation tests do we need to perform?
    """
    fixtures = ['apps/intake/fixtures/intake_test_data.json',
                'apps/accounts/fixtures/accounts_test_data.json']

    def test_grouped_consent_invalid_tester(self):
        """
        Use Non-Tester permission - we should get a 401 - not authorised
        """
        Test_Start()

        prn_info = False

        # We should search for this
        p = get_object_or_404(PatientProfile, patient_id=VALID_PATIENT_ID)
        print p

        calling_test_function = inspect.getframeinfo(inspect.currentframe().f_back)[2]
        # print "calling:["+calling_test_function+"]"
        usrname = USERNAME_NOT_TEST
        passwd=PASSWORD_NOT_TEST
        output = []
        post_url = '/hivtest/grouped-consent/'+VALID_PATIENT_ID
        post_parameters = {}

        Access_Authorised = test_for_401(self, usrname, passwd, output, post_url,post_parameters, calling_test_function, prn_info )
        if Access_Authorised == None:
            Test_Msg("Successful Test for 401")
        else:
            Test_Msg("Test Failed for 401")

        Test_End()
        return

    def test_grouped_consent_valid_tester_valid_pat_id(self):
        '''
        Use Tester Permission. We should get the HIV Grouped Consent returned with the Pat_id
        that was loaded via fixture: intake_test_data.json
        '''
        Test_Start()

        prn_info = False


        # We should search for this
        p = get_object_or_404(PatientProfile, patient_id=VALID_PATIENT_ID)
        print p

        usrname = USERNAME_FOR_TEST
        passwd=PASSWORD_FOR_TEST
        output = []
        post_url = '/hivtest/grouped-consent/'+VALID_PATIENT_ID
        post_parameters = {}
        look_for_this = GROUPED_CONSENT_VALID_TEXT+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME+" ("+VALID_PATIENT_ID+")"
        calling_test_function = inspect.getframeinfo(inspect.currentframe().f_back)[2]
        # print "calling:["+calling_test_function+"]"

        Access_Authorised = test_for_200_with_get(self, usrname, passwd, output, post_url,post_parameters, look_for_this, calling_test_function, prn_info )
        if Access_Authorised == None:
            Test_Msg("Successful Test for Valid Pat_Id:"+VALID_PATIENT_ID)
        else:
            Test_Msg("Test Failed for Valid Pat_Id:"+VALID_PATIENT_ID)

        Test_End()

        return

    def test_grouped_consent_valid_tester_pat_id_and_input(self):
        """
        Use Tester Permission and valid pat_id submit valid input to get to clienthome page

        SELF_READ_CHOICES=(('READ-SELF','I read this myself'),
                   ("READ-WORKER", "I had this read to me."))


        creation_date*          = models.DateField(default=datetime.date.today)
        self_or_read_to*        = models.CharField(max_length=20,
                                                choices=SELF_READ_CHOICES)
        ctra_consent            = models.CharField(max_length=10, blank=True, default=None, choices=YN_CHOICES,
                                               verbose_name= "Patient Consent to Confidentital HIV Antibody Counseling, Testing, and Referral"
                                               )
        rapid_hiv_consent       = models.CharField(max_length=10, blank=True, default=None, choices=YN_CHOICES,
                                               verbose_name="Do you consent to Rapid HIV Testing?")
        rapid_hiv_verbal        = models.BooleanField(default=False, verbose_name="Verbal Agreement?")
        patient_signature*      = models.CharField(max_length=10000, blank=True)
        worker_signature*       = models.CharField(max_length=10000, blank=True)
        """

        prn_info = False

        usrname = USERNAME_FOR_TEST
        passwd=PASSWORD_FOR_TEST
        output = []
        post_url = '/hivtest/grouped-consent/'+VALID_PATIENT_ID
        calling_test_function = inspect.getframeinfo(inspect.currentframe().f_back)[2]
        # print "calling:["+calling_test_function+"]"

        Test_Start("Testing for valid inputs")

        Test_Msg("Testing ")
        post_parameters = {'creation_date_month':'1',
                           'creation_date_day':'2',
                           'creation_date_year':'2012',
                           'self_or_read_to':'READ-SELF',
                           'patient_signature':[{"lx":62,"ly":28,"mx":62,"my":27},{"lx":63,"ly":27,"mx":62,"my":28},{"lx":66,"ly":26,"mx":63,"my":27},{"lx":71,"ly":24,"mx":66,"my":26},{"lx":75,"ly":22,"mx":71,"my":24},{"lx":80,"ly":20,"mx":75,"my":22},{"lx":83,"ly":19,"mx":80,"my":20},{"lx":85,"ly":18,"mx":83,"my":19},{"lx":86,"ly":17,"mx":85,"my":18},{"lx":87,"ly":17,"mx":86,"my":17},{"lx":87,"ly":18,"mx":87,"my":17},{"lx":87,"ly":20,"mx":87,"my":18},{"lx":87,"ly":22,"mx":87,"my":20},{"lx":88,"ly":24,"mx":87,"my":22},{"lx":88,"ly":26,"mx":88,"my":24},{"lx":88,"ly":27,"mx":88,"my":26},{"lx":88,"ly":28,"mx":88,"my":27},{"lx":89,"ly":29,"mx":88,"my":28},{"lx":90,"ly":29,"mx":89,"my":29},{"lx":91,"ly":29,"mx":90,"my":29},{"lx":92,"ly":29,"mx":91,"my":29},{"lx":94,"ly":29,"mx":92,"my":29},{"lx":96,"ly":29,"mx":94,"my":29},{"lx":97,"ly":29,"mx":96,"my":29},{"lx":98,"ly":29,"mx":97,"my":29},{"lx":99,"ly":28,"mx":98,"my":29},{"lx":99,"ly":27,"mx":99,"my":28},{"lx":100,"ly":26,"mx":99,"my":27},{"lx":100,"ly":25,"mx":100,"my":26},{"lx":100,"ly":24,"mx":100,"my":25},{"lx":101,"ly":24,"mx":100,"my":24},{"lx":102,"ly":23,"mx":101,"my":24}],
                           'worker_signature':[{"lx":62,"ly":28,"mx":62,"my":27},{"lx":63,"ly":27,"mx":62,"my":28},{"lx":66,"ly":26,"mx":63,"my":27},{"lx":71,"ly":24,"mx":66,"my":26},{"lx":75,"ly":22,"mx":71,"my":24},{"lx":80,"ly":20,"mx":75,"my":22},{"lx":83,"ly":19,"mx":80,"my":20},{"lx":85,"ly":18,"mx":83,"my":19},{"lx":86,"ly":17,"mx":85,"my":18},{"lx":87,"ly":17,"mx":86,"my":17},{"lx":87,"ly":18,"mx":87,"my":17},{"lx":87,"ly":20,"mx":87,"my":18},{"lx":87,"ly":22,"mx":87,"my":20},{"lx":88,"ly":24,"mx":87,"my":22},{"lx":88,"ly":26,"mx":88,"my":24},{"lx":88,"ly":27,"mx":88,"my":26},{"lx":88,"ly":28,"mx":88,"my":27},{"lx":89,"ly":29,"mx":88,"my":28},{"lx":90,"ly":29,"mx":89,"my":29},{"lx":91,"ly":29,"mx":90,"my":29},{"lx":92,"ly":29,"mx":91,"my":29},{"lx":94,"ly":29,"mx":92,"my":29},{"lx":96,"ly":29,"mx":94,"my":29},{"lx":97,"ly":29,"mx":96,"my":29},{"lx":98,"ly":29,"mx":97,"my":29},{"lx":99,"ly":28,"mx":98,"my":29},{"lx":99,"ly":27,"mx":99,"my":28},{"lx":100,"ly":26,"mx":99,"my":27},{"lx":100,"ly":25,"mx":100,"my":26},{"lx":100,"ly":24,"mx":100,"my":25},{"lx":101,"ly":24,"mx":100,"my":24},{"lx":102,"ly":23,"mx":101,"my":24}],
                           }
        # look_for_this = "Visit Count:"
        # look_for_this = VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME+" ("+VALID_PATIENT_ID+")"
        look_for_this = '<td><a href="/hivtest/grouped-consent/ARFT1234">HIV Grouped Consent </a></td>'

        # look_for_this = '<td><a href="/hivtest/grouped-consent/'+VALID_PATIENT_ID+'">HIV Grouped Consent </a></td><td>Complete</td><td><a href="/hivtest/grouped-consent/'+VALID_PATIENT_ID+'">Redo</a>|<a href="/hivtest/view/grouped-consent/'+VALID_PATIENT_ID+'">View</a></td>'

        Access_Authorised = test_for_200(self, usrname, passwd, output, post_url,post_parameters, look_for_this, calling_test_function, prn_info )
        if Access_Authorised == None:
            Test_Msg("Successful Test for ("+VALID_PATIENT_ID+") "+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME)
            Test_Msg("Looked for:"+look_for_this)
        else:
           Test_Msg("Test Failed for ("+VALID_PATIENT_ID+") "+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME)

        # response=self.client.post('/clienthome/'+VALID_PATIENT_ID,post_parameters,follow=True)
        # print response
        # completed_test = '<td><a href="/hivtest/grouped-consent/'+VALID_PATIENT_ID+'">HIV Grouped Consent </a></td><td>Complete</td><td><a href="/hivtest/grouped-consent/'+VALID_PATIENT_ID+'">Redo</a>|<a href="/hivtest/view/grouped-consent/'+VALID_PATIENT_ID+'">View</a></td>'
        # updated_hivtest = self.assertContains(response, completed_test)
        # print updated_hivtest
        Test_End("End of valid input test")

        return

class HIVTest_TestCase(TestCase):
    """
    Test HIVtest-result and HIVTest-Result-view
    """
    fixtures = ['apps/intake/fixtures/intake_test_data.json',
                'apps/accounts/fixtures/accounts_test_data.json']

    def test_HIVtest_Invalid_tester(self):
        """
        Use Non-Tester permission - we should get a 401 - not authorised
        """
        Test_Start()

        prn_info = False

        # We should search for this
        p = get_object_or_404(PatientProfile, patient_id=VALID_PATIENT_ID)
        print p

        calling_test_function = inspect.getframeinfo(inspect.currentframe().f_back)[2]
        # print "calling:["+calling_test_function+"]"
        usrname = USERNAME_NOT_TEST
        passwd=PASSWORD_NOT_TEST
        output = []
        post_url = '/hivtest/test-result/'+VALID_PATIENT_ID
        post_parameters = {}

        Access_Authorised = test_for_401(self, usrname, passwd, output, post_url,post_parameters, calling_test_function, prn_info )
        if Access_Authorised == None:
            Test_Msg("Successful Test for 401")
        else:
            Test_Msg("Test Failed for 401")

        Test_End()
        return

    def test_HIVtest_ValidTester(self):
        """
        Do HIVTest Input and then test view-HIVTest-Result for content created in Input phase
        """
        Test_Start()

        prn_info = False

        # We should search for this
        p = get_object_or_404(PatientProfile, patient_id=VALID_PATIENT_ID)
        print p
        print PatientProfile.objects.get(patient_id=VALID_PATIENT_ID)

        usrname = USERNAME_FOR_TEST
        passwd=PASSWORD_FOR_TEST
        output = []
        post_url = '/hivtest/test-result/'+VALID_PATIENT_ID
        calling_test_function = inspect.getframeinfo(inspect.currentframe().f_back)[2]
        # print "calling:["+calling_test_function+"]"

        Test_Start("Testing for valid inputs")

        Test_Msg("Testing ")
        post_parameters = {'creation_date_month':'1',
                       'creation_date_day':'2',
                       'creation_date_year':'2012',
                       'cdc_form_id':'123456789',
                       'hiv_test_result':'REACTIVE',
                       'patient_signature':[{"lx":62,"ly":28,"mx":62,"my":27},{"lx":63,"ly":27,"mx":62,"my":28},{"lx":66,"ly":26,"mx":63,"my":27},{"lx":71,"ly":24,"mx":66,"my":26},{"lx":75,"ly":22,"mx":71,"my":24},{"lx":80,"ly":20,"mx":75,"my":22},{"lx":83,"ly":19,"mx":80,"my":20},{"lx":85,"ly":18,"mx":83,"my":19},{"lx":86,"ly":17,"mx":85,"my":18},{"lx":87,"ly":17,"mx":86,"my":17},{"lx":87,"ly":18,"mx":87,"my":17},{"lx":87,"ly":20,"mx":87,"my":18},{"lx":87,"ly":22,"mx":87,"my":20},{"lx":88,"ly":24,"mx":87,"my":22},{"lx":88,"ly":26,"mx":88,"my":24},{"lx":88,"ly":27,"mx":88,"my":26},{"lx":88,"ly":28,"mx":88,"my":27},{"lx":89,"ly":29,"mx":88,"my":28},{"lx":90,"ly":29,"mx":89,"my":29},{"lx":91,"ly":29,"mx":90,"my":29},{"lx":92,"ly":29,"mx":91,"my":29},{"lx":94,"ly":29,"mx":92,"my":29},{"lx":96,"ly":29,"mx":94,"my":29},{"lx":97,"ly":29,"mx":96,"my":29},{"lx":98,"ly":29,"mx":97,"my":29},{"lx":99,"ly":28,"mx":98,"my":29},{"lx":99,"ly":27,"mx":99,"my":28},{"lx":100,"ly":26,"mx":99,"my":27},{"lx":100,"ly":25,"mx":100,"my":26},{"lx":100,"ly":24,"mx":100,"my":25},{"lx":101,"ly":24,"mx":100,"my":24},{"lx":102,"ly":23,"mx":101,"my":24}],
                       'worker_signature':[{"lx":62,"ly":28,"mx":62,"my":27},{"lx":63,"ly":27,"mx":62,"my":28},{"lx":66,"ly":26,"mx":63,"my":27},{"lx":71,"ly":24,"mx":66,"my":26},{"lx":75,"ly":22,"mx":71,"my":24},{"lx":80,"ly":20,"mx":75,"my":22},{"lx":83,"ly":19,"mx":80,"my":20},{"lx":85,"ly":18,"mx":83,"my":19},{"lx":86,"ly":17,"mx":85,"my":18},{"lx":87,"ly":17,"mx":86,"my":17},{"lx":87,"ly":18,"mx":87,"my":17},{"lx":87,"ly":20,"mx":87,"my":18},{"lx":87,"ly":22,"mx":87,"my":20},{"lx":88,"ly":24,"mx":87,"my":22},{"lx":88,"ly":26,"mx":88,"my":24},{"lx":88,"ly":27,"mx":88,"my":26},{"lx":88,"ly":28,"mx":88,"my":27},{"lx":89,"ly":29,"mx":88,"my":28},{"lx":90,"ly":29,"mx":89,"my":29},{"lx":91,"ly":29,"mx":90,"my":29},{"lx":92,"ly":29,"mx":91,"my":29},{"lx":94,"ly":29,"mx":92,"my":29},{"lx":96,"ly":29,"mx":94,"my":29},{"lx":97,"ly":29,"mx":96,"my":29},{"lx":98,"ly":29,"mx":97,"my":29},{"lx":99,"ly":28,"mx":98,"my":29},{"lx":99,"ly":27,"mx":99,"my":28},{"lx":100,"ly":26,"mx":99,"my":27},{"lx":100,"ly":25,"mx":100,"my":26},{"lx":100,"ly":24,"mx":100,"my":25},{"lx":101,"ly":24,"mx":100,"my":24},{"lx":102,"ly":23,"mx":101,"my":24}],
                       }
        # look_for_this = "Visit Count:"
        # look_for_this = VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME+" ("+VALID_PATIENT_ID+")"
        look_for_this = '<td><a href="/hivtest/test-result/'+VALID_PATIENT_ID+'">HIV Test Result</a></td>'

        # look_for_this = '<td><a href="/hivtest/grouped-consent/'+VALID_PATIENT_ID+'">HIV Grouped Consent </a></td><td>Complete</td><td><a href="/hivtest/grouped-consent/'+VALID_PATIENT_ID+'">Redo</a>|<a href="/hivtest/view/grouped-consent/'+VALID_PATIENT_ID+'">View</a></td>'

        Access_Authorised = test_for_200(self, usrname, passwd, output, post_url,post_parameters, look_for_this, calling_test_function, prn_info )
        if Access_Authorised == None:
            Test_Msg("Successful Test for ("+VALID_PATIENT_ID+") "+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME)
            Test_Msg("Looked for:"+look_for_this)
        else:
            Test_Msg("Test Failed for ("+VALID_PATIENT_ID+") "+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME)


        # print HIVTest.objects.all()


        output = []
        post_url = '/hivtest/view/test-result/'+VALID_PATIENT_ID
        post_parameters = {}
        look_for_this = VIEW_HIV_TEST_TEXT+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME+" ("+VALID_PATIENT_ID+")"
        calling_test_function = inspect.getframeinfo(inspect.currentframe().f_back)[2]
        # print "calling:["+calling_test_function+"]"

        Access_Authorised = test_for_200_with_get(self, usrname, passwd, output, post_url,post_parameters, look_for_this, calling_test_function, prn_info )
        if Access_Authorised == None:
            Test_Msg("Successful Test for Valid Pat_Id:"+VALID_PATIENT_ID)
        else:
            Test_Msg("Test Failed for Valid Pat_Id:"+VALID_PATIENT_ID)

        Test_End()

        return

class RiskAssessment_TestCase(TestCase):
    """
    Do Risk Assessment and View
    Test with invalid tester then valid tester
    """
    fixtures = ['apps/intake/fixtures/intake_test_data.json',
                'apps/accounts/fixtures/accounts_test_data.json']

    def test_RiskAssessment_Invalid_tester(self):
        """
        Use Non-Tester permission - we should get a 401 - not authorised
        """
        Test_Start()

        prn_info = False

        # We should search for this
        p = get_object_or_404(PatientProfile, patient_id=VALID_PATIENT_ID)
        print p

        calling_test_function = inspect.getframeinfo(inspect.currentframe().f_back)[2]
        # print "calling:["+calling_test_function+"]"
        usrname = USERNAME_NOT_TEST
        passwd=PASSWORD_NOT_TEST
        output = []
        post_url = '/hivtest/risk-assessment/'+VALID_PATIENT_ID
        post_parameters = {}

        Access_Authorised = test_for_401(self, usrname, passwd, output, post_url,post_parameters, calling_test_function, prn_info )
        if Access_Authorised == None:
            Test_Msg("Successful Test for 401")
        else:
            Test_Msg("Test Failed for 401")

        Test_End()
        return

    def test_RiskAssessment_ValidTester(self):
        """
        Use Tester Permission, submit valid input and then test View page
        """
        Test_Start()

        # We should search for this
        p = get_object_or_404(PatientProfile, patient_id=VALID_PATIENT_ID)
        print p
        print PatientProfile.objects.get(patient_id=VALID_PATIENT_ID)

        prn_info = False

        usrname = USERNAME_FOR_TEST
        passwd=PASSWORD_FOR_TEST
        output = []
        post_url = '/hivtest/risk-assessment/'+VALID_PATIENT_ID
        calling_test_function = inspect.getframeinfo(inspect.currentframe().f_back)[2]
        # print "calling:["+calling_test_function+"]"

        Test_Start("Testing for valid inputs")

        Test_Msg("Testing ")
        post_parameters = {'reason':"REQUESTING-HIV-TEST",
                           'creation_date_month':'1',
                           'creation_date_day':'2',
                           'creation_date_year':'2012',
                           'important_to_get_hiv_test':'1',
                           'should_negative_person_test':'1',
                           'ever_drug_alc_treatment':'1',
                           'important_to_get_hiv_test_after_unp_sex':'1',
                           'ever_mental_health_diagnosis':'1',
                           'mental_health_seeing_therapist':'1',
                           'mental_health_taking_medication':'1',
                           'been_incarcerated':'1',
                           'incarceration_release_date':'2012-01-01',
                           'patient_signature':[{"lx":62,"ly":28,"mx":62,"my":27},{"lx":63,"ly":27,"mx":62,"my":28},{"lx":66,"ly":26,"mx":63,"my":27},{"lx":71,"ly":24,"mx":66,"my":26},{"lx":75,"ly":22,"mx":71,"my":24},{"lx":80,"ly":20,"mx":75,"my":22},{"lx":83,"ly":19,"mx":80,"my":20},{"lx":85,"ly":18,"mx":83,"my":19},{"lx":86,"ly":17,"mx":85,"my":18},{"lx":87,"ly":17,"mx":86,"my":17},{"lx":87,"ly":18,"mx":87,"my":17},{"lx":87,"ly":20,"mx":87,"my":18},{"lx":87,"ly":22,"mx":87,"my":20},{"lx":88,"ly":24,"mx":87,"my":22},{"lx":88,"ly":26,"mx":88,"my":24},{"lx":88,"ly":27,"mx":88,"my":26},{"lx":88,"ly":28,"mx":88,"my":27},{"lx":89,"ly":29,"mx":88,"my":28},{"lx":90,"ly":29,"mx":89,"my":29},{"lx":91,"ly":29,"mx":90,"my":29},{"lx":92,"ly":29,"mx":91,"my":29},{"lx":94,"ly":29,"mx":92,"my":29},{"lx":96,"ly":29,"mx":94,"my":29},{"lx":97,"ly":29,"mx":96,"my":29},{"lx":98,"ly":29,"mx":97,"my":29},{"lx":99,"ly":28,"mx":98,"my":29},{"lx":99,"ly":27,"mx":99,"my":28},{"lx":100,"ly":26,"mx":99,"my":27},{"lx":100,"ly":25,"mx":100,"my":26},{"lx":100,"ly":24,"mx":100,"my":25},{"lx":101,"ly":24,"mx":100,"my":24},{"lx":102,"ly":23,"mx":101,"my":24}],
                           'worker_signature':[{"lx":62,"ly":28,"mx":62,"my":27},{"lx":63,"ly":27,"mx":62,"my":28},{"lx":66,"ly":26,"mx":63,"my":27},{"lx":71,"ly":24,"mx":66,"my":26},{"lx":75,"ly":22,"mx":71,"my":24},{"lx":80,"ly":20,"mx":75,"my":22},{"lx":83,"ly":19,"mx":80,"my":20},{"lx":85,"ly":18,"mx":83,"my":19},{"lx":86,"ly":17,"mx":85,"my":18},{"lx":87,"ly":17,"mx":86,"my":17},{"lx":87,"ly":18,"mx":87,"my":17},{"lx":87,"ly":20,"mx":87,"my":18},{"lx":87,"ly":22,"mx":87,"my":20},{"lx":88,"ly":24,"mx":87,"my":22},{"lx":88,"ly":26,"mx":88,"my":24},{"lx":88,"ly":27,"mx":88,"my":26},{"lx":88,"ly":28,"mx":88,"my":27},{"lx":89,"ly":29,"mx":88,"my":28},{"lx":90,"ly":29,"mx":89,"my":29},{"lx":91,"ly":29,"mx":90,"my":29},{"lx":92,"ly":29,"mx":91,"my":29},{"lx":94,"ly":29,"mx":92,"my":29},{"lx":96,"ly":29,"mx":94,"my":29},{"lx":97,"ly":29,"mx":96,"my":29},{"lx":98,"ly":29,"mx":97,"my":29},{"lx":99,"ly":28,"mx":98,"my":29},{"lx":99,"ly":27,"mx":99,"my":28},{"lx":100,"ly":26,"mx":99,"my":27},{"lx":100,"ly":25,"mx":100,"my":26},{"lx":100,"ly":24,"mx":100,"my":25},{"lx":101,"ly":24,"mx":100,"my":24},{"lx":102,"ly":23,"mx":101,"my":24}],
                           }
        # look_for_this = "Visit Count:"
        # look_for_this = VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME+" ("+VALID_PATIENT_ID+")"
        look_for_this = '<td><a href="/hivtest/risk-assessment/'+VALID_PATIENT_ID+'">Risk Assessment</a></td>'


        Access_Authorised = test_for_200(self, usrname, passwd, output, post_url,post_parameters, look_for_this, calling_test_function, prn_info )
        if Access_Authorised == None:
            Test_Msg("Successful Test for ("+VALID_PATIENT_ID+") "+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME)
            Test_Msg("Looked for:"+look_for_this)
        else:
            Test_Msg("Test Failed for ("+VALID_PATIENT_ID+") "+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME)


        # print HIVTest.objects.all()


        output = []
        post_url = '/hivtest/view/risk-assessment/'+VALID_PATIENT_ID
        post_parameters = {}
        look_for_this = VIEW_RISK_ASSESSMENT_TEXT+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME+" ("+VALID_PATIENT_ID+")"
        calling_test_function = inspect.getframeinfo(inspect.currentframe().f_back)[2]
        # print "calling:["+calling_test_function+"]"

        Access_Authorised = test_for_200_with_get(self, usrname, passwd, output, post_url,post_parameters, look_for_this, calling_test_function, prn_info )
        if Access_Authorised == None:
            Test_Msg("Successful Test for Valid Pat_Id:"+VALID_PATIENT_ID)
        else:
            Test_Msg("Test Failed for Valid Pat_Id:"+VALID_PATIENT_ID)

        Test_End()

        return

class Incentive_TestCase(TestCase):
    """
    Do Incentive Receipt and View
    Test with invalid tester then valid tester
    """
    fixtures = ['apps/intake/fixtures/intake_test_data.json',
                'apps/accounts/fixtures/accounts_test_data.json']

    def test_IncentiveReceipt_Invalid_tester(self):
        """
        Use Non-Tester permission - we should get a 401 - not authorised
        """
        Test_Start()

        prn_info = False

        # We should search for this
        p = get_object_or_404(PatientProfile, patient_id=VALID_PATIENT_ID)
        print p

        calling_test_function = inspect.getframeinfo(inspect.currentframe().f_back)[2]
        # print "calling:["+calling_test_function+"]"
        usrname = USERNAME_NOT_TEST
        passwd=PASSWORD_NOT_TEST
        output = []
        post_url = '/hivtest/incentive-receipt/'+VALID_PATIENT_ID
        post_parameters = {}

        Access_Authorised = test_for_401(self, usrname, passwd, output, post_url,post_parameters, calling_test_function, prn_info )
        if Access_Authorised == None:
            Test_Msg("Successful Test for 401")
        else:
            Test_Msg("Test Failed for 401")

        Test_End()
        return

    def test_IncentiveReceipt_ValidTester(self):
        """
        Use Tester Permission, submit valid input and then test View page
        """
        Test_Start()

        prn_info = False

        # We should search for this
        p = get_object_or_404(PatientProfile, patient_id=VALID_PATIENT_ID)
        print p

        print PatientProfile.objects.get(patient_id=VALID_PATIENT_ID)

        usrname = USERNAME_FOR_TEST
        passwd=PASSWORD_FOR_TEST
        output = []
        post_url = '/hivtest/incentive-receipt/'+VALID_PATIENT_ID
        calling_test_function = inspect.getframeinfo(inspect.currentframe().f_back)[2]
        # print "calling:["+calling_test_function+"]"

        Test_Start("Testing for valid inputs")

        Test_Msg("Testing ")
        post_parameters = {'reason':"REQUESTING-HIV-TEST",
                           'creation_date_month':'1',
                           'creation_date_day':'2',
                           'creation_date_year':'2012',
                           'incentive_amount':'10',
                           'card_number':'1234567890',
                           'patient_signature':[{"lx":62,"ly":28,"mx":62,"my":27},{"lx":63,"ly":27,"mx":62,"my":28},{"lx":66,"ly":26,"mx":63,"my":27},{"lx":71,"ly":24,"mx":66,"my":26},{"lx":75,"ly":22,"mx":71,"my":24},{"lx":80,"ly":20,"mx":75,"my":22},{"lx":83,"ly":19,"mx":80,"my":20},{"lx":85,"ly":18,"mx":83,"my":19},{"lx":86,"ly":17,"mx":85,"my":18},{"lx":87,"ly":17,"mx":86,"my":17},{"lx":87,"ly":18,"mx":87,"my":17},{"lx":87,"ly":20,"mx":87,"my":18},{"lx":87,"ly":22,"mx":87,"my":20},{"lx":88,"ly":24,"mx":87,"my":22},{"lx":88,"ly":26,"mx":88,"my":24},{"lx":88,"ly":27,"mx":88,"my":26},{"lx":88,"ly":28,"mx":88,"my":27},{"lx":89,"ly":29,"mx":88,"my":28},{"lx":90,"ly":29,"mx":89,"my":29},{"lx":91,"ly":29,"mx":90,"my":29},{"lx":92,"ly":29,"mx":91,"my":29},{"lx":94,"ly":29,"mx":92,"my":29},{"lx":96,"ly":29,"mx":94,"my":29},{"lx":97,"ly":29,"mx":96,"my":29},{"lx":98,"ly":29,"mx":97,"my":29},{"lx":99,"ly":28,"mx":98,"my":29},{"lx":99,"ly":27,"mx":99,"my":28},{"lx":100,"ly":26,"mx":99,"my":27},{"lx":100,"ly":25,"mx":100,"my":26},{"lx":100,"ly":24,"mx":100,"my":25},{"lx":101,"ly":24,"mx":100,"my":24},{"lx":102,"ly":23,"mx":101,"my":24}],
                           'worker_signature':[{"lx":62,"ly":28,"mx":62,"my":27},{"lx":63,"ly":27,"mx":62,"my":28},{"lx":66,"ly":26,"mx":63,"my":27},{"lx":71,"ly":24,"mx":66,"my":26},{"lx":75,"ly":22,"mx":71,"my":24},{"lx":80,"ly":20,"mx":75,"my":22},{"lx":83,"ly":19,"mx":80,"my":20},{"lx":85,"ly":18,"mx":83,"my":19},{"lx":86,"ly":17,"mx":85,"my":18},{"lx":87,"ly":17,"mx":86,"my":17},{"lx":87,"ly":18,"mx":87,"my":17},{"lx":87,"ly":20,"mx":87,"my":18},{"lx":87,"ly":22,"mx":87,"my":20},{"lx":88,"ly":24,"mx":87,"my":22},{"lx":88,"ly":26,"mx":88,"my":24},{"lx":88,"ly":27,"mx":88,"my":26},{"lx":88,"ly":28,"mx":88,"my":27},{"lx":89,"ly":29,"mx":88,"my":28},{"lx":90,"ly":29,"mx":89,"my":29},{"lx":91,"ly":29,"mx":90,"my":29},{"lx":92,"ly":29,"mx":91,"my":29},{"lx":94,"ly":29,"mx":92,"my":29},{"lx":96,"ly":29,"mx":94,"my":29},{"lx":97,"ly":29,"mx":96,"my":29},{"lx":98,"ly":29,"mx":97,"my":29},{"lx":99,"ly":28,"mx":98,"my":29},{"lx":99,"ly":27,"mx":99,"my":28},{"lx":100,"ly":26,"mx":99,"my":27},{"lx":100,"ly":25,"mx":100,"my":26},{"lx":100,"ly":24,"mx":100,"my":25},{"lx":101,"ly":24,"mx":100,"my":24},{"lx":102,"ly":23,"mx":101,"my":24}],
                           }
        # look_for_this = "Visit Count:"
        # look_for_this = VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME+" ("+VALID_PATIENT_ID+")"
        look_for_this = '<td><a href="/hivtest/incentive-receipt/'+VALID_PATIENT_ID+'">Incentive Receipt</a></td>'


        Access_Authorised = test_for_200(self, usrname, passwd, output, post_url,post_parameters, look_for_this, calling_test_function, prn_info )
        if Access_Authorised == None:
            Test_Msg("Successful Test for ("+VALID_PATIENT_ID+") "+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME)
            Test_Msg("Looked for:"+look_for_this)
        else:
            Test_Msg("Test Failed for ("+VALID_PATIENT_ID+") "+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME)


        # print HIVTest.objects.all()


        output = []
        post_url = '/hivtest/view/incentive-receipt/'+VALID_PATIENT_ID
        post_parameters = {}
        look_for_this = VIEW_INCENTIVE_TEXT+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME+" ("+VALID_PATIENT_ID+")"
        calling_test_function = inspect.getframeinfo(inspect.currentframe().f_back)[2]
        # print "calling:["+calling_test_function+"]"

        Access_Authorised = test_for_200_with_get(self, usrname, passwd, output, post_url,post_parameters, look_for_this, calling_test_function, prn_info )
        if Access_Authorised == None:
            Test_Msg("Successful Test for Valid Pat_Id:"+VALID_PATIENT_ID)
        else:
            Test_Msg("Test Failed for Valid Pat_Id:"+VALID_PATIENT_ID)

        Test_End()

        return