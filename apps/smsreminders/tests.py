"""
run "python manage.py test smsreminders>test_results/smsreminders_testresult.txt"

Author: Mark Scrimshire @ekivemark

To test SMS Responses set TESTER_CELL_NUMBER to your cellphone number

Some SMS Transactions have been amended to recognize 999-999-9999 as a special number
and NOT send an SMS Message via Twilio

"""

__author__ = 'mark'
from django.test import TestCase

from datetime import *
from apps.intake.urls import *
from testutils import  Test_Start, Test_End, Test_Msg, test_for_401, test_for_200, test_for_404_with_get
import inspect
from django.conf import settings
from settings_test import *



"""
Tests for the Hive.smsreminders app.

Run from root of hive app.
Run with "python manage.py test {app name}"
Example: python manage.py test smsreminders >./test_results/smsreminders_testresult.txt

Generate the test data
python manage.py dumpdata smsreminders --indent=4 >./apps/smsreminders/fixtures/smsreminders_testdata.json

"""


# Add module specific test variables here

# End of Module specific test variables section


# SimpleTest for a working Test Harness
# @unittest.skip
class smsreminders_SimpleTest(TestCase):
    """Background to this test harness
    and prove the test harness works
    """

    fixtures = ['apps/intake/fixtures/intake_test_data.json',
                'apps/services/fixtures/services_testdata.json',
                'apps/accounts/fixtures/accounts_test_data.json']

    def test_smsreminders_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        Test_Start("1+1=2")
        answer = self.assertEqual(1 + 1, 2)
        Test_Msg("hive.apps.smsreminders.tests.py")
        print "     Test Runtime: "+str(datetime.datetime.now())
        if answer == None:
            print "     Test Harness ready"
        else:
            print "     This Test Harness has a problem"

        Test_End("hive.apps.smsreminders.tests.py")
        return

class smsreminders_non_tester_failed_access_TestCase(TestCase):
    """
    Non-Tester gets 401 not authorised
    Tester gets 200 submits without all required fields - gets error
    Tester gets 200 submits with all required fields - gets success

    Access Tests:
        /sms-reminders/appointment/search-by-name/
        /sms-reminders/appointment/create/
        /sms-reminders/appointment/view/
        /sms-reminders/adherence/create/
        /sms-reminders/adherence/search-by-name/
        /sms-reminders/adherence/view/
        /sms-reminders/cron/insert/
        /sms-reminders/send/
        /sms-reminders/messages/

    """

    fixtures =  ['apps/intake/fixtures/intake_test_data.json',
                 'apps/services/fixtures/services_testdata.json',
                 'apps/accounts/fixtures/accounts_test_data.json',
                 'apps/intake/fixtures/intake_inprocess.json']

    def test_smsreminders_non_testers(self):
        """
        Test with non-tester permission for 401 not authorised
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
        post_url = '/sms-reminders/appointment/search-by-name'
        post_parameters = {}

        Access_Authorised = test_for_401(self, usrname, passwd, output, post_url,post_parameters, calling_test_function, prn_info )
        if Access_Authorised == None:
            Test_Msg("Successful Test for 401:"+post_url)
        else:
            Test_Msg("Test Failed for 401:"+post_url)

        post_url = '/sms-reminders/appointment/create/'+VALID_PATIENT_ID

        Access_Authorised = test_for_401(self, usrname, passwd, output, post_url,post_parameters, calling_test_function, prn_info )
        if Access_Authorised == None:
            Test_Msg("Successful Test for 401:"+post_url)
        else:
            Test_Msg("Test Failed for 401:"+post_url)

        post_url = '/sms-reminders/appointment/view/1'

        Access_Authorised = test_for_401(self, usrname, passwd, output, post_url,post_parameters, calling_test_function, prn_info )
        if Access_Authorised == None:
            Test_Msg("Successful Test for 401:"+post_url)
        else:
            Test_Msg("Test Failed for 401:"+post_url)

        post_url = '/sms-reminders/adherence/create/'+VALID_PATIENT_ID

        Access_Authorised = test_for_401(self, usrname, passwd, output, post_url,post_parameters, calling_test_function, prn_info )
        if Access_Authorised == None:
            Test_Msg("Successful Test for 401:"+post_url)
        else:
            Test_Msg("Test Failed for 401:"+post_url)

        post_url = '/sms-reminders/adherence/search-by-name'

        Access_Authorised = test_for_401(self, usrname, passwd, output, post_url,post_parameters, calling_test_function, prn_info )
        if Access_Authorised == None:
            Test_Msg("Successful Test for 401:"+post_url)
        else:
            Test_Msg("Test Failed for 401:"+post_url)

        post_url = '/sms-reminders/adherence/view/1'

        Access_Authorised = test_for_401(self, usrname, passwd, output, post_url,post_parameters, calling_test_function, prn_info )
        if Access_Authorised == None:
            Test_Msg("Successful Test for 401:"+post_url)
        else:
            Test_Msg("Test Failed for 401:"+post_url)


        post_url = '/sms-reminders/send/'

        Access_Authorised = test_for_401(self, usrname, passwd, output, post_url,post_parameters, calling_test_function, prn_info )
        if Access_Authorised == None:
            Test_Msg("Successful Test for 401:"+post_url)
        else:
            Test_Msg("Test Failed for 401:"+post_url)


        post_url =  '/sms-reminders/messages/'

        Access_Authorised = test_for_401(self, usrname, passwd, output, post_url,post_parameters, calling_test_function, prn_info )
        if Access_Authorised == None:
            Test_Msg("Successful Test for 401:"+post_url)
        else:
            Test_Msg("Test Failed for 401:"+post_url)

        Test_End()

        return

class smsreminders_test_valid_transactions_TestCase(TestCase):
    """
    Tester gets 200 submits without all required fields - gets error
    Tester gets 200 submits with all required fields - gets success

    Access Tests:
        /sms-reminders/appointment/search-by-name/
        /sms-reminders/appointment/create/
        /sms-reminders/appointment/view/
        /sms-reminders/adherence/create/
        /sms-reminders/adherence/search-by-name/
        /sms-reminders/adherence/view/
        /sms-reminders/cron/insert/
        /sms-reminders/send/
        /sms-reminders/messages/

    """
    fixtures =  ['apps/intake/fixtures/intake_test_data.json',
                 'apps/services/fixtures/services_testdata.json',
                 'apps/accounts/fixtures/accounts_test_data.json',
                 'apps/intake/fixtures/intake_inprocess.json']

    def test_smsreminders_send(self):
        """
        Send a text message to a cell number
        enter your cell number in TESTER_CELL_NUMBER = "999-999-9999"
        """

        Test_Start()
        # We should search for this
        prn_info = False

        calling_test_function = inspect.getframeinfo(inspect.currentframe().f_back)[2]
        if prn_info!=False:
            print "calling:["+calling_test_function+"]"

        usrname = USERNAME_FOR_TEST
        passwd=PASSWORD_FOR_TEST
        output = []
        post_url = '/sms-reminders/send/'
        post_parameters = {"to": TESTER_CELL_NUMBER,
                           "message": "Hello world via "+post_url
                           }
        look_for_this = "SMS Sent."
        Access_Authorised = test_for_200(self, usrname, passwd, output, post_url,post_parameters, look_for_this, calling_test_function, prn_info )
        if prn_info!=False:
            print "Access Authorised:"
            print Access_Authorised

        if Access_Authorised == None:
            Test_Msg("Successful Test for send message:["+post_parameters['message']+"] to:"+TESTER_CELL_NUMBER)
        else:
            Test_Msg("Test Failed for target:"+TESTER_CELL_NUMBER)

        Test_End()


        return

    def test_smsreminders_appointment(self):
        """
        Search by name
        Then create adherence message

        ToDo: Get Current Date and Time and populate in to message

        """
        Test_Start()
        # We should search for this
        prn_info = False

        now = date.today()

        now_day = now.strftime("%d")
        now_month = now.strftime("%m")
        now_year  = now.strftime("%Y")

        now_to_then = now + timedelta(days=7)

        timeoday = datetime.datetime.now()
        test_time = timeoday + timedelta(minutes=10)

        now_time = test_time.strftime("%H:%M")
        now_hour = test_time.strftime("%H")
        now_minute = test_time.strftime("%M")

        then_day = now_to_then.strftime("%d")
        then_month = now_to_then.strftime("%m")
        then_year = now_to_then.strftime("%Y")

        print str(now) + "[Year:"+ now_year + " Month:"+ now_month +" Day:"+ now_day +"]"
        print str(timeoday) + "[Test time:"+ str(test_time) + "]"
        print "Valid Time for submit:"+ now_time

        calling_test_function = inspect.getframeinfo(inspect.currentframe().f_back)[2]
        if prn_info!=False:
            print "calling:["+calling_test_function+"]"

        usrname = USERNAME_FOR_TEST
        passwd=PASSWORD_FOR_TEST
        output = []
        post_url = '/sms-reminders/appointment/search-by-name'
        post_parameters = {"first_name": VALID_PATIENT_FIRSTNAME
                           }
        look_for_this = "Create a reminder for "+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME
        Access_Authorised = test_for_200(self, usrname, passwd, output, post_url,post_parameters, look_for_this, calling_test_function, prn_info )
        if prn_info!=False:
            print "Access Authorised:"
            print Access_Authorised

        if Access_Authorised == None:
            Test_Msg("Successfully found: "+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME)
        else:
            Test_Msg("Test Failed for: "+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME)


        post_url = '/sms-reminders/appointment/create/'+VALID_PATIENT_ID
        post_parameters = {"title": "Reminding You",
                           "creation_date_month": now_month,
                           "creation_date_day": now_day,
                           "creation_date_year": now_year,
                           "reminder_datetime": str(now)+" "+now_time,
                           "message": "Don't forget your appointment"+post_url,
                           }

        look_for_this = "Successfully added an appointment reminder"

        Access_Authorised = test_for_200(self, usrname, passwd, output, post_url,post_parameters, look_for_this, calling_test_function, prn_info )
        if prn_info!=False:
            print "Access Authorised:"
            print Access_Authorised

        if Access_Authorised == None:
            Test_Msg("Successfully Added Appointment: "+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME)
        else:
            Test_Msg("Test Failed To Add Appointment: "+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME)

        post_url = '/sms-reminders/appointment/view/1'
        post_parameters = {}
        look_for_this = "Appointment Reminder for"

        Access_Authorised = test_for_200(self, usrname, passwd, output, post_url,post_parameters, look_for_this, calling_test_function, prn_info )
        if prn_info!=False:
            print "Access Authorised:"
            print Access_Authorised

        if Access_Authorised == None:
            Test_Msg("Successfully Viewed Appointment: "+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME)
        else:
            Test_Msg("Test Failed To View Appointment: "+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME)



        Test_End()

        return


    def test_smsreminders_adherence(self):
        """
        Search by name
        Then create appointment message

        ToDo: Get Current Date and Time and populate in to message

        """
        Test_Start()

        now = date.today()

        now_day = now.strftime("%d")
        now_month = now.strftime("%m")
        now_year  = now.strftime("%Y")

        now_to_then = now + timedelta(days=7)

        timeoday = datetime.datetime.now()
        test_time = timeoday + timedelta(minutes=10)

        now_time = test_time.strftime("%H:%M")
        now_hour = test_time.strftime("%H")
        now_minute = test_time.strftime("%M")

        then_day = now_to_then.strftime("%d")
        then_month = now_to_then.strftime("%m")
        then_year = now_to_then.strftime("%Y")

        print str(now) + "[Year:"+ now_year + " Month:"+ now_month +" Day:"+ now_day +"]"
        print str(timeoday) + "[Test time:"+ str(test_time) + "]"
        print "Valid Time for submit:"+ now_time

        # We should search for this
        prn_info = False

        calling_test_function = inspect.getframeinfo(inspect.currentframe().f_back)[2]
        if prn_info!=False:
            print "calling:["+calling_test_function+"]"

        usrname = USERNAME_FOR_TEST
        passwd=PASSWORD_FOR_TEST
        output = []
        post_url = '/sms-reminders/adherence/search-by-name'
        post_parameters = {"first_name": VALID_PATIENT_FIRSTNAME
        }
        look_for_this = "Create a reminder for "+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME
        Access_Authorised = test_for_200(self, usrname, passwd, output, post_url,post_parameters, look_for_this, calling_test_function, prn_info )
        if prn_info!=False:
            print "Access Authorised:"
            print Access_Authorised

        if Access_Authorised == None:
            Test_Msg("Successfully found: "+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME)
        else:
            Test_Msg("Test Failed for: "+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME)


        post_url = '/sms-reminders/adherence/create/'+VALID_PATIENT_ID
        post_parameters = {"title": "Reminding You",
                           "creation_date_month": now_month,
                           "creation_date_day": now_day,
                           "creation_date_year": now_year,
                           "reminder_time": now_time,
                           "start_date_month": now_month,
                           "start_date_day": now_day,
                           "start_date_year": now_year,
                           "end_date_month": then_month,
                           "end_date_day": then_day,
                           "end_date_year": then_year,
                           "message": "Adherence reminders"+post_url,
                           "monday": 1,
                           "tuesday": 1,
                           "wednesday": 1,
                           "thursday": 1,
                           "friday": 1,
                           "saturday": 1,
                           "sunday": 1
        }
        ############ Quick display
        # prn_info = True
        look_for_this = "Successfully added an adherence reminder"

        Access_Authorised = test_for_200(self, usrname, passwd, output, post_url,post_parameters, look_for_this, calling_test_function, prn_info )
        if prn_info!=False:
            print "Access Authorised:"
            print Access_Authorised

        if Access_Authorised == None:
            Test_Msg("Successfully Added Reminder: "+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME)
        else:
            Test_Msg("Test Failed To Add Reminder: "+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME)

        post_url = '/sms-reminders/adherence/view/1'
        post_parameters = {}
        look_for_this = "Adherence Schedule for"

        Access_Authorised = test_for_200(self, usrname, passwd, output, post_url,post_parameters, look_for_this, calling_test_function, prn_info )
        if prn_info!=False:
            print "Access Authorised:"
            print Access_Authorised

        if Access_Authorised == None:
            Test_Msg("Successfully Viewed Reminder: "+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME)
        else:
            Test_Msg("Test Failed To View Reminder: "+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME)



        Test_End()

        return

class smsreminders_cron_interaction_TestCase(TestCase):
    """
    Test for Invalid CRON_KEY should return 401 - not authorized
    /sms-reminders/cron/insert/(?P<cron_key>  - insert Today's reminders
    /sms-reminders/cron/adherence-send/(?P<cron_key>
    /sms-reminders/cron/appointment-send/(?P<cron_key>
    /sms-reminders/cron/adherence-response/(?P<cron_key>

    """
    fixtures =  ['apps/intake/fixtures/intake_test_data.json',
                 'apps/services/fixtures/services_testdata.json',
                 'apps/accounts/fixtures/accounts_test_data.json',
                 'apps/intake/fixtures/intake_inprocess.json']

    def test_sms_reminders_cron_bad_cron_key(self):
        """
        Test transactions for not authorized - bad or missing cron key
        """
        Test_Start()
        # We should search for this
        prn_info = False

        bad_cron_key = '123456789'
        empty_cron_key = ''

        calling_test_function = inspect.getframeinfo(inspect.currentframe().f_back)[2]
        if prn_info!=False:
            print "calling:["+calling_test_function+"]"

        usrname = USERNAME_NOT_TEST
        passwd=PASSWORD_NOT_TEST
        output = []
        post_parameters = {}

        post_url = '/sms-reminders/cron/insert/'+bad_cron_key

        Access_Authorised = test_for_401(self, usrname, passwd, output, post_url,post_parameters, calling_test_function, prn_info )
        if Access_Authorised == None:
            Test_Msg("Successful Test for 401:"+post_url)
        else:
            Test_Msg("Test Failed for 401:"+post_url)

        post_url = '/sms-reminders/cron/insert/'+empty_cron_key

        Access_Authorised = test_for_404_with_get(self, usrname, passwd, output, post_url,post_parameters, calling_test_function, prn_info )
        if Access_Authorised == None:
            Test_Msg("Successful Test for 404:"+post_url)
        else:
            Test_Msg("Test Failed for 404:"+post_url)

        post_url = '/sms-reminders/cron/adherence-send/'+bad_cron_key

        Access_Authorised = test_for_401(self, usrname, passwd, output, post_url,post_parameters, calling_test_function, prn_info )
        if Access_Authorised == None:
            Test_Msg("Successful Test for 401:"+post_url)
        else:
            Test_Msg("Test Failed for 401:"+post_url)

        post_url = '/sms-reminders/cron/adherence-send/'+empty_cron_key

        Access_Authorised = test_for_404_with_get(self, usrname, passwd, output, post_url,post_parameters, calling_test_function, prn_info )
        if Access_Authorised == None:
            Test_Msg("Successful Test for 404:"+post_url)
        else:
            Test_Msg("Test Failed for 404:"+post_url)

        post_url = '/sms-reminders/cron/appointment-send/'+bad_cron_key

        Access_Authorised = test_for_401(self, usrname, passwd, output, post_url,post_parameters, calling_test_function, prn_info )
        if Access_Authorised == None:
            Test_Msg("Successful Test for 401:"+post_url)
        else:
            Test_Msg("Test Failed for 401:"+post_url)

        post_url = '/sms-reminders/cron/appointment-send/'+empty_cron_key

        Access_Authorised = test_for_404_with_get(self, usrname, passwd, output, post_url,post_parameters, calling_test_function, prn_info )
        if Access_Authorised == None:
            Test_Msg("Successful Test for 404:"+post_url)
        else:
            Test_Msg("Test Failed for 404:"+post_url)


        post_url = '/sms-reminders/cron/adherence-response/'+bad_cron_key

        Access_Authorised = test_for_401(self, usrname, passwd, output, post_url,post_parameters, calling_test_function, prn_info )
        if Access_Authorised == None:
            Test_Msg("Successful Test for 401:"+post_url)
        else:
            Test_Msg("Test Failed for 401:"+post_url)

        post_url = '/sms-reminders/cron/adherence-response/'+empty_cron_key

        Access_Authorised = test_for_404_with_get(self, usrname, passwd, output, post_url,post_parameters, calling_test_function, prn_info )
        if Access_Authorised == None:
            Test_Msg("Successful Test for 404:"+post_url)
        else:
            Test_Msg("Test Failed for 404:"+post_url)

        Test_End()

        return

    def test_sms_reminders_cron_valid_messages(self):
        """
        Load messages
        Run Cron Insert with Valid Key
        Run Cron Insert again
        """
        Test_Start()

        now = date.today()

        now_day = now.strftime("%d")
        now_month = now.strftime("%m")
        now_year  = now.strftime("%Y")

        now_to_then = now + timedelta(days=7)

        timeoday = datetime.datetime.now()
        test_time = timeoday + timedelta(minutes=10)

        now_time = test_time.strftime("%H:%M")
        now_hour = test_time.strftime("%H")
        now_minute = test_time.strftime("%M")

        then_day = now_to_then.strftime("%d")
        then_month = now_to_then.strftime("%m")
        then_year = now_to_then.strftime("%Y")

        print str(now) + "[Year:"+ now_year + " Month:"+ now_month +" Day:"+ now_day +"]"
        print str(timeoday) + "[Test time:"+ str(test_time) + "]"
        print "Valid Time for submit:"+ now_time

        prn_info = False

        calling_test_function = inspect.getframeinfo(inspect.currentframe().f_back)[2]
        if prn_info!=False:
            print "calling:["+calling_test_function+"]"

        usrname = USERNAME_FOR_TEST
        passwd=PASSWORD_FOR_TEST
        output = []
        post_url = '/sms-reminders/adherence/search-by-name'
        post_parameters = {"first_name": VALID_PATIENT_FIRSTNAME
                          }
        look_for_this = "Create a reminder for "+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME
        Access_Authorised = test_for_200(self, usrname, passwd, output, post_url,post_parameters, look_for_this, calling_test_function, prn_info )
        if prn_info!=False:
            print "Access Authorised:"
            print Access_Authorised

        if Access_Authorised == None:
            Test_Msg("Successfully found: "+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME)
        else:
            Test_Msg("Test Failed for: "+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME)


        post_url = '/sms-reminders/adherence/create/'+VALID_PATIENT_ID
        post_parameters = {"title": "Reminding You",
                           "creation_date_month": now_month,
                           "creation_date_day": now_day,
                           "creation_date_year": now_year,
                           "reminder_time": now_time,
                           "start_date_month": now_month,
                           "start_date_day": now_day,
                           "start_date_year": now_year,
                           "end_date_month": then_month,
                           "end_date_day": then_day,
                           "end_date_year": then_year,
                           "message": "Adherence reminders"+post_url,
                           "monday": 1,
                           "tuesday": 1,
                           "wednesday": 1,
                           "thursday": 1,
                           "friday": 1,
                           "saturday": 1,
                           "sunday": 1
                          }
        ############ Quick display
        # prn_info = True
        look_for_this = "Successfully added an adherence reminder"

        Access_Authorised = test_for_200(self, usrname, passwd, output, post_url,post_parameters, look_for_this, calling_test_function, prn_info )
        if prn_info!=False:
            print "Access Authorised:"
            print Access_Authorised

        if Access_Authorised == None:
            Test_Msg("Successfully Added Reminder: "+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME)
        else:
            Test_Msg("Test Failed To Add Reminder: "+VALID_PATIENT_FIRSTNAME+" "+VALID_PATIENT_LASTNAME)

        calling_test_function = inspect.getframeinfo(inspect.currentframe().f_back)[2]
        if prn_info!=False:
            print "calling:["+calling_test_function+"]"

        usrname = USERNAME_NOT_TEST
        passwd=PASSWORD_NOT_TEST
        output = []
        post_parameters = {}

        post_url = '/sms-reminders/cron/insert/'+settings.CRON_KEY
        look_for_this = "The following reminders have been scheduled for today"

        prn_info = False
        Access_Authorised = test_for_200(self, usrname, passwd, output, post_url,post_parameters, calling_test_function, prn_info )
        if Access_Authorised == None:
            Test_Msg("Successful Test for 200:"+post_url)
        else:
            Test_Msg("Test Failed for 200:"+post_url)

        return
