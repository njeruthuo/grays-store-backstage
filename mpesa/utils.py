import base64
from datetime import datetime
import requests
import os
from dotenv import load_dotenv
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

load_dotenv()


def get_access_token():
    consumer_key = os.getenv('CONSUMER_KEY')
    consumer_secret = os.getenv('CONSUMER_SECRET')

    auth_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    response = requests.get(auth_url, auth=(consumer_key, consumer_secret))
    return response.json().get('access_token')


def generate_password():
    shortcode = os.getenv('MPESA_SHORTCODE')
    passkey = os.getenv('MPESA_PASSKEY')
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    password_string = f"{shortcode}{passkey}{timestamp}"
    return base64.b64encode(password_string.encode()).decode()


def generate_security_credential(initiator_password):
    cert_path = 'path_to_certificate.cer'
    with open(cert_path, 'r') as f:
        certificate = f.read()

    public_key = RSA.importKey(certificate)
    cipher = PKCS1_v1_5.new(public_key)
    encrypted = cipher.encrypt(initiator_password.encode())
    return base64.b64encode(encrypted).decode()
