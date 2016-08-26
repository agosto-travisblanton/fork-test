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

        translation_map = {}

        for each_ou in all_tenant_OUs:
            translation_map[each_ou["name"]] = {}
            all_devices_in_OU = self.cod_api.list_all_devices_in_path(each_ou["orgUnitPath"])

            if len(all_devices_in_OU) == 0:
                message = "No Devices in OrgUnitPath. No match to a Provisioning Tenant can be made."
                translation_map[each_ou["name"]]["tenant_code"] = message

            else:
                translation_map[each_ou["name"]]["not_found_devices"] = []
                device_found = False

                for each_device in all_devices_in_OU:
                    device_entity = ChromeOsDevice.get_by_serial_number(each_device["serialNumber"])
                    if device_entity:
                        # we would have already identified the tenant of the tenant_ou if a previous device was found.
                        # however, there could be other devices in the Tenant OU that provisioning doesn't know about.
                        # it will be helpful to collect all of these devices.
                        if not device_found:
                            device_found = True
                            tenant_entity = device_entity.tenant_key.get()
                            tenant_code = tenant_entity.tenant_code

                            if tenant_code != each_ou["name"]:
                                translation_map[each_ou["name"]]["tenant_code"] = tenant_code
                            else:
                                translation_map[each_ou["name"]]["tenant_code"] = each_ou["name"]

                            del translation_map[each_ou["name"]]["not_found_devices"]

                            tenant_entity.ou_id = each_ou["orgUnitId"]
                            tenant_entity.put()

                            # updates org unit path (tenant OU's) name with new with new_tenant_code argument
                            # WE DON'T WANT TO DO THIS YET!!!
                            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                            # self.ou_api.patch_tenant_name(
                            #     org_unit_path=each_ou["orgUnitPath"],
                            #     new_tenant_code=tenant_code_of_device
                            # )
                            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

                    else:
                        translation_map[each_ou["name"]]["not_found_devices"].append(each_device["serialNumber"])

                if not device_found:
                    message = "No match for device(s) found in datastore. No match to a Provisioning Tenant can be made"
                    translation_map[each_ou["name"]]["tenant_code"] = message

        print json.dumps(translation_map, sort_keys=True, indent=4)

    @staticmethod
    def convert_tenant_name_to_tenant_code(tenant_name):
        new_tenant_code = tenant_name.lower()
        new_tenant_code = new_tenant_code.replace(' ', '_')
        new_tenant_code = re.sub('[^0-9a-zA-Z_]+', '', new_tenant_code)
        return new_tenant_code
