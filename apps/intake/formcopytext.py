#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.conf import settings

#Risk Assessment ----------------------------------------------------------------
risk_assessment_form_top=""
risk_assessment_form_bottom=""
risk_assessment_view_top=risk_assessment_form_top
risk_assessment_view_bottom=risk_assessment_form_bottom


# Grouped Consent Copy ---------------------------------------------------------
grouped_consent_form_top="""
I hereby authorize the %s authority to perform the rapid
HIV test.

I have read the Subject Information Brochure, or it was explained to me, and I
fully understand its contents.

I hereby give my consent for %s to test me for the
presence of antibodies to the human immunodeficiency virus (HIV), the virus
known to cause acquired immune deficiency syndrome (AIDS). I consent to 
counseling concerning the test itself and the test results. In giving my consent,
I understand the following:

As part of the %s's program to combat AIDS, voluntary HIV antibody counseling
and testing services are being provided by %s on a confidential basis.  This
form gives my consent to confidential testing.

The HIV antibody test IS NOT a test for AIDS.  The test DOES NOT tell if a
person has or will ever develop AIDS or any AIDS related condition.  The test
does detect the presence of antibodies to the human immunodeficiency virus (HIV),
the virus known to cause AIDS.

Absence of a court order, information concerning this test will not be released
to anyone else, including an insurance company, without my written consent.

My signature indicates special consent to have my results released to my local
health department for the sole purpose of notifying me of the result.

""" % (settings.ORGANIZATION_NAME,
       settings.ORGANIZATION_NAME,
       settings.LOCATION_NAME,
       settings.ORGANIZATION_NAME,)


grouped_consent_form_bottom="""
I have received HIV prevention and risk reduction as counseling which has
included information:

- About the test; what the test means; and

- What the result will tell me about my health; and

- My risk of HIV infection and AIDS; and

- How I can prevent others and myself from becoming infected with HIV.

I understand that I am consenting to receive the following services from %s:

1. HIV ANTIBODY TEST RESULTS: The results of my test will be given to me in
person during the counseling session. Under no circumstances will my test result
be given out over the phone or through the mail.

2. POST TEST COUNSELING: It is my responsibility to return for my test results
in person.  I will receive post-test counseling after my test results are known.
I will be counseled on the following:

- An explanation of my test results and HIV prevention measures;

- The importance of informing my partner(s) about my antibody status if my
result is reactive;

- The importance of informing other health care providers of my antibody status
to assist them in the evaluation of my health; and

- The importance of maintaining confidentiality of my HIV results to avoid
possible discrimination

3. REFERRAL TO CONFIRMATORY TESTING OF MY TEST RESULT IS POSITIVE: In the event
of a reactive result, a referral to a confirmatory testing will be given
immediately to have a confirmatory test conducted to validate this result.

I have read, or have had it read to me, the above description of the HIV
antibody test and I understand the limitations and possible consequences of this
test.  I have been given the opportunity to ask questions about HIV testing and
have had my questions answered.

By signing my name below, I agree to test for HIV antibodies and the counseling
procedures below.
""" % (settings.ORGANIZATION_NAME)

grouped_consent_view_top=grouped_consent_form_top
grouped_consent_view_bottom=grouped_consent_form_bottom


#Referral Copy -----------------------------------------------------------------
referral_form_top=""
referral_form_bottom="""
*AUTHORIZATION TO RELEASE CLIENT INFORMATION*
    In signing this locator form, I authorize the appropriate officials to
    release and/or obtain personal information as requested to acquire assistance
    and to verify it accuracy. I understand that my records may contain information
    regarding my mental health, substance use or dependency, or sexuality, and
    also may contain confidential HIV/AIDS-related information.  I further understand
    that by signing in the above, I am authorizing the release or exchange of
    these records to the parties named below.  I understand the authorization is voluntary.
"""
referral_view_top=referral_form_top
referral_view_bottom=referral_form_bottom

# Demographics Copy ------------------------------------------------------------
demographics_form_top=""
demographics_form_bottom=""
demographics_view_top=demographics_form_top
demographics_view_bottom=demographics_form_bottom


#Test Result Copy---------------------------------------------------------------

test_result_form_top=""" """
test_result_form_bottom="""
MEANING OF TEST RESULT:

A non-reactive (negative) test result means that no antibodies to HIV-1 and HIV-2
were detected. HIV antibodies may be absent during the "window period" of
infection: the 6-week period prior to the test date.  Follow-up testing may be
necessary if indicated by risk factors.

A reactive (positive) test result suggests that antibodies to HIV-1 and/or HIV-2
are present in the blood.  A specimen will be sent for testing to confirm the
preliminary result.

An invalid test result means the test test was not valid.  An invalid test can
result from a problem running the rest or an interfering substance in the
specimen.  This result is rare and another test will be provided immediately.
"""
test_result_view_top=test_result_form_top
test_result_view_bottom=test_result_form_bottom


# Incentive Copy ---------------------------------------------------------------
incentive_receipt_form_top="""
    I confirm that I received a Safeway gift card, in the amount listed below, from
    Community Education Group for taking an Oral Quick Advance HIV Rapid Test
    on the date shown.
    """
incentive_receipt_form_bottom=""" """
incentive_receipt_view_top=incentive_receipt_form_top
incentive_receipt_view_bottom=incentive_receipt_form_bottom



# Locator Copy -----------------------------------------------------------------

locator_form_top=""" """
locator_form_bottom="""
*AUTHORIZATION TO RELEASE CLIENT INFORMATION*
    In signing this locator form, I authorize the appropriate officials to
    release and/or obtain personal information as requested to acquire assistance
    and to verify its accuracy. I understand that my records may contain information
    regarding my mental health, substance user or dependency, or sexuality, and
    also may contain confidential HIV/AIDS-related information.  I further understand
    that by signing in the above box, I am authorizing the release or exchange of
    these records to the parties named below.  I understand the authorization is voluntary.
"""
locator_view_top=locator_form_top
locator_view_bottom=locator_form_bottom