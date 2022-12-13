from sslcommerz_lib import SSLCOMMERZ
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from students.models import AdmissionStudent
from payments.models import SSLPayment
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView
from django.views.generic.edit import UpdateView
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
# Check if settings.DISALLOW_PAYMENT is False.
# otherwise, these variables can't be imported and will raise exception.
ssl_settings = {
    'store_id': settings.STORE_ID,
    'store_pass': settings.STORE_PASS,
    'issandbox': settings.SSL_ISSANDBOX
}


def store_admission_pay_record(post_body):
    try:
        SSLPayment.objects.create(
            transaction_id=post_body['tran_id'],
            payer=post_body['cus_name'],
            received_amount=post_body['total_amount'],
            pay_reason=post_body['pay_reason'],
            payer_mobile=post_body['cus_phone'],
            payer_email=post_body['cus_email'],
            payer_city=post_body['cus_city'],
            payer_country=post_body['cus_country']
        )
        return True
    except:
        return False

@csrf_exempt
def online_admission_sslpayment(request, pk):
    registrant = AdmissionStudent.objects.get(pk=pk)

    sslcommerz = SSLCOMMERZ(ssl_settings)

    post_body = {}
    post_body['total_amount'] = 0
    post_body['currency'] = ""
    post_body['tran_id'] = registrant.id
    post_body['success_url'] = "https://tareqmonwer.com"
    post_body['fail_url'] = "www.erpbud.com/blog/"
    post_body['cancel_url'] = "www.erpbud.com"
    post_body['emi_option'] = 0
    post_body['cus_name'] = registrant.name
    post_body['cus_email'] = registrant.email
    post_body['cus_phone'] = registrant.mobile_number
    post_body['cus_add1'] = registrant.current_address
    post_body['cus_city'] = registrant.city
    post_body['cus_country'] = "Zimbabwe"
    post_body['product_profile'] = "general"
    post_body['product_name'] = 'Online Admission'
    post_body['product_category'] = 'Educational Service'
    post_body['shipping_method'] = 'NO'
    post_body['num_of_item'] = 1
    post_body['cus_postcode'] = '0000'

    import pprint


    if request.method == 'POST':
        amount =request.POST['amount']
        reason=request.POST['reason']
        datepaid = request.POST['paydate']
        methodpayment = request.POST['method']
        post_body['total_amount'] = int(amount)
        post_body['currency'] = "USD"
        post_body['pay_reason'] = reason
        store_record = store_admission_pay_record(post_body)
        print(store_record)
        if store_record:
            return HttpResponseRedirect( post_body['success_url'])
        else:
            return HttpResponse(
                "Failed to Store Payment Info, Contact Admins ASAP."
            )
    return render(request, 'pages/payment.html')
