from chrome_os_devices_api import ChromeOsDevicesApi
from organization_units_api import OrganizationUnitsApi
from models import ChromeOsDevice
import re
import json


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

        final_translation_dict = {}

        for each_ou in all_tenant_OUs:
            final_translation_dict[each_ou["name"]] = {}
            all_devices_in_OU = self.cod_api.list_all_devices_in_path(each_ou["orgUnitPath"])

            if len(all_devices_in_OU) == 0:
                final_translation_dict[each_ou["name"]]["tenant_code"] = "No Devices in Path / No Match"

            else:
                devices_that_werent_found = []
                final_translation_dict[each_ou["name"]]["not_found_devices"] = devices_that_werent_found
                device_found = False
                for each_device in all_devices_in_OU:
                    device_entity = ChromeOsDevice.get_by_serial_number(each_device["serialNumber"])
                    if device_entity:
                        device_found = True
                        tenant_code_of_device = device_entity.tenant_key.get().tenant_code
                        if tenant_code_of_device != each_ou["name"]:
                            final_translation_dict[each_ou["name"]]["tenant_code"] = tenant_code_of_device
                        else:
                            final_translation_dict[each_ou["name"]]["tenant_code"] = each_ou["name"]
                        del final_translation_dict[each_ou["name"]]["not_found_devices"]
                        break  # we don't need to keep looping through devices now that we found the tenant name                                                                  tenant_code_of_device)

                    else:
                        devices_that_werent_found.append(each_device["serialNumber"])

                if not device_found:
                    final_translation_dict[each_ou["name"]][
                        "tenant_code"] = "At least one device was found, but none match in datastore."
                    # if self.convert_tenant_name_to_tenant_code(each_ou["name"]) != each_ou["name"]:
                    #     self.patch_tenant_name(self.convert_tenant_name_to_tenant_code(each_name))
        print json.dumps(final_translation_dict, sort_keys=True, indent=4)

    @staticmethod
    def convert_tenant_name_to_tenant_code(tenant_name):
        new_tenant_code = tenant_name.lower()
        new_tenant_code = new_tenant_code.replace(' ', '_')
        new_tenant_code = re.sub('[^0-9a-zA-Z_]+', '', new_tenant_code)
        return new_tenant_code
