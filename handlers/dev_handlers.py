from webapp2 import RequestHandler
from google.appengine.ext.deferred import deferred
from app_config import config
from models import User, Distributor, Domain, Tenant, ChromeOsDevice, PlayerCommandEvent, TenantEntityGroup, \
    DeviceIssueLog, Location
import random

USER_EMAIL = 'daniel.ternyak@agosto.com'
DISTRIBUTOR_NAME = 'Dunder'
SECOND_DISTRIBUTOR = "Mifflin"
DOMAIN = 'local.skykit.com'
TENANT_NAME = 'Acme, Inc.'
TENANT_CODE = 'acme_inc'
TENANT_ADMIN_EMAIL = 'admin@acme.com'
SECOND_TENANT_NAME = 'DaveDistribution'
SECOND_TENANT_CODE = 'davedistribution'
SECOND_TENANT_ADMIN_EMAIL = 'dave@dave.com'
DEVICE_ID = '132e235a-b346-4a37-a100-de49fa753a2a'
GCM_REGISTRATION_ID = '8d70a8d78a6dfa6df76dfasd'
MAC_ADDRESS = '54271e619346'
UNMANAGED_MAC_ADDRESS = '04271e61934b'
UNMANAGED_GCM_REGISTRATION_ID = '3c70a8d70a6dfa6df76dfas2'
SERIAL_NUMBER = 'E6MSCX057790'
array_of_devices_with_values = []


def create_email(first, last):
    return first + "." + last + "@agosto.com"


class SeedScript(RequestHandler):
    def get(self, user_first, user_last):
        deferred.defer(kick_off, user_first, user_last)
        self.response.out.write(
            "A SEED SCRIPT HAS BEEN KICKED OFF FOR {}. PLEASE WATCH FOR A COMPLETE STATEMENT IN THE TERMINAL".format(
                create_email(user_first, user_last))
        )


def kick_off(user_first, user_last):
    global USER_EMAIL
    USER_EMAIL = create_email(user_first, user_last)
    print "-------------------------------------------------------------------------------"
    print "SEED SCRIPT HAS BEGUN!!! "
    print "-------------------------------------------------------------------------------"
    print "-------------------------------------------------------------------------------"
    print "CREATE DATA FOR DATASTORE!!! "
    print "-------------------------------------------------------------------------------"
    make_data_for_a_distributor()
    print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    print "-------------------------------------------------------------------------------"
    print "COMPLETED SEED SCRIPT"
    print "-------------------------------------------------------------------------------"
    print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    print "THESE ARE THE DEVICES WITH EVENTS AND COMMANDS"
    global array_of_devices_with_values
    print array_of_devices_with_values



def make_data_for_a_distributor():
    ##########################################################################################
    # DISTRIBUTORS
    ##########################################################################################
    first_distributor = Distributor.query(Distributor.name == SECOND_DISTRIBUTOR).get()
    if not first_distributor:
        first_distributor = Distributor.create(name=SECOND_DISTRIBUTOR, active=True)
        first_distributor.put()
        print 'Distributor ' + first_distributor.name + ' created'
    else:
        print 'Distributor ' + first_distributor.name + ' already exists, so did not create'

    distributor = Distributor.query(Distributor.name == DISTRIBUTOR_NAME).get()
    if not distributor:
        distributor = Distributor.create(name=DISTRIBUTOR_NAME, active=True)
        distributor.put()
        print 'Distributor ' + distributor.name + ' created'
    else:
        print 'Distributor ' + distributor.name + ' already exists, so did not create'

    ##########################################################################################
    # USERS
    ##########################################################################################
    user = User.get_or_insert_by_email(email=USER_EMAIL)
    if not distributor:
        print 'Distributor ' + DISTRIBUTOR_NAME + ' not found'
        print 'Could not add ' + USER_EMAIL + ' to ' + DISTRIBUTOR_NAME
    else:
        if not user:
            print 'User with email ' + USER_EMAIL + ' not found. Could not add ' + USER_EMAIL + ' to ' + DISTRIBUTOR_NAME
        else:
            user.add_distributor(distributor.key, is_distributor_administrator=True)
            print 'SUCCESS! ' + user.email + ' is linked to ' + distributor.name
            user.add_distributor(first_distributor.key)
            print 'SUCCESS! ' + user.email + ' is linked to ' + first_distributor.name
    ##########################################################################################
    # DOMAINS
    ##########################################################################################
    domain = Domain.query(Domain.name == DOMAIN).get()
    if not domain:
        domain = Domain.create(name=DOMAIN,
                               distributor_key=distributor.key,
                               impersonation_admin_email_address='test@skykit.com',
                               active=True)
        domain.put()
        print 'Domain ' + domain.name + ' created'
    else:
        print 'Domain ' + domain.name + ' already exists, so did not creat'

    ##########################################################################################
    # CREATE TENANTS
    ##########################################################################################
    for i in range(1, 300):
        tenant_code = "my_tenant" + str(i)
        tenant_code = tenant_code.lower()
        tenant_code_datastore = Tenant.find_by_tenant_code(tenant_code)
        if not tenant_code_datastore:
            tenant = Tenant.create(tenant_code=tenant_code,
                                   name="my_tenant" + str(i),
                                   admin_email=TENANT_ADMIN_EMAIL,
                                   content_server_url='https://skykit-contentmanager-int.appspot.com',
                                   content_manager_base_url='https://skykit-contentmanager-int.appspot.com/content',
                                   domain_key=domain.key,
                                   active=True)
            tenant.put()
        print 'Tenant ' + tenant.name + ' created'
    else:
        print 'Tenant ' + tenant.name + ' already exists, so did not create'

    ##########################################################################################
    tenant = Tenant.find_by_tenant_code(SECOND_TENANT_CODE)
    if not tenant:
        tenant = Tenant.create(tenant_code=SECOND_TENANT_CODE,
                               name=SECOND_TENANT_NAME,
                               admin_email=SECOND_TENANT_ADMIN_EMAIL,
                               content_server_url='https://skykit-contentmanager-int.appspot.com',
                               content_manager_base_url='https://skykit-contentmanager-int.appspot.com/content',
                               domain_key=domain.key,
                               active=True)
        tenant.put()
        print 'Tenant ' + tenant.name + ' created'

    ##########################################################################################
    tenant = Tenant.find_by_tenant_code(TENANT_CODE)
    if not tenant:
        tenant = Tenant.create(tenant_code=TENANT_CODE,
                               name=TENANT_NAME,
                               admin_email=TENANT_ADMIN_EMAIL,
                               content_server_url='https://skykit-contentmanager-int.appspot.com',
                               content_manager_base_url='https://skykit-contentmanager-int.appspot.com/content',
                               domain_key=domain.key,
                               active=True)
        tenant.put()
        print 'Tenant ' + tenant.name + ' created'

    ##########################################################################################
    # CREATE LOCATIONS
    ##########################################################################################
    for i in range(1, 103):
        if Location.is_customer_location_code_unique("my_location" + str(i), tenant.key):
            location = Location.create(tenant_key=tenant.key,
                                       customer_location_name="my_location" + str(i),
                                       customer_location_code="my_location" + str(i))
            location.address = None
            location.city = None
            location.state = None
            location.postal_code = None
            location.dma = None
            location.active = True
            location.put()

    ##########################################################################################
    # UNMANAGED DEVICES
    ##########################################################################################
    unmanaged_device = ChromeOsDevice.get_unmanaged_device_by_mac_address(UNMANAGED_MAC_ADDRESS)
    if not unmanaged_device:

        unmanaged_device = ChromeOsDevice.create_unmanaged(
            gcm_registration_id=UNMANAGED_GCM_REGISTRATION_ID,
            mac_address=UNMANAGED_MAC_ADDRESS)
        unmanaged_device.tenant_key = tenant.key
        unmanaged_device.put()
        print 'Unmanaged device created with MAC ' + UNMANAGED_MAC_ADDRESS
    else:
        print 'Unmanaged device with MAC ' + unmanaged_device.mac_address + ' already exists, so did not create'

    ##########################################################################################
    # MANAGED DEVICES
    ##########################################################################################
    for i in range(1, 225):
        managed_device = ChromeOsDevice.get_by_device_id(DEVICE_ID + str(i))
        if not managed_device:
            managed_device = ChromeOsDevice.create_managed(
                tenant_key=tenant.key,
                gcm_registration_id=GCM_REGISTRATION_ID + str(i),
                device_id=DEVICE_ID + str(i),
                mac_address=str(i) + MAC_ADDRESS,
                ethernet_mac_address=str(i) + "ether" + MAC_ADDRESS
            )
            managed_device.serial_number = SERIAL_NUMBER + str(i)
            managed_device.put()
            print 'Managed device created with MAC ' + str(i) + MAC_ADDRESS

            if random.randint(1, 10) == 1:
                global array_of_devices_with_values
                array_of_devices_with_values.append(str(managed_device.serial_number))

                for z in range(1, 101):
                    issue = DeviceIssueLog.create(device_key=managed_device.key,
                                                  category=config.DEVICE_ISSUE_PLAYER_DOWN,
                                                  up=False,
                                                  storage_utilization=random.randint(1, 100),
                                                  memory_utilization=random.randint(1, 100),
                                                  program=str(random.randint(1, 100)),
                                                  program_id=managed_device.program_id,
                                                  last_error=managed_device.last_error,
                                                  )
                    issue.put()

                    payload = 'reset content'.format(i)
                    gcm_registration_id = 'gcm-registration-id-{0}'.format(i)
                    event = PlayerCommandEvent.create(device_urlsafe_key=managed_device.key.urlsafe(),
                                                      payload=payload, gcm_registration_id=gcm_registration_id)

                    event.put()
                    print 'Added ' + payload + ' event to ' + managed_device.key.urlsafe()
                    payload = 'reset player'.format(i)
                    gcm_registration_id = 'gcm-registration-id-{0}'.format(i)
                    event = PlayerCommandEvent.create(device_urlsafe_key=managed_device.key.urlsafe(),
                                                      payload=payload, gcm_registration_id=gcm_registration_id)
                    event.player_has_confirmed = True
                    event.put()
                    print 'Added ' + payload + ' event to ' + managed_device.key.urlsafe()
                    payload = 'panel on'.format(i)
                    gcm_registration_id = 'gcm-registration-id-{0}'.format(i)
                    event = PlayerCommandEvent.create(device_urlsafe_key=managed_device.key.urlsafe(),
                                                      payload=payload, gcm_registration_id=gcm_registration_id)

                    event.player_has_confirmed = True
                    event.put()
                    print 'Added ' + payload + ' event to ' + managed_device.key.urlsafe()

        else:
            print 'Managed device with Device ID ' + managed_device.device_id + ' already exists, so did not create'

    ##########################################################################################
    # PROOF OF PLAY
    #########################################################################################
    tenants = Tenant.query(ancestor=TenantEntityGroup.singleton().key)
    for tenant in tenants:
        if tenant.proof_of_play_url is None:
            tenant.proof_of_play_url = config.DEFAULT_PROOF_OF_PLAY_URL
            tenant.put()
        print '{0}: {1}'.format(tenant.name, tenant.proof_of_play_url)
