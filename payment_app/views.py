from django.shortcuts import render

# Create your views here.
import random
from django.shortcuts import render, redirect
from django.contrib import messages
from user_app.models import Userinfo, Payment
import razorpay
from django.contrib.auth.decorators import login_required
import requests
from django.utils import timezone

import json
import hashlib
import hmac
from django.conf import settings

PHONEPE_BASE_URL = "https://api-preprod.phonepe.com/apis/pg-sandbox/pg/v1"
CLIENT_ID = "TEST-M220SEDYJDCQ6_25042"
CLIENT_SECRET = "MWUyYzQ0MWYtNWFmMi00ZmEwLThhMTctMzFjNzhkODk4NmU3"
CLIENT_VERSION = 1

# Initialize Razorpay client
razorpay_client = razorpay.Client(auth=("RAZORPAY_KEY_ID", "RAZORPAY_KEY_SECRET"))


def payment(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_app:login')
    try:
        user = Userinfo.objects.get(id=user_id)
    except Userinfo.DoesNotExist:
        return redirect('user_app:login')
    if request.method == 'POST':
        plan = request.POST.get('plan')
        method = request.POST.get('payment_method')
        request.session['plan'] = plan  # Save plan in session
        if method == 'upi':
            return redirect('payment_app:upi_payment')
        elif method in ['debit', 'credit']:
            return redirect('payment_app:card_payment')
        else:
            return redirect('payment')
    return render(request, 'payment.html', {'first_name': user.first_name})



def upi_payment(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_app:login')
    
    if request.method == 'POST':
        upi_id = request.POST.get('upi_id')
        # amount = float(request.POST.get('amount'))  # Amount in INR
        amount = 100.00
        
        CLIENT_ID = 'TEST-M220SEDYJDCQ6_25042'
        client_secret = 'MWUyYzQ0MWYtNWFmMi00ZmEwLThhMTctMzFjNzhkODk4NmU3'
        print('AAAAA')
        api_url = 'https://sandbox.phonepe.com/v1/payment/upi' 
        print('BBBB')

        payment_data = {
                    "merchantId": CLIENT_ID,
                    "merchantTransactionId": merchant_transaction_id,
                    "amount": int(amount * 100),  # Convert to paise
                    "merchantUserId": str(user_id),
                    "callbackUrl": "http://localhost:8000/payment/callback/",
                    "paymentInstrument": {
                        "type": "UPI_INTENT",
                        "target": upi_id,
                    }
                }
        print('CCCC')

        response_data = create_payment(payment_data)

        if response_data.get('success') == True:
            # Check payment status after initiation
            status_data = check_payment_status(merchant_transaction_id)

            if status_data.get('data', {}).get('state') == 'COMPLETED':
                Payment.objects.create(
                    user_id=user_id,
                    amount=amount,
                    status='success',
                    method='UPI',
                    transaction_id=merchant_transaction_id,
                    order_id=status_data['data'].get('merchantOrderId'),
                    payment_date=timezone.now()
                )
                messages.success(request, 'Payment successful!')
                return render(request, 'success.html', {
                    'method': 'UPI',
                    'upi_id': upi_id,
                    'payment_status': 'Success',
                    'message': 'Your payment was successful!'
                })
            else:
                messages.error(request, 'Payment pending or failed!')
                return render(request, 'success.html', {
                    'method': 'UPI',
                    'upi_id': upi_id,
                    'payment_status': 'Failure',
                    'message': 'Payment failed or still processing. Please try again.'
                })
        else:
            messages.error(request, 'Payment initiation failed!')
            return render(request, 'success.html', {
                'method': 'UPI',
                'upi_id': upi_id,
                'payment_status': 'Failure',
                'message': 'Unable to initiate payment.'
            })

    # Handle GET request (render the UPI payment form)
    return render(request, 'upi_payment.html')



# Utility: generate Authorization Signature
def generate_signature(payload: str, client_secret: str) -> str:
    key_bytes = client_secret.encode('utf-8')
    data_bytes = payload.encode('utf-8')
    signature = hmac.new(key_bytes, data_bytes, hashlib.sha256).hexdigest()
    return signature

# 1. Create Payment
def create_payment(payment_data):
    url = f"{PHONEPE_BASE_URL}/pay"
    payload = json.dumps(payment_data)
    signature = generate_signature(payload, CLIENT_SECRET)

    headers = {
        "Content-Type": "application/json",
        "X-CLIENT-ID": CLIENT_ID,
        "X-CLIENT-VERSION": CLIENT_VERSION,
        "X-CLIENT-SIGNATURE": signature,
    }

    response = requests.post(url, headers=headers, data=payload)
    return response.json()

# 2. Check Status
def check_payment_status(merchant_transaction_id):
    url = f"{PHONEPE_BASE_URL}/status/{merchant_transaction_id}"
    headers = {
        "X-CLIENT-ID": CLIENT_ID,
        "X-CLIENT-VERSION": CLIENT_VERSION,
    }
    response = requests.get(url, headers=headers)
    return response.json()

# Main View
def upi_payment_view(request):
    if request.method == 'POST':
        user_id = request.user.id
        amount = request.POST.get('amount')
        upi_id = request.POST.get('upi_id')

        payment_data = {
            "merchantId": CLIENT_ID,
            "merchantTransactionId": f"txn_{timezone.now().timestamp()}",
            "amount": int(float(amount) * 100),
            "merchantUserId": str(user_id),
            "callbackUrl": "http://localhost:8000/payment/callback/",
            "paymentInstrument":{
                "type": "UPI_INTENT",
                "target": upi_id,
            }
        }

        try:
            print('Initiating payment...')
            response_data = create_payment(payment_data)
            print(response_data)

            if response_data.get('success') == True:
                merchant_transaction_id = payment_data['merchantTransactionId']
                status_data = check_payment_status(merchant_transaction_id)
                print(status_data)

                if status_data.get('data', {}).get('state') == 'COMPLETED':
                    Payment.objects.create(
                        user_id=user_id,
                        amount=amount,
                        status='success',
                        method='UPI',
                        transaction_id=merchant_transaction_id,
                        order_id=status_data['data'].get('merchantOrderId'),
                        payment_date=timezone.now()
                    )
                    messages.success(request, 'Payment successful!')
                    return render(request, 'success.html', {
                        'method': 'UPI',
                        'upi_id': upi_id,
                        'payment_status': 'Success',
                        'message': 'Your payment was successful!'
                    })
                else:
                    messages.error(request, 'Payment pending or failed!')
                    return render(request, 'success.html', {
                        'method': 'UPI',
                        'upi_id': upi_id,
                        'payment_status': 'Failure',
                        'message': 'Payment failed or still processing. Please try again.'
                    })

            else:
                messages.error(request, 'Payment initiation failed!')
                return render(request, 'success.html', {
                    'method': 'UPI',
                    'upi_id': upi_id,
                    'payment_status': 'Failure',
                    'message': 'Unable to initiate payment.'
                })

        except requests.exceptions.RequestException as e:
            print('Request Exception:', e)
            messages.error(request, f'Error while processing payment: {e}')
            return redirect('payment_app:error_page')

    else:
        return render(request, 'payment_form.html')


def card_payment(request):
    user = request.user

    if request.method == 'POST':
        # Get payment details from the form
        amount_rupees = request.POST.get('amount')
        card_number = request.POST.get('card_number')
        expiry_date = request.POST.get('expiry_date')
        cvv = request.POST.get('cvv')

        if not amount_rupees or not amount_rupees.replace('.', '', 1).isdigit():
            return render(request, 'card_payment.html', {'error': 'Enter a valid amount'})
        
        amount_paise = int(float(amount_rupees) * 100)
        currency = "INR"

        try:
            # Create Razorpay order
            payment_order = razorpay_client.order.create({
                "amount": amount_paise,
                "currency": currency,
                "payment_capture": 1
            })
            print('ADDDDDD')
        except Exception as e:
            return render(request, 'card_payment.html', {'error': f'Payment creation failed: {str(e)}'})

        payment_order_id = payment_order['id']

        # Store the payment in the Payment model
        payment = Payment(
            user=user,
            amount=amount_rupees,
            status=Payment.PENDING,
            method=Payment.CARD,
            transaction_id=None,  # Update later after payment confirmation
            order_id=payment_order_id
        )
        payment.save()

        context = {
            'razorpay_key_id': "RAZORPAY_KEY_ID",  # Replace with your Razorpay Key ID
            'amount': amount_paise,
            'display_amount': amount_rupees,
            'currency': currency,
            'order_id': payment_order_id,
        }

        return render(request, 'razorpay_checkout.html', context)

    return render(request, 'card_payment.html')


def payment_success(request):
    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')
    signature = request.GET.get('signature')

    # Verify payment signature (this should be done by Razorpay's API)
    try:
        razorpay_client.payment.verify_payment_signature({
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        })

        # Update payment status
        payment = Payment.objects.get(order_id=order_id)
        payment.status = Payment.COMPLETED
        payment.transaction_id = payment_id
        payment.save()

        return render(request, 'success.html', {'message': 'Payment successful', 'payment': payment})

    except Exception as e:
        return render(request, 'failure.html', {'error': f'Payment verification failed: {str(e)}'})


# views.py
def error_page(request):
    return render(request, 'error.html')

def success(request):
    return render(request, 'success.html')