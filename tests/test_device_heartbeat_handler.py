from env_setup import setup_test_paths
from webtest import AppError

setup_test_paths()

import json
from agar.test import BaseTest, WebTest
from models import Distributor, Domain
from routes import application
from utils.web_util import build_uri
from app_config import config

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class TestDeviceHeartbeatHandler(BaseTest, WebTest):
    APPLICATION = application
    DISTRIBUTOR_NAME = 'agosto'
    CHROME_DEVICE_DOMAIN = 'dev.agosto.com'
    CHROME_DEVICE_DOMAIN_INACTIVE = 'inactive.agosto.com'
    FORBIDDEN = '403 Forbidden'
    IMPERSONATION_EMAIL = 'test@test.com'

    def setUp(self):
        super(TestDeviceHeartbeatHandler, self).setUp()
        self.distributor = Distributor.create(name=self.DISTRIBUTOR_NAME,
                                              active=True)
        self.distributor_key = self.distributor.put()
        self.domain = Domain.create(name=self.CHROME_DEVICE_DOMAIN,
                                    distributor_key=self.distributor_key,
                                    impersonation_admin_email_address=self.IMPERSONATION_EMAIL,
                                    active=True)
        self.domain_key = self.domain.put()
        self.inactive_domain = Domain.create(name=self.CHROME_DEVICE_DOMAIN_INACTIVE,
                                             distributor_key=self.distributor_key,
                                             impersonation_admin_email_address=self.IMPERSONATION_EMAIL,
                                             active=False)
        self.inactive_domain_key = self.inactive_domain.put()
        self.headers = {
            'Authorization': config.API_TOKEN,
            'X-Provisioning-Distributor': self.distributor_key.urlsafe()
        }
        self.bad_authorization_header = {
            'Authorization': 'Forget about it!',
            'X-Provisioning-Distributor': self.distributor_key.urlsafe()
        }


    ##################################################################################################################
    ## put
    ##################################################################################################################

    def test_device_resource_put_no_authorization_header_returns_forbidden(self):
        request_body = {'name': self.CHROME_DEVICE_DOMAIN,
                        'active': True,
                        'impersonation_admin_email_address': self.IMPERSONATION_EMAIL,
                        'distributor_key': self.distributor_key.urlsafe()}
        uri = build_uri('manage-domain', params_dict={'domain_key': self.domain_key.urlsafe()})
        response = self.put(uri, params=request_body, headers=self.bad_authorization_header)
        self.assertForbidden(response)

    def test_put_http_status_no_content(self):
        request_body = {'name': self.CHROME_DEVICE_DOMAIN,
                        'active': True,
                        'impersonation_admin_email_address': self.IMPERSONATION_EMAIL,
                        'distributor_key': self.distributor_key.urlsafe()}
        uri = build_uri('manage-domain', params_dict={'domain_key': self.domain_key.urlsafe()})
        response = self.put(uri, params=json.dumps(request_body), headers=self.headers)
        self.assertEqual('204 No Content', response.status)

    def test_put_updates_domain_entity_name(self):
        updated_domain_name = 'foobar.agosto.com'
        request_body = {'name': updated_domain_name,
                        'active': True,
                        'impersonation_admin_email_address': self.IMPERSONATION_EMAIL,
                        'distributor_key': self.distributor_key.urlsafe()}
        uri = build_uri('manage-domain', params_dict={'domain_key': self.domain_key.urlsafe()})
        self.put(uri, params=json.dumps(request_body), headers=self.headers)
        updated_domain = self.domain_key.get()
        self.assertEqual(updated_domain_name, updated_domain.name)

    def test_put_updates_domain_entity_impersonation_admin_email_address(self):
        impersonation_admin_email_address = 'bob.macneal@agosto.com'
        request_body = {'name': self.CHROME_DEVICE_DOMAIN,
                        'active': True,
                        'impersonation_admin_email_address': impersonation_admin_email_address,
                        'distributor_key': self.distributor_key.urlsafe()}
        uri = build_uri('manage-domain', params_dict={'domain_key': self.domain_key.urlsafe()})
        self.put(uri, params=json.dumps(request_body), headers=self.headers)
        updated_domain = self.domain_key.get()
        self.assertEqual(impersonation_admin_email_address, updated_domain.impersonation_admin_email_address)

    def test_put_updates_domain_entity_active_to_false(self):
        active = False
        request_body = {'name': self.CHROME_DEVICE_DOMAIN,
                        'active': active,
                        'impersonation_admin_email_address': self.IMPERSONATION_EMAIL,
                        'distributor_key': self.distributor_key.urlsafe()}
        uri = build_uri('manage-domain', params_dict={'domain_key': self.domain_key.urlsafe()})
        self.put(uri, params=json.dumps(request_body), headers=self.headers)
        updated_domain = self.domain_key.get()
        self.assertFalse(updated_domain.active)

    ##################################################################################################################
    ## delete
    ##################################################################################################################

    def test_delete_returns_no_content_status(self):
        uri = build_uri('manage-domain', params_dict={'domain_key': self.domain_key.urlsafe()})
        response = self.delete(uri, headers=self.headers)
        self.assertEqual(204, response.status_int)

    def test_delete_soft_deletes_domain(self):
        request_parameters = {}
        uri = build_uri('manage-domain', params_dict={'domain_key': self.domain_key.urlsafe()})
        response = self.get(uri, params=request_parameters, headers=self.headers)
        response_json = json.loads(response.body)
        self.assertEqual(response_json.get('active'), True)

        self.delete(uri, headers=self.headers)

        response = self.get(uri, params=request_parameters, headers=self.headers)
        response_json = json.loads(response.body)
        self.assertEqual(response_json.get('active'), False)
