from proofplay_models import Resource, ProgramRecord, Location, Device, ProgramPlayEvent
from db import Session
from data_processing import transform_resource_data_between_date_range_by_location_to_dict_by_device, \
    transform_resource_data_between_date_ranges_by_date
import datetime
from models import Domain, Tenant, TenantEntityGroup
from google.appengine.ext import ndb


def get_tenant_names_for_distributor(distributor_key):
    return [result.tenant_code for result in get_tenant_list_from_distributor_key(distributor_key)]


def retrieve_all_devices_of_tenant(tenant):
    session = Session()
    search = session.query(Device.customer_display_code.distinct().label("customer_display_code"))
    session.close()
    return [row.customer_display_code for row in search.all()]


def retrieve_all_resources_of_tenant(tenant):
    session = Session()
    search = session.query(Resource).filter(Resource.tenant_code == tenant).all()
    session.close()
    return [resource.resource_name for resource in search]


def retrieve_all_resources():
    session = Session()
    search = session.query(Resource).all()
    session.close()
    return [resource.resource_name for resource in search]


def insert_raw_program_play_event_data(each_log):
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


def mark_raw_event_complete(raw_event_id):
    session = Session()

    entry = session.query(ProgramPlayEvent).filter_by(id=raw_event_id).first()
    if entry:
        entry.completed = True
        session.commit()
    session.close()


def insert_new_program_record(location_id, device_id, resource_id, started_at, ended_at):
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


def insert_new_resource_or_get_existing(resource_name, resource_identifier, tenant_code):
    session = Session()

    resource_exits = session.query(Resource).filter_by(resource_name=resource_name).first()

    if not resource_exits:
        new_resource = Resource(
                resource_name=resource_name,
                resource_identifier=resource_identifier,
                tenant_code=tenant_code
        )
        session.add(new_resource)
        session.commit()
        session.close()
        return new_resource.id

    else:
        session.close()
        return resource_exits.id


def insert_new_location_or_get_existing(customer_location_code):
    session = Session()

    location_exists = session.query(Location).filter_by(customer_location_code=customer_location_code).first()

    if not location_exists:
        new_location = Location(
                customer_location_code=customer_location_code
        )
        session.add(new_location)
        session.commit()
        session.close()
        return new_location.id

    session.close()
    return location_exists.id


def insert_new_device_or_get_existing(location_id, serial_number, device_key, customer_display_code, tenant_code):
    session = Session()

    device_exists = session.query(Device).filter_by(serial_number=serial_number).first()

    if not device_exists:
        new_device = Device(
                location_id=location_id,
                serial_number=serial_number,
                device_key=device_key,
                customer_display_code=customer_display_code,
                tenant_code=tenant_code

        )

        session.add(new_device)
        session.commit()
        session.close()
        return new_device.id

    session.close()
    return device_exists.id


def program_record_for_resource_by_location(start_date, end_date, resource, tenant_code):
    from_db = get_raw_program_record_data(start_date, end_date, resource, tenant_code)
    all_results = transform_resource_data_between_date_range_by_location_to_dict_by_device(from_db)
    return all_results


def program_record_for_resource_by_date(start_date, end_date, resource, tenant_code):
    from_db = get_raw_program_record_data(start_date, end_date, resource, tenant_code)
    all_results = transform_resource_data_between_date_ranges_by_date(from_db)
    return all_results


def get_raw_program_record_data(start_date, end_date, resource, tenant_code):
    session = Session()
    resource_id = session.query(Resource).filter_by(resource_name=resource).first().id

    rows = session.query(ProgramRecord).filter(
            ProgramRecord.ended_at.between(start_date, end_date)).filter(
            ProgramRecord.resource_id == resource_id).filter(
            ProgramRecord.full_device.has(tenant_code=tenant_code)).all()

    from_db = []

    for program_record in rows:
        d = {
            "location_id": program_record.full_location.customer_location_code,
            "device_id": program_record.full_device.serial_number,
            "resource_id": program_record.full_resource.resource_name,
            "started_at": program_record.started_at,
            "ended_at": program_record.ended_at
        }

        from_db.append(d)

    session.close()
    return from_db


####################################################################################

def get_raw_program_data_by_device(start_date, end_date, customer_display_code, tenant_code):
    session = Session()
    device_id = session.query(Device).filter_by(customer_display_code=customer_display_code).first().id

    rows = session.query(ProgramRecord) \
        .filter(
            ProgramRecord.ended_at.between(start_date, end_date)) \
        .filter(
            ProgramRecord.device_id == device_id) \
        .filter(
            ProgramRecord.full_device.has(tenant_code=tenant_code)).all()

    from_db = []

    for program_record in rows:
        d = {
            "location_id": program_record.full_location.customer_location_code,
            "device_id": program_record.full_device.customer_display_code,
            "resource_id": program_record.full_resource.resource_name,
            "started_at": program_record.started_at,
            "ended_at": program_record.ended_at
        }

        from_db.append(d)

    session.close()
    return transform_resource_data_between_date_range_by_location_to_dict_by_device(
            from_db)


####################################################################################

def get_tenant_list_from_distributor_key(distributor_key):
    distributor = ndb.Key(urlsafe=distributor_key)
    domain_keys = Domain.query(Domain.distributor_key == distributor).fetch(100, keys_only=True)
    tenant_list = Tenant.query(ancestor=TenantEntityGroup.singleton().key)
    tenant_list = filter(lambda x: x.active is True, tenant_list)
    result = filter(lambda x: x.domain_key in domain_keys, tenant_list)
    return result
