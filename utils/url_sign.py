from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
import urllib
from app_config import config
import base64
import time
from utils.datetime_util import unix_time

GCS_API_ACCESS_ENDPOINT = 'https://storage.googleapis.com'

def sign_cloud_storage_url(gcs_filename, method='GET', content_type=None, content_md5=None, expiration=None):
    expiration = str(unix_time(expiration)) if expiration is not None else None

    urlsafe_filename = urllib.quote(gcs_filename)

    signature_string = '\n'.join([
        method,
        content_md5 or '',
        content_type or '',
        expiration or '',
        urlsafe_filename])

    key64 = config.SERVICE_PRIVATE_KEY
    key_der = base64.b64decode(key64)
    pem_key = RSA.importKey(key_der)

    signer = PKCS1_v1_5.new(pem_key)
    signature_hash = SHA256.new(signature_string)
    signature_bytes = signer.sign(signature_hash)
    signature = base64.b64encode(signature_bytes)

    query_params = {
        'GoogleAccessId': config.SERVICE_CLIENT_EMAIL,
        'Signature': signature
    }
    if expiration is not None:
        query_params['Expires'] = expiration

    return '{endpoint}{resource}?{querystring}'.format(endpoint=GCS_API_ACCESS_ENDPOINT, resource=urlsafe_filename,
        querystring=urllib.urlencode(query_params))

