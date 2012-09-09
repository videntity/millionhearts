from django import forms

class CouponRangeForm(forms.Form):
        starting_coupon=forms.IntegerField()
        number_of_coupons = forms.IntegerField()