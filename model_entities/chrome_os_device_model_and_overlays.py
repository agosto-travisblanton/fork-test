import logging
import uuid

from datetime import datetime
from google.appengine.ext import ndb
import ndb_json

from app_config import config
from restler.decorators import ae_ndb_serializer
from utils.timezone_util import TimezoneUtil


@ae_ndb_serializer
class ChromeOsDevice(ndb.Model):
    tenant_key = ndb.KeyProperty(required=False, indexed=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    device_id = ndb.StringProperty(required=False, indexed=True)
    gcm_registration_id = ndb.StringProperty(required=True)
    mac_address = ndb.StringProperty(required=True, indexed=True)
    api_key = ndb.StringProperty(required=True, indexed=True)
    serial_number = ndb.StringProperty(required=False, indexed=True)
    status = ndb.StringProperty(required=False, indexed=False)
    last_sync = ndb.StringProperty(required=False, indexed=False)
    kind = ndb.StringProperty(required=False, indexed=False)
    ethernet_mac_address = ndb.StringProperty(required=False, indexed=True)
    org_unit_path = ndb.StringProperty(required=False, indexed=False)
    annotated_user = ndb.StringProperty(required=False, indexed=False)
    annotated_location = ndb.StringProperty(required=False, indexed=False)
    annotated_asset_id = ndb.StringProperty(required=False, indexed=False)
    notes = ndb.StringProperty(required=False, indexed=False)
    boot_mode = ndb.StringProperty(required=False, indexed=False)
    last_enrollment_time = ndb.StringProperty(required=False, indexed=False)
    platform_version = ndb.StringProperty(required=False, indexed=False)
    model = ndb.StringProperty(required=False, indexed=False)
    os = ndb.StringProperty(required=False, indexed=False)
    os_version = ndb.StringProperty(required=False, indexed=False)
    firmware_version = ndb.StringProperty(required=False, indexed=False)
    etag = ndb.StringProperty(required=False, indexed=False)
    name = ndb.ComputedProperty(lambda self: '{0} {1}'.format(self.serial_number, self.model))
    loggly_link = ndb.ComputedProperty(lambda self: 'https://skykit.loggly.com/search?&terms=tag%3A"{0}"'.format(
        self.serial_number))
    is_unmanaged_device = ndb.BooleanProperty(default=False, required=True, indexed=True)
    pairing_code = ndb.StringProperty(required=False, indexed=True)
    panel_model = ndb.StringProperty(required=False, indexed=True)
    panel_input = ndb.StringProperty(required=False, indexed=True)
    heartbeat_updated = ndb.DateTimeProperty(required=False, auto_now=False, indexed=True)
    up = ndb.BooleanProperty(default=True, required=True, indexed=True)
    storage_utilization = ndb.IntegerProperty(default=0, required=True, indexed=True)
    memory_utilization = ndb.IntegerProperty(default=0, required=True, indexed=True)
    program = ndb.StringProperty(required=False, indexed=True)
    program_id = ndb.StringProperty(required=False, indexed=True)
    last_error = ndb.StringProperty(required=False, indexed=True)
    playlist = ndb.StringProperty(required=False, indexed=True)
    playlist_id = ndb.StringProperty(required=False, indexed=True)
    connection_type = ndb.StringProperty(required=False, indexed=True)
    sk_player_version = ndb.StringProperty(required=False, indexed=True)
    heartbeat_interval_minutes = ndb.IntegerProperty(default=config.PLAYER_HEARTBEAT_INTERVAL_MINUTES, required=True,
                                                     indexed=False)
    check_for_content_interval_minutes = ndb.IntegerProperty(default=config.CHECK_FOR_CONTENT_INTERVAL_MINUTES,
                                                             required=True, indexed=True)
    proof_of_play_logging = ndb.BooleanProperty(default=False, required=True, indexed=True)
    proof_of_play_editable = ndb.BooleanProperty(default=False, required=True)
    customer_display_name = ndb.StringProperty(required=False, indexed=True)
    customer_display_code = ndb.StringProperty(required=False, indexed=True)
    content_manager_display_name = ndb.StringProperty(required=False, indexed=True)
    content_manager_location_description = ndb.StringProperty(required=False, indexed=True)
    location_key = ndb.KeyProperty(required=False, indexed=True)
    timezone = ndb.StringProperty(required=False, indexed=True)
    timezone_offset = ndb.IntegerProperty(required=False, indexed=True)  # computed property
    registration_correlation_identifier = ndb.StringProperty(required=False, indexed=True)
    archived = ndb.BooleanProperty(default=False, required=True, indexed=True)
    panel_sleep = ndb.BooleanProperty(default=False, required=True, indexed=True)
    overlay_available = ndb.BooleanProperty(default=False, required=True, indexed=True)
    class_version = ndb.IntegerProperty()

    def get_tenant(self):
        if self.tenant_key:
            return self.tenant_key.get()
        else:
            logging.debug(
                'Device has no tenant. Most likely an unmanaged device where tenant has not been specified.')
            return None

    @property
    def overlays(self):
        return OverlayTemplate.get_overlay_templates_for_device(self.key)

    @property
    def overlays_as_dict(self):
        """ This method is offered because restler doesn't support keyProperty serialization beyond a single child"""
        json = ndb_json.dumps(self.overlays)
        return ndb_json.loads(json)


    def enable_overlays(self):
        self.overlay_available = True
        self.put()
        return self

    @classmethod
    def get_by_device_id(cls, device_id):
        if device_id:
            chrome_os_device_key = ChromeOsDevice.query(ndb.AND(ChromeOsDevice.archived == False,
                                                                ChromeOsDevice.device_id == device_id)).get(
                keys_only=True)
            if chrome_os_device_key:
                return chrome_os_device_key.get()

    @classmethod
    def create_managed(cls, tenant_key, gcm_registration_id, mac_address, ethernet_mac_address=None, device_id=None,
                       serial_number=None, archived=False,
                       model=None, timezone='America/Chicago', registration_correlation_identifier=None):
        timezone_offset = TimezoneUtil.get_timezone_offset(timezone)
        proof_of_play_editable = False
        tenant = tenant_key.get()
        if tenant:
            if tenant.proof_of_play_logging:
                proof_of_play_editable = True
        device = cls(
            device_id=device_id,
            archived=archived,
            tenant_key=tenant_key,
            gcm_registration_id=gcm_registration_id,
            mac_address=mac_address,
            ethernet_mac_address=ethernet_mac_address,
            api_key=str(uuid.uuid4().hex),
            serial_number=serial_number,
            model=model,
            is_unmanaged_device=False,
            up=True,
            storage_utilization=0,
            memory_utilization=0,
            heartbeat_updated=datetime.utcnow(),
            program='****initial****',
            program_id='****initial****',
            playlist='****initial playlist****',
            playlist_id='****initial playlist id****',
            heartbeat_interval_minutes=config.PLAYER_HEARTBEAT_INTERVAL_MINUTES,
            timezone=timezone,
            timezone_offset=timezone_offset,
            proof_of_play_editable=proof_of_play_editable,
            registration_correlation_identifier=registration_correlation_identifier)
        return device

    @classmethod
    def create_unmanaged(cls,
                         gcm_registration_id,
                         mac_address,
                         timezone='America/Chicago',
                         registration_correlation_identifier=None):
        timezone_offset = TimezoneUtil.get_timezone_offset(timezone)
        device = cls(
            archived=False,
            gcm_registration_id=gcm_registration_id,
            mac_address=mac_address,
            api_key=str(uuid.uuid4().hex),
            pairing_code='{0}-{1}-{2}-{3}'.format(str(uuid.uuid4().hex)[:4], str(uuid.uuid4().hex)[:4],
                                                  str(uuid.uuid4().hex)[:4], str(uuid.uuid4().hex)[:4]),
            is_unmanaged_device=True,
            up=True,
            storage_utilization=0,
            memory_utilization=0,
            heartbeat_updated=datetime.utcnow(),
            program='****initial****',
            program_id='****initial****',
            playlist='****initial playlist****',
            playlist_id='****initial playlist id****',
            heartbeat_interval_minutes=config.PLAYER_HEARTBEAT_INTERVAL_MINUTES,
            timezone=timezone,
            timezone_offset=timezone_offset,
            proof_of_play_editable=False,
            registration_correlation_identifier=registration_correlation_identifier,
            model='unmanaged device',
            serial_number='no serial number')
        return device

    @classmethod
    def get_by_gcm_registration_id(cls, gcm_registration_id):
        if gcm_registration_id:
            results = ChromeOsDevice.query(ChromeOsDevice.gcm_registration_id == gcm_registration_id,
                                           ndb.AND(ChromeOsDevice.archived == False)).fetch()
            return results
        else:
            return None

    @classmethod
    def get_by_mac_address(cls, mac_address):
        if mac_address:
            results = ChromeOsDevice.query(
                ndb.OR(ChromeOsDevice.mac_address == mac_address,
                       ChromeOsDevice.ethernet_mac_address == mac_address),
                ndb.AND(ChromeOsDevice.archived == False)).fetch()
            return results
        else:
            return None

    @classmethod
    def get_by_pairing_code(cls, pairing_code):
        if pairing_code:
            results = ChromeOsDevice.query(ChromeOsDevice.pairing_code == pairing_code,
                                           ndb.AND(ChromeOsDevice.archived == False)).fetch()
            return results
        else:
            return None

    @classmethod
    def get_unmanaged_device_by_mac_address(cls, mac_address):
        if mac_address:
            device_key = ChromeOsDevice.query(ndb.AND(ChromeOsDevice.mac_address == mac_address,
                                                      ChromeOsDevice.is_unmanaged_device == True,
                                                      ChromeOsDevice.archived == False)).get(keys_only=True)
            if not device_key:
                return None
            else:
                return device_key.get()
        else:
            return None

    @classmethod
    def get_unmanaged_device_by_gcm_registration_id(cls, gcm_registration_id):
        if gcm_registration_id:
            device_key = ChromeOsDevice.query(ndb.AND(ChromeOsDevice.gcm_registration_id == gcm_registration_id,
                                                      ChromeOsDevice.is_unmanaged_device == True,
                                                      ChromeOsDevice.archived == False)).get(keys_only=True)
            if not device_key:
                return None
            else:
                return device_key.get()
        else:
            return None

    @classmethod
    def mac_address_already_assigned(cls, device_mac_address, is_unmanaged_device=False):
        mac_address_already_assigned_to_device = ChromeOsDevice.query(
            ndb.OR(ChromeOsDevice.mac_address == device_mac_address,
                   ChromeOsDevice.ethernet_mac_address == device_mac_address),
            ndb.AND(
                ChromeOsDevice.is_unmanaged_device == is_unmanaged_device,
                ChromeOsDevice.archived == False)).count() > 0
        return mac_address_already_assigned_to_device

    @classmethod
    def gcm_registration_id_already_assigned(cls, gcm_registration_id, is_unmanaged_device=False):
        gcm_registration_id_already_assigned_to_device = ChromeOsDevice.query(
            ndb.AND(ChromeOsDevice.gcm_registration_id == gcm_registration_id,
                    ChromeOsDevice.is_unmanaged_device == is_unmanaged_device,
                    ChromeOsDevice.archived == False)).count() > 0
        return gcm_registration_id_already_assigned_to_device

    @classmethod
    def is_rogue_unmanaged_device(cls, mac_address):
        device = ChromeOsDevice.get_unmanaged_device_by_mac_address(mac_address)
        if device is not None and device.pairing_code is not None and device.tenant_key is None:
            return True
        else:
            return False

    @classmethod
    def is_customer_display_code_unique(cls, customer_display_code, tenant_key):
        return None is ChromeOsDevice.query(
            ndb.AND(ChromeOsDevice.archived == False,
                    ChromeOsDevice.customer_display_code == customer_display_code,
                    ChromeOsDevice.tenant_key == tenant_key)).get(
            keys_only=True)

    def _pre_put_hook(self):
        self.class_version = 3

    def get_impersonation_email(self):
        return self.get_tenant().get_domain().impersonation_admin_email_address


#####################################################
# OVERLAYS
#####################################################
OVERLAY_POSITIONS = ["TOP_LEFT", "BOTTOM_LEFT", "BOTTOM_RIGHT", "TOP_RIGHT"]
OVERLAY_TYPES = ["TIME", "DATE", "DATETIME", "LOGO"]


@ae_ndb_serializer
class Image(ndb.Model):
    svg_rep = ndb.TextProperty(required=True, indexed=True)

    @staticmethod
    def exists(svg_rep):
        images = Image.query(Image.svg_rep == svg_rep).fetch()
        if len(images) > 0:
            return images[0]
        else:
            return False

    @staticmethod
    def create(svg_rep):
        existing_image = Image.exists(svg_rep=svg_rep)
        if not existing_image:
            image = Image(
                svg_rep=svg_rep
            )
            image.put()
            return image
        else:
            return existing_image

    def _pre_put_hook(self):
        self.class_version = 1


@ae_ndb_serializer
class Overlay(ndb.Model):
    type = ndb.StringProperty(required=True, indexed=True)
    # an overlay is optionally associated with an image
    image_key = ndb.KeyProperty(kind=Image, required=False)

    @staticmethod
    def create_or_get(overlay_type, image_urlsafe_key=None):
        if overlay_type == "LOGO":
            if image_urlsafe_key == None:
                print "raise value error"
                raise ValueError("You must provide an image_key if you are creating an overlay logo")

        # its not an overlay with an image that doesn't have a image_urlsafe_key
        overlay_query = Overlay.query(Overlay.type == overlay_type).fetch()

        if overlay_query:
            overlay = overlay_query[0]


        # this type of overlay has not been created yet
        else:
            if image_urlsafe_key:
                image_key = ndb.Key(urlsafe=image_urlsafe_key).get().key
            else:
                image_key = None

            overlay = Overlay(
                type=overlay_type,
                image_key=image_key
            )

            overlay.put()

        return overlay


@ae_ndb_serializer
class OverlayTemplate(ndb.Model):
    top_left = ndb.KeyProperty(kind=Overlay, required=False)
    top_right = ndb.KeyProperty(kind=Overlay, required=False)
    bottom_left = ndb.KeyProperty(kind=Overlay, required=False)
    bottom_right = ndb.KeyProperty(kind=Overlay, required=False)
    device_key = ndb.KeyProperty(kind=ChromeOsDevice, required=True)

    @staticmethod
    def get_overlay_templates_for_device(device_key):
        query = OverlayTemplate.query(OverlayTemplate.device_key == device_key).fetch()
        return [
            {
                "top_left": query_result.top_left,
                "top_right": query_result.top_right,
                "bottom_left": query_result.bottom_left,
                "bottom_right": query_result.bottom_right
            } for query_result in query
        ]

    @staticmethod
    def create_or_get_by_device_key(device_key):
        existing_template_exists = OverlayTemplate.get_overlay_templates_for_device(device_key)
        if existing_template_exists:
            return existing_template_exists[0]

        else:
            overlay_template = OverlayTemplate(
                device_key=device_key
            )
            overlay_template.put()
            return overlay_template

    # expects a a dictionary with config about overlay
    def set_overlay(self, overlay):
        position = overlay["position"]
        overlay_type = overlay["overlay_type"]
        # expects the front-end to already know the urlsafe_key of a previously posted image
        associated_image_urlsafe_key = overlay["associated_image"]
        overlay = Overlay.create_or_get(overlay_type=overlay_type, image_urlsafe_key=associated_image_urlsafe_key)

        if position == "TOP_LEFT":
            self.top_left = overlay.key
            self.put()

        elif position == "BOTTOM_LEFT":
            self.bottom_left = overlay.key
            self.put()

        elif position == "BOTTOM_RIGHT":
            self.bottom_right = overlay.key
            self.put()

        elif position == "TOP_RIGHT":
            self.top_right = overlay.key
            self.put()
