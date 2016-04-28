from webapp2 import RequestHandler
from google.appengine.ext.deferred import deferred
from google.appengine.ext import ndb
from app_config import config
from models import User, Distributor, Domain, Tenant, ChromeOsDevice, PlayerCommandEvent, TenantEntityGroup, \
    DeviceIssueLog, DistributorEntityGroup, Location, DistributorUser
import time
import random

USER_EMAIL = 'daniel.ternyak@agosto.com'
DISTRIBUTOR_NAME = 'Agosto'
DOMAIN = 'local.skykit.com'
TENANT_NAME = 'Acme, Inc.'
TENANT_CODE = 'acme_inc'
TENANT_ADMIN_EMAIL = 'admin@acme.com'
DEVICE_ID = '132e235a-b346-4a37-a100-de49fa753a2a'
GCM_REGISTRATION_ID = '8d70a8d78a6dfa6df76dfasd'
MAC_ADDRESS = '54271e619346'
UNMANAGED_MAC_ADDRESS = '04271e61934b'
UNMANAGED_GCM_REGISTRATION_ID = '3c70a8d70a6dfa6df76dfas2'
SERIAL_NUMBER = 'E6MSCX057790'


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
    print "DELETING CURRENT DATASTORE!!! "
    print "-------------------------------------------------------------------------------"
    delete_all()
    print "-------------------------------------------------------------------------------"
    print "CREATE DATA FOR DATASTORE!!! "
    print "-------------------------------------------------------------------------------"
    make_data_for_a_distributor()
    print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    print "-------------------------------------------------------------------------------"
    print "COMPLETED SEED SCRIPT"
    print "-------------------------------------------------------------------------------"
    print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"


def run_delete_multi_on_model(model):
    ndb.delete_multi(
        model.query().fetch(keys_only=True),
    )
    return True


def delete_all():
    models_to_delete = [
        DistributorEntityGroup,
        Location,
        DistributorUser,
        ChromeOsDevice,
        User,
        Distributor,
        Domain,
        Tenant,
        PlayerCommandEvent,
        TenantEntityGroup,
        DeviceIssueLog
    ]
    return [run_delete_multi_on_model(model) for model in models_to_delete]


def make_data_for_a_distributor():
    ##########################################################################################
    # DISTRIBUTORS
    ##########################################################################################
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
            user.add_distributor(distributor.key)
            print 'SUCCESS! ' + user.email + ' is linked to ' + distributor.name

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
        tenant_code = "AUTO_TENANT" + str(i)
        tenant_code = tenant_code.lower()
        tenant = Tenant.create(tenant_code=tenant_code,
                               name="AUTO_TENANT" + str(i),
                               admin_email=TENANT_ADMIN_EMAIL,
                               content_server_url='https://skykit-contentmanager-int.appspot.com',
                               content_manager_base_url='https://skykit-contentmanager-int.appspot.com/content',
                               domain_key=domain.key,
                               active=True)
        tenant.put()
        print 'Tenant ' + tenant.name + ' created'
    else:
        print 'Tenant ' + tenant.name + ' already exists, so did not create'

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
    for i in range(1, 26):
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
        else:
            print 'Managed device with Device ID ' + managed_device.device_id + ' already exists, so did not create'

    ##########################################################################################
    # COMMAND EVENTS
    ##########################################################################################
    time.sleep(2)
    query = ChromeOsDevice.query().order(ChromeOsDevice.created)
    devices = query.fetch(1000)
    print 'Device count = ' + str(len(devices))
    for device in devices:
        for i in range(1, 100):
            payload = 'reset content'.format(i)
            gcm_registration_id = 'gcm-registration-id-{0}'.format(i)
            event = PlayerCommandEvent.create(device_urlsafe_key=device.key.urlsafe(),
                                              payload=payload, gcm_registration_id=gcm_registration_id)

            event.put()
            print 'Added ' + payload + ' event to ' + device.key.urlsafe()
            payload = 'reset player'.format(i)
            gcm_registration_id = 'gcm-registration-id-{0}'.format(i)
            event = PlayerCommandEvent.create(device_urlsafe_key=device.key.urlsafe(),
                                              payload=payload, gcm_registration_id=gcm_registration_id)
            event.player_has_confirmed = True
            event.put()
            print 'Added ' + payload + ' event to ' + device.key.urlsafe()
            payload = 'panel on'.format(i)
            gcm_registration_id = 'gcm-registration-id-{0}'.format(i)
            event = PlayerCommandEvent.create(device_urlsafe_key=device.key.urlsafe(),
                                              payload=payload, gcm_registration_id=gcm_registration_id)

            event.player_has_confirmed = True
            event.put()
            print 'Added ' + payload + ' event to ' + device.key.urlsafe()

    ##########################################################################################
    # PROOF OF PLAY
    #########################################################################################
    tenants = Tenant.query(ancestor=TenantEntityGroup.singleton().key)
    for tenant in tenants:
        if tenant.proof_of_play_url is None:
            tenant.proof_of_play_url = config.DEFAULT_PROOF_OF_PLAY_URL
            tenant.put()
        print '{0}: {1}'.format(tenant.name, tenant.proof_of_play_url)
