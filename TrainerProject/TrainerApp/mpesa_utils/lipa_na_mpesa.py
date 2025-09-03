import base64
from datetime import datetime
import json
import time
from django.http import HttpResponse
import requests
from requests.auth import HTTPBasicAuth
from django.views.decorators.csrf import csrf_exempt

from TrainerApp.mpesa_utils import utils

def get_timestamp():
    unformatted_time = datetime.now()
    formatted_time = unformatted_time.strftime("%Y%m%d%H%M%S")
    return formatted_time

def generate_password(formatted_time):
    data_to_encode = (
        utils.business_short_code + utils.pass_key + formatted_time
    )

    encoded_string = base64.b64encode(data_to_encode.encode())
    # print(encoded_string) b'MjAxOTAyMjQxOTUwNTc='

    decoded_password = encoded_string.decode("utf-8")

    return decoded_password
def generate_access_token():
    consumer_key = utils.consumer_key
    consumer_secret = utils.consumer_secret
    api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    try:
        r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    except:
        r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret), verify=False)

    print(r.text)

    json_response = (
        r.json()
    )

    my_access_token = json_response["access_token"]

    return my_access_token


def stk_push(phone_number, access_token):
    date_time = get_timestamp()
    pwd = generate_password(date_time)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': "Bearer %s" %access_token
    }
    payload = {
        "BusinessShortCode": 174379,
        "Password": pwd,
        "Timestamp": date_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 1,
        "PartyA": phone_number,
        "PartyB": 174379,
        "PhoneNumber": phone_number,
        "CallBackURL": "https://tvettrainer.co.ke/callback",
        "AccountReference": "Tvet Trainer",
        "TransactionDesc": "Generate Learning Plan" 
    }
    response = requests.post('https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest',
                             json=payload,
                             headers=headers
                                )
    return response

def query_stk(request_id, access_token):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer %s' %access_token
    }

    payload = {
        "BusinessShortCode": 174379,
        "Password": generate_password(get_timestamp()),
        "Timestamp": get_timestamp(),
        "CheckoutRequestID": request_id,
    }

    response = requests.post('https://sandbox.safaricom.co.ke/mpesa/stkpushquery/v1/query', 
                             headers = headers, 
                             json = payload)
    print(response.text.encode('utf8'))
    return response
