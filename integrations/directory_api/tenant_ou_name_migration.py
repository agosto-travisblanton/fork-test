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
        self.cod_api = ChromeOsDevicesApi('admin@dev.agosto.com', prod_credentials=prod_credentials,
                                           int_credentials=int_credentials)

    def migrate_all_existing_tenant_names(self):
        all_tenant_OUs = [
            {
                "orgUnitPath": each["orgUnitPath"],
                "orgUnitId": each["orgUnitId"],
                "name": each["name"]
            } for each in self.ou_api.list()["organizationUnits"]]

        for each_ou in all_tenant_OUs:
            all_devices_in_OU = self.cod_api.list_all_devices_in_path(each_ou["orgUnitPath"])

            if len(all_devices_in_OU) == 0:
                print "THERE ARE NO DEVICES IN TENANT: {}".format(each_ou["name"])
                print "RENAME FOR {} FAILED".format(each_ou["name"])

            else:
                # any device in this OU will have a serial number that corresponds to a device entity
                # in provisioning that will have the tenant_code associated with the tenant_key KeyProperty
                first_device_serial_code = all_devices_in_OU[0]["serialNumber"]

                if on_development_server:
                    # REPLACE ChromeOsDevice.get_by_serial_number with searching INT's Provisioning in dev env
                    device_entity = ChromeOsDevice.get_by_serial_number(first_device_serial_code)

                else:
                    device_entity = ChromeOsDevice.get_by_serial_number(first_device_serial_code)

                # if we find the device by serial_code
                if device_entity:
                    tenant_code_of_device = device_entity.tenant_key.get().tenant_code
                    print "CORRECTED NAME OF TENANT OU NAME: {} IS TENANT CODE: {}".format(each_ou["name"],
                                                                                   tenant_code_of_device)
                else:
                    print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                    print "{} DOES NOT EXIST IN DATASTORE".format(first_device_serial_code)
                    print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"


                    # if self.convert_tenant_name_to_tenant_code(each_ou["name"]) != each_ou["name"]:
                    #     self.patch_tenant_name(self.convert_tenant_name_to_tenant_code(each_name))

    @staticmethod
    def convert_tenant_name_to_tenant_code(tenant_name):
        new_tenant_code = tenant_name.lower()
        new_tenant_code = new_tenant_code.replace(' ', '_')
        new_tenant_code = re.sub('[^0-9a-zA-Z_]+', '', new_tenant_code)
        return new_tenant_code
