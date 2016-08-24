from chrome_os_devices_api import ChromeOsDevicesApi
from organization_units_api import OrganizationUnitsApi
from models import ChromeOsDevice
import re
from provisioning_env import (
    on_development_server,
)


class TenantOUNameMigration(object):
    def __init__(self, prod_credentials=False,
                 int_credentials=False):
        self.ou_api = OrganizationUnitsApi('admin@dev.agosto.com', prod_credentials=prod_credentials,
                                           int_credentials=int_credentials)

    def migrate_all_existing_tenant_names(self):
        all_existing_tenant_OUs = [
            {
                "orgUnitPath": each["orgUnitPath"],
                "orgUnitId": each["orgUnitId"],
                "name": each["name"]
            } for each in self.ou_api.list()["organizationUnits"]]
        for each_ou in all_existing_tenant_OUs:
            all_devices_in_OU = self.list_all_devices_in_path(each_ou["orgUnitPath"])
            if len(all_devices_in_OU) == 0:
                print "THERE ARE NO DEVICES IN THIS TENANT OU." \
                      " I HAVE NO IDEA HOW TO RENAME IT, and I probably don't need to anyway"
            else:
                first_device_serial_code = all_devices_in_OU[0]["serialNumber"]
                if on_development_server:
                    # REPLACE ChromeOsDevice.get_by_serial_number with searching INT's Provisioning in dev env
                    device_entity = ChromeOsDevice.get_by_serial_number(first_device_serial_code)
                else:
                    device_entity = ChromeOsDevice.get_by_serial_number(first_device_serial_code)

                if device_entity:
                    tenant_code_of_device = device_entity.tenant_key.get().tenant_code
                    print "CORRECTED NAME OF TENANT: {} IS TENANT CODE: {}".format(each_ou["name"],
                                                                                   tenant_code_of_device)
                else:
                    print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                    print "{} DOES NOT EXIST IN DATASTORE".format(first_device_serial_code)


                    # if self.convert_tenant_name_to_tenant_code(each_ou["name"]) != each_ou["name"]:
                    #     self.patch_tenant_name(self.convert_tenant_name_to_tenant_code(each_name))

    @staticmethod
    def list_all_devices_in_path(orgUnitPath, int_credentials=True, prod_credentials=False):
        cdm_api = ChromeOsDevicesApi('admin@dev.agosto.com', int_credentials=int_credentials,
                                     prod_credentials=prod_credentials)
        devices_list = cdm_api.list('my_customer')

        # ensures that patterns like /Skykit/Agosto/Blah/<device> match, but /Skykit/AgostoDevTest does not ...
        # given an input of /Skykit/Agosto
        return [
            device for device in devices_list
            if orgUnitPath == device["orgUnitPath"]
            or (orgUnitPath in device["orgUnitPath"] and device["orgUnitPath"].split(orgUnitPath, 1)[1][0] == "/")
            ]

    @staticmethod
    def convert_tenant_name_to_tenant_code(tenant_name):
        new_tenant_code = tenant_name.lower()
        new_tenant_code = new_tenant_code.replace(' ', '_')
        new_tenant_code = re.sub('[^0-9a-zA-Z_]+', '', new_tenant_code)
        return new_tenant_code
