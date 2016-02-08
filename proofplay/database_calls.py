from models import Resource, ProgramRecord, Location, ScheduleWentLive, Device, GamestopStoreLocation, ProgramPlayEvent
from db import Session
import datetime


def retrieve_all_resources():
    session = Session()
    resources = [resource.resource_name for resource in session.query(Resource).all()]
    return resources


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
    return new_raw_event.id


def mark_raw_event_complete(raw_event_id):
    session = Session()

    entry = session.query(ProgramPlayEvent).filter_by(id=raw_event_id).first()
    if entry:
        entry.completed = True
        session.commit()


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


def insert_new_resource_or_get_existing(resource_name, resource_identifier):
    session = Session()

    resource_exits = session.query(Resource).filter_by(resource_name=resource_name).first()

    if not resource_exits:
        new_resource = Resource(
                resource_name=resource_name,
                resource_identifier=resource_identifier
        )
        session.add(new_resource)
        session.commit()
        return new_resource.id

    else:
        return resource_exits.id


def insert_new_location_or_get_existing(location_identifier):
    session = Session()

    location_exists = session.query(Location).filter_by(location_identifier=location_identifier).first()

    if not location_exists:
        new_location = Location(
                location_identifier=location_identifier
        )
        session.add(new_location)
        session.commit()
        return new_location.id

    return location_exists.id


def insert_new_device_or_get_existing(location_id, serial_number, device_key, tenant_code):
    session = Session()

    device_exists = session.query(Device).filter_by(serial_number=serial_number).first()

    if not device_exists:
        new_device = Device(
                location_id=location_id,
                serial_number=serial_number,
                device_key=device_key,
                tenant_code=tenant_code

        )

        session.add(new_device)
        session.commit()
        return new_device.id

    return device_exists.id


def insert_new_gamestop_store_location(location_name, serial_number):
    session = Session()

    already_exists = session.query(GamestopStoreLocation).filter_by(serial_number=serial_number).first()

    if not already_exists:
        new_pair = GamestopStoreLocation(
                location_name=location_name,
                serial_number=serial_number
        )

        session.add(new_pair)
        session.commit()


def get_gamestop_store_location_from_serial_via_db(serial):
    session = Session()
    location_id = session.query(GamestopStoreLocation).filter_by(serial_number=serial).first()

    if location_id:
        return location_id.location_name

    else:
        return False


def transform_resource_data_between_date_range_by_location(from_db):
    to_return = {}

    for item in from_db:
        location_id = item["location_id"]
        if location_id not in to_return:
            to_return[location_id] = []

        to_return[location_id].append(item)

    return to_return


def get_raw_program_record_data_for_resource_between_date_ranges_by_location(start_date, end_date, resource):
    session = Session()

    resource_id = session.query(Resource).filter_by(resource_name=resource).first().id

    rows = session.query(ProgramRecord).filter(
            ProgramRecord.ended_at.between(start_date, end_date)).filter(
            ProgramRecord.resource_id == resource_id).all()

    from_db = []

    for program_record in rows:
        d = {}
        d["location_id"] = program_record.full_location.location_identifier
        d["device_id"] = program_record.full_device.serial_number
        d["resource_id"] = program_record.full_resource.resource_name
        d["started_at"] = program_record.started_at
        d["ended_at"] = program_record.ended_at

        from_db.append(d)

    all_results = transform_resource_data_between_date_range_by_location(from_db)
    return all_results


def transform_resource_data_between_date_ranges_by_date(from_db):
    to_return = {}

    for item in from_db:
        started_at = item["started_at"]
        midnight_start_day = str(datetime.datetime.combine(started_at.date(), datetime.time()))

        if midnight_start_day not in to_return:
            to_return[midnight_start_day] = []

        to_return[midnight_start_day].append(item)

    return to_return


def get_raw_program_record_data_for_resource_between_date_ranges_by_date(start_date, end_date, resource):
    session = Session()
    resource_id = session.query(Resource).filter_by(resource_name=resource).first().id

    rows = session.query(ProgramRecord).filter(
            ProgramRecord.ended_at.between(start_date, end_date)).filter(
            ProgramRecord.resource_id == resource_id).all()

    from_db = []

    for program_record in rows:
        d = {
            "location_id": program_record.full_location.location_identifier,
            "device_id": program_record.full_device.serial_number,
            "resource_id": program_record.full_resource.resource_name,
            "started_at": program_record.started_at,
            "ended_at": program_record.ended_at
        }

        from_db.append(d)

    all_results = transform_resource_data_between_date_ranges_by_date(from_db)
    return all_results
