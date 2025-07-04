from django.conf import settings
from django.shortcuts import render
from django.urls import reverse
#from paypal.standard.forms import PayPalPaymentsForm
from django.http import JsonResponse

def payment_process(request):
    host = request.get_host()
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '100',
        'item_name': 'Item_Name_xyz',
        'invoice': 'Test Payment Invoice',
        'currency_code': 'USD',
        'notify_url': f'http://{host}{reverse("paypal-ipn")}',
        'return_url': f'http://{host}{reverse("payment_done")}',
        'cancel_return': f'http://{host}{reverse("payment_canceled")}',
    }
    #form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'pets/payment_process.html', {})
    
def example_api(request):
    return JsonResponse({'message': 'Example API works'})


