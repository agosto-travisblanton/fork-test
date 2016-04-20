# database_calls.py
from proofplay_models import Resource, ProgramRecord, Location, Device, ProgramPlayEvent, TenantCode
from db import Session
from data_processing import (
    transform_db_data_to_by_device,
    transform_db_data_to_by_date,
    transform_db_data_to_by_location_then_resource
)
import datetime
from models import Domain, Tenant, TenantEntityGroup
from google.appengine.ext import ndb
from proofplay_config import config
import logging
import time


def unique_tenant_resource_identifier(resource_identifier, tenant_code):
    return str(resource_identifier) + "__" + str(tenant_code)


####################################################################################
# Maintenance
####################################################################################
def delete_raw_event_entries_older_than_thirty_days(retries=0):
    session = Session()
    now = datetime.datetime.now()
    midnight_now = datetime.datetime.combine(now.date(), datetime.time())
    thirty_days_ago = midnight_now - datetime.timedelta(days=config.DAYS_TO_KEEP_RAW_EVENTS)
    session.query(ProgramPlayEvent).filter(ProgramPlayEvent.started_at <= thirty_days_ago).delete()
    session.commit()
    session.close()


####################################################################################
# REST Queries
####################################################################################
def retrieve_all_devices_of_tenant(tenant, retries=0):
    session = Session()
    tenant = session.query(TenantCode).filter_by(tenant_code=tenant).first()
    if tenant:
        tenant_id = tenant.id

        search = session.query(Device.customer_display_code.distinct().label("customer_display_code")).filter(
            Device.tenant_id == tenant_id)

        session.close()

        return [row.customer_display_code for row in search.all()]

    else:
        session.close()
        return []


def retrieve_all_locations_of_tenant(tenant, retries=0):
    session = Session()
    tenant = session.query(TenantCode).filter_by(tenant_code=tenant).first()

    if tenant:
        tenant_id = tenant.id

        search = session.query(Device.location_id.distinct().label("location_id")).filter(
            Device.tenant_id == tenant_id)
        session.close()
        location_ids = [row.location_id for row in search.all()]
        return map(retrieve_customer_location_code_from_location_id, location_ids)

    else:
        session.close()
        return []


def retrieve_customer_location_code_from_location_id(location_id, retries=0):
    session = Session()
    search = session.query(Location).filter_by(id=location_id).first().customer_location_code
    session.close()
    return search


def retrieve_all_resources_of_tenant(tenant, retries=0):
    session = Session()
    tenant = session.query(TenantCode).filter_by(tenant_code=tenant).first()
    if tenant:
        tenant_id = tenant.id
        search = session.query(Resource).filter(Resource.tenant_id == tenant_id).all()
        session.close()
        return [
            {
                "resource_name": resource.resource_name,
                "resource_identifier": resource.resource_identifier
            } for resource in search]
    else:
        session.close()
        return []


def retrieve_resource_name_from_resource_identifier(modified_resource_identifier, retries=0):
    session = Session()
    resource_name = session.query(Resource).filter_by(
        resource_identifier=modified_resource_identifier).first().resource_name
    session.close()
    return resource_name


def retrieve_all_resources(retries=0):
    session = Session()
    search = session.query(Resource).all()
    session.close()
    return [resource.resource_name for resource in search]


####################################################################################
# Inserts / updates
####################################################################################
def insert_raw_program_play_event_data(each_log, retries=0):
    session = Session()
    new_raw_event = ProgramPlayEvent(
        resource_name=each_log["resource_name"],
        resource_id=each_log["resource_id"],
        serial_number=each_log["serial_number"],
        device_key=each_log["device_key"],
        tenant_code=each_log["tenant_code"],
        started_at=datetime.datetime.strptime(each_log["started_at"], '%Y-%m-%dT%H:%M:%S.%fZ'),
        ended_at=datetime.datetime.strptime(each_log["ended_at"], '%Y-%m-%dT%H:%M:%S.%fZ')
    )
    session.add(new_raw_event)
    session.commit()
    session.close()
    return new_raw_event.id


def mark_raw_event_complete(raw_event_id, retries=0):
    session = Session()

    entry = session.query(ProgramPlayEvent).filter_by(id=raw_event_id).first()
    if entry:
        entry.completed = True
        session.commit()
    session.close()


def insert_new_program_record(location_id, device_id, resource_id, started_at, ended_at, retries=0):
    session = Session()

    new_program_record = ProgramRecord(
        location_id=location_id,
        resource_id=resource_id,
        device_id=device_id,
        started_at=started_at,
        ended_at=ended_at
    )

    session.add(new_program_record)
    session.commit()
    session.close()
    return True


def insert_new_resource_or_get_existing(resource_name, resource_identifier, tenant_code, retries=0):
    session = Session()
    unique_resource_identifier = unique_tenant_resource_identifier(
        resource_identifier=resource_identifier,
        tenant_code=tenant_code
    )
    resource_exists = session.query(Resource).filter_by(resource_identifier=unique_resource_identifier).first()

    if not resource_exists:
        tenant_id = session.query(TenantCode).filter_by(tenant_code=tenant_code).first().id

        new_resource = Resource(
            resource_name=resource_name,
            resource_identifier=unique_resource_identifier,
            tenant_id=tenant_id
        )
        session.add(new_resource)
        session.commit()
        session.close()
        return new_resource.id

    else:
        if resource_exists.resource_name != resource_name:
            resource_exists.resource_name = resource_name
            session.add(resource_exists)
            session.commit()

        session.close()
        return resource_exists.id


def insert_new_tenant_code_or_get_existing(tenant_code, retries=0):
    session = Session()

    tenant_exists = session.query(TenantCode).filter_by(tenant_code=tenant_code).first()

    if not tenant_exists:
        new_tenant = TenantCode(
            tenant_code=tenant_code,

        )
        session.add(new_tenant)
        session.commit()
        session.close()
        return new_tenant.id

    else:
        return tenant_exists.id


def insert_new_location_or_get_existing(customer_location_code, tenant_id, retries=0):
    session = Session()

    location_exists = session.query(Location).filter_by(customer_location_code=customer_location_code).filter_by(
        tenant_id=tenant_id).first()

    if not location_exists:
        new_location = Location(
            customer_location_code=customer_location_code,
            tenant_id=tenant_id
        )
        session.add(new_location)
        session.commit()
        session.close()
        return new_location.id

    session.close()
    return location_exists.id


def insert_new_device_or_get_existing(location_id, serial_number, device_key, customer_display_code, tenant_code,
                                      retries=0):
    session = Session()

    device_exists = session.query(Device).filter_by(device_key=device_key).filter_by(
        customer_display_code=customer_display_code).first()

    if not device_exists:
        tenant_id = session.query(TenantCode).filter_by(tenant_code=tenant_code).first().id

        new_device = Device(
            location_id=location_id,
            serial_number=serial_number,
            device_key=device_key,
            customer_display_code=customer_display_code,
            tenant_id=tenant_id

        )

        session.add(new_device)
        session.commit()
        session.close()
        return new_device.id

    session.close()
    return device_exists.id


####################################################################################
# CSV Queries
####################################################################################
####################################################################################
# BY RESOURCE
####################################################################################
def program_record_for_resource_by_device(start_date, end_date, resource, tenant_code):
    from_db = get_raw_program_record_data_by_resource(start_date, end_date, resource, tenant_code)
    all_results = transform_db_data_to_by_device(from_db)
    return all_results


def program_record_for_resource_by_date(start_date, end_date, resource, tenant_code):
    from_db = get_raw_program_record_data_by_resource(start_date, end_date, resource, tenant_code)
    all_results = transform_db_data_to_by_date(from_db)
    return all_results


def get_raw_program_record_data_by_resource(start_date, end_date, resource_identifier, tenant_code, retries=0):
    session = Session()

    resource_id = session.query(Resource).filter_by(resource_identifier=resource_identifier).first().id
    tenant_id = session.query(TenantCode).filter_by(tenant_code=tenant_code).first().id

    rows = session.query(ProgramRecord).filter(
        ProgramRecord.ended_at.between(start_date, end_date)).filter(
        ProgramRecord.resource_id == resource_id).filter(
        ProgramRecord.full_device.has(tenant_id=tenant_id)).all()

    from_db = []

    for program_record in rows:
        d = {
            "location_id": program_record.full_location.customer_location_code if program_record.full_location else "None",
            "device_id": program_record.full_device.customer_display_code,
            "resource_id": program_record.full_resource.resource_name,
            "started_at": program_record.started_at,
            "ended_at": program_record.ended_at
        }

        from_db.append(d)

    session.close()
    return from_db


####################################################################################
# BY DEVICE
####################################################################################
def program_record_for_device_by_date(start_date, end_date, customer_display_code, tenant_code):
    from_db = get_raw_program_record_data_by_device(start_date, end_date, customer_display_code, tenant_code)
    return transform_db_data_to_by_date(from_db)


def program_record_for_device_summarized(start_date, end_date, customer_display_code, tenant_code):
    from_db = get_raw_program_record_data_by_device(start_date, end_date, customer_display_code, tenant_code)
    return transform_db_data_to_by_device(from_db)


def get_raw_program_record_data_by_device(start_date, end_date, customer_display_code, tenant_code, retries=0):
    session = Session()
    device_id = session.query(Device).filter_by(customer_display_code=customer_display_code).first().id
    tenant_id = session.query(TenantCode).filter_by(tenant_code=tenant_code).first().id

    rows = session.query(ProgramRecord) \
        .filter(
        ProgramRecord.ended_at.between(start_date, end_date)) \
        .filter(
        ProgramRecord.device_id == device_id) \
        .filter(
        ProgramRecord.full_device.has(tenant_id=tenant_id)).all()

    from_db = []

    for program_record in rows:
        d = {
            "location_id": program_record.full_location.customer_location_code if program_record.full_location else "None",
            "device_id": program_record.full_device.customer_display_code,
            "resource_id": program_record.full_resource.resource_name,
            "started_at": program_record.started_at,
            "ended_at": program_record.ended_at
        }

        from_db.append(d)

    session.close()
    return from_db


####################################################################################
# BY LOCATION
####################################################################################
def program_record_for_location_summarized(start_date, end_date, customer_location_code, tenant_code):
    from_db = get_raw_program_record_data_by_location(start_date, end_date, customer_location_code, tenant_code)
    return transform_db_data_to_by_location_then_resource(from_db)


def get_raw_program_record_data_by_location(start_date, end_date, customer_location_code, tenant_code, retries=0):
    session = Session()
    location_id = session.query(Location).filter_by(customer_location_code=customer_location_code).first().id
    tenant_id = session.query(TenantCode).filter_by(tenant_code=tenant_code).first().id

    rows = session.query(ProgramRecord) \
        .filter(
        ProgramRecord.ended_at.between(start_date, end_date)) \
        .filter(
        ProgramRecord.location_id == location_id) \
        .filter(
        ProgramRecord.full_device.has(tenant_id=tenant_id)).all()

    from_db = []

    for program_record in rows:
        d = {
            "location_id": program_record.full_location.customer_location_code if program_record.full_location else "None",
            "device_id": program_record.full_device.customer_display_code,
            "resource_id": program_record.full_resource.resource_name,
            "started_at": program_record.started_at,
            "ended_at": program_record.ended_at
        }

        from_db.append(d)

    session.close()
    return from_db


####################################################################################
# DataStore Related
####################################################################################
def tenant_code_from_urlsafe_key(urlsafe_key):
    tenant_key = ndb.Key(urlsafe=urlsafe_key)
    if tenant_key:
        return tenant_key.get().tenant_code
    return None


def get_tenant_list_from_distributor_key(distributor_key):
    distributor = ndb.Key(urlsafe=distributor_key)
    domain_keys = Domain.query(Domain.distributor_key == distributor).fetch(100, keys_only=True)
    tenant_list = Tenant.query(ancestor=TenantEntityGroup.singleton().key)
    tenant_list = filter(lambda x: x.active is True, tenant_list)
    result = filter(lambda x: x.domain_key in domain_keys, tenant_list)
    return result


def get_tenant_names_for_distributor(distributor_key):
    return [result.tenant_code.encode('ascii', 'ignore')
            for result in
            get_tenant_list_from_distributor_key(distributor_key)]
