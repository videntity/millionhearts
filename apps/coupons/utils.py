from ..intake.models import Coupon
from django.db import IntegrityError
def save_new_coupon_range(member_issued, worker, starting_coupon,
                          number_of_coupons):
    coupon_range = [ ]
    end_coupon= starting_coupon + number_of_coupons
    for i in range(starting_coupon, end_coupon):
        coupon_code=str(i)
        #print coupon_code
        coupon_range.append(coupon_code)
        try:
            c=Coupon.objects.create(worker=worker,
                        member_issued=member_issued,
                        coupon_code=coupon_code)
            c.save()
        except(IntegrityError):
            msg="Coupon # %s had already been issued!" % (coupon_code)
            coupon_range.pop()
            coupon_range.append(msg)
            return coupon_range
            
    return coupon_range