from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
import urllib
from app_config import config
import base64
from agar.env import on_development_server
from web_util import build_uri

GCS_API_ACCESS_ENDPOINT = 'https://storage.googleapis.com'


def _sign_cloud_storage_url(gcs_filename, method='GET', content_type=None, content_md5=None, expiration=None):
    expiration = None

    urlsafe_filename = urllib.quote(gcs_filename)

    signature_string = '\n'.join([
        method,
        content_md5 or '',
        content_type or '',
        expiration or '',
        urlsafe_filename])

    rsa_key = RSA.importKey(config.PRIVATE_KEY)

    signer = PKCS1_v1_5.new(rsa_key)
    signature_hash = SHA256.new(signature_string)
    signature_bytes = signer.sign(signature_hash)
    signature = base64.b64encode(signature_bytes)

    query_params = {
        'GoogleAccessId': config.SERVICE_ACCOUNT_EMAIL,
        'Signature': signature
    }
    if expiration is not None:
        query_params['Expires'] = expiration

    return '{endpoint}{resource}?{querystring}'.format(endpoint=GCS_API_ACCESS_ENDPOINT, resource=urlsafe_filename,
                                                       querystring=urllib.urlencode(query_params))


def build_local_cloud_storage_download_url(gcs_filename, request_url=None):
    """ On dev-appserver, serve cloud storage files locally and bypass URL signing. """
    # FIXME: write test
    if request_url is None:
        request_url = 'http://localhost:8080'
    uri = build_uri('gcs-download', {'base64_filename': base64.b64encode(gcs_filename)})
    return '{}{}'.format(request_url, uri)


def sign_cloud_storage_url(gcs_filename, method='GET', content_type=None, content_md5=None, expiration=None,
                           request_url=None):
    signed_url = None
    if gcs_filename is not None:
        if on_development_server:
            signed_url = build_local_cloud_storage_download_url(gcs_filename, request_url)
        else:
            signed_url = _sign_cloud_storage_url(gcs_filename, method, content_type, content_md5, expiration)

    return signed_url
