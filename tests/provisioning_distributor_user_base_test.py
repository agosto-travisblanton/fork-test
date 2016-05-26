from env_setup import setup_test_paths

setup_test_paths()

from utils.web_util import build_uri
from models import Distributor, Domain
from routes import application
from provisioning_base_test import ProvisioningBaseTest
from app_config import config


class ProvisioningDistributorUserBase(ProvisioningBaseTest):
    APPLICATION = application
    AGOSTO = 'agosto'
    DISTRIBUTOR = 'Distributor'
    INACTIVE_DISTRIBUTOR = 'Inactive Distributor'
    FORBIDDEN = '403 Forbidden'
    CHROME_DEVICE_DOMAIN_BOB = 'bob.agosto.com'
    CHROME_DEVICE_DOMAIN_FOO = 'foo.agosto.com'
    IMPERSONATION_EMAIL = 'admin@skykit.com'

    def setUp(self):
        super(ProvisioningDistributorUserBase, self).setUp()
        self.headers = {
            'Authorization': config.API_TOKEN
        }
        self.bad_authorization_header = {
            'Authorization': 'Forget about it!'
        }
        self.default_distributor_name = "agosto"

        self.distributor_admin_user = self.create_distributor_admin(email='john.jones@demo.agosto.com',
                                                                    distributor_name=self.default_distributor_name)

        self.admin_user = self.create_platform_admin(email='jim.bob@demo.agosto.com',
                                                     distributor_name=self.default_distributor_name)

        self.user = self.create_user(email='dwight.schrute@demo.agosto.com',
                                     distributor_name=self.default_distributor_name)

        self.user_key = self.user.key

        self.agosto = Distributor.find_by_name(name=self.default_distributor_name)
        self.agosto_key = self.agosto.key

        self.distributor = Distributor.create(name=self.DISTRIBUTOR)
        self.distributor_key = self.distributor.put()

        self.user.add_distributor(self.distributor_key)

        self.inactive_distributor = Distributor.create(name=self.INACTIVE_DISTRIBUTOR, active=False)
        self.inactive_distributor_key = self.inactive_distributor.put()

        self.domain_bob = Domain.create(name=self.CHROME_DEVICE_DOMAIN_BOB,
                                        distributor_key=self.agosto_key,
                                        impersonation_admin_email_address=self.IMPERSONATION_EMAIL,
                                        active=True).put()

        self.domain_foo = Domain.create(name=self.CHROME_DEVICE_DOMAIN_FOO,
                                        distributor_key=self.agosto_key,
                                        impersonation_admin_email_address=self.IMPERSONATION_EMAIL,
                                        active=True).put()

        self.domain_inactive = Domain.create(name=self.CHROME_DEVICE_DOMAIN_BOB,
                                             distributor_key=self.agosto_key,
                                             impersonation_admin_email_address=self.IMPERSONATION_EMAIL,
                                             active=False).put()

        self.default_distributor = self.agosto_key.get()

        self.login_url = build_uri('login')
        self.logout_url = build_uri('logout')
        self.identity_url = build_uri('identity')
