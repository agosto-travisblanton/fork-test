from env_setup import setup_test_paths

setup_test_paths()

from utils.web_util import build_uri
from models import Distributor, Domain, ChromeOsDevice, Tenant
from routes import application
from provisioning_base_test import ProvisioningBaseTest
from app_config import config


class ProvisioningDistributorUserBase(ProvisioningBaseTest):
    APPLICATION = application
    AGOSTO = 'agosto'
    DISTRIBUTOR = 'Distributor'
    INACTIVE_DISTRIBUTOR = 'Inactive Distributor'
    TENANT_CODE = 'foobar'
    TENANT_NAME = 'Foobar'
    FORBIDDEN = '403 Forbidden'
    MAC_ADDRESS = 'bladfkdkddkdkd'
    TEST_GCM_REGISTRATION_ID = '3k3k3k3k3k3kdldldldld'
    TESTING_DEVICE_ID = '232jmkskkk34k42k3l423k2'
    CHROME_DEVICE_DOMAIN = 'default.agosto.com'
    CHROME_DEVICE_DOMAIN_BOB = 'bob.agosto.com'
    CHROME_DEVICE_DOMAIN_FOO = 'foo.agosto.com'
    IMPERSONATION_EMAIL = 'admin@skykit.com'
    ADMIN_EMAIL = 'foo@bar.com'
    CONTENT_SERVER_URL = 'https://www.content.com'
    CONTENT_MANAGER_BASE_URL = 'https://skykit-contentmanager-int.appspot.com'

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

        self.domain = Domain.create(name=self.CHROME_DEVICE_DOMAIN,
                                    distributor_key=self.agosto_key,
                                    impersonation_admin_email_address=self.IMPERSONATION_EMAIL,
                                    active=True)

        self.domain.put()

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

        self.tenant = Tenant.create(tenant_code=self.TENANT_CODE,
                                    name=self.TENANT_NAME,
                                    admin_email=self.ADMIN_EMAIL,
                                    content_server_url=self.CONTENT_SERVER_URL,
                                    content_manager_base_url=self.CONTENT_MANAGER_BASE_URL,
                                    domain_key=self.domain.key,
                                    active=True)

        self.tenant_key = self.tenant.put()

        self.device = ChromeOsDevice.create_managed(tenant_key=self.tenant_key,
                                                    device_id=self.TESTING_DEVICE_ID,
                                                    gcm_registration_id=self.TEST_GCM_REGISTRATION_ID,
                                                    mac_address=self.MAC_ADDRESS)
        self.device_key = self.device.put()
