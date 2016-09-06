from chrome_os_devices_api import ChromeOsDevicesApi
from organization_units_api import OrganizationUnitsApi
from models import ChromeOsDevice, Tenant
import re
from google.appengine.ext import deferred
from google.appengine.api import mail


def convert_tenant_name_to_tenant_code(tenant_name):
    new_tenant_code = tenant_name.lower()
    new_tenant_code = new_tenant_code.replace(' ', '_')
    new_tenant_code = re.sub('[^0-9a-zA-Z_]+', '', new_tenant_code)
    return new_tenant_code


def migrate_all_existing_tenant_names(prod_credentials=False,
                                      int_credentials=False,
                                      stage_credentials=False,
                                      qa_credentials=False):
    if int_credentials:
        email = 'admin@dev.agosto.com'
    elif prod_credentials:
        email = 'skykit.api@skykit.agosto.com'
    elif stage_credentials:
        email = 'skykit.api@devstage.skykit.com'
    elif qa_credentials:
        email = 'skykit.api@devqa.skykit.com'

    ou_api = OrganizationUnitsApi(email, prod_credentials=prod_credentials,
                                  int_credentials=int_credentials,
                                  stage_credentials=stage_credentials,
                                  qa_credentials=qa_credentials)

    cod_api = ChromeOsDevicesApi(email, prod_credentials=prod_credentials,
                                 int_credentials=int_credentials,
                                 stage_credentials=stage_credentials,
                                 qa_credentials=qa_credentials)

    all_tenant_OUs = [
        {
            "orgUnitPath": each["orgUnitPath"],
            "orgUnitId": each["orgUnitId"],
            "name": each["name"]
        } for each in ou_api.list()["organizationUnits"]
        ]

    translation_map = {}

    for each_ou in all_tenant_OUs:
        translation_map[each_ou["name"]] = {}
        all_devices_in_OU = cod_api.list_all_devices_in_path(each_ou["orgUnitPath"])

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

                        # insert the ou_id for the tenant
                        tenant_entity.ou_id = each_ou["orgUnitId"]
                        tenant_entity.put()

                else:
                    translation_map[each_ou["name"]]["not_found_devices"].append(each_device["serialNumber"])

            if not device_found:
                tenant_by_ou_name = Tenant.find_by_tenant_code(each_ou["name"])
                tenant_by_converted_ou_name = Tenant.find_by_tenant_code(
                    convert_tenant_name_to_tenant_code(each_ou["name"]))

                if tenant_by_ou_name:
                    translation_map[each_ou["name"]]["tenant_code"] = tenant_code + " (found via exact match)"
                    tenant_by_ou_name.ou_id = each_ou["orgUnitId"]
                    tenant_entity.put()

                elif tenant_by_converted_ou_name:
                    translation_map[each_ou["name"]]["tenant_code"] = tenant_code + " (found via converted ou name)"
                    tenant_by_ou_name.ou_id = each_ou["orgUnitId"]
                    tenant_entity.put()

                else:
                    message = "No match for device(s) found in datastore. No match to a Provisioning Tenant can be made"
                    translation_map[each_ou["name"]]["tenant_code"] = message

    mail.send_mail(sender='gcp.admin@agosto.com',
                   to="Daniel Ternyak <daniel.ternyak@agosto.com>",
                   subject='Migration',
                   body=str(translation_map))

    print "MIGRATION END"


def migrate(prod_credentials=False,
            int_credentials=False,
            stage_credentials=False,
            qa_credentials=False):
    print "MIGRATION BEGIN"
    deferred.defer(migrate_all_existing_tenant_names, prod_credentials=prod_credentials,
                   int_credentials=int_credentials,
                   stage_credentials=stage_credentials,
                   qa_credentials=qa_credentials)
