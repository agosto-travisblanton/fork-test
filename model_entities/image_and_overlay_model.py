from google.appengine.ext import ndb

from restler.decorators import ae_ndb_serializer
from chrome_os_device_model import ChromeOsDevice

overlay_positions = ["TOP_LEFT", "BOTTOM_LEFT", "BOTTOM_RIGHT", "TOP_RIGHT"]
overlay_types = ["TIME", "DATE", "DATETIME", "LOGO"]


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
    position = ndb.StringProperty(required=True, indexed=True)
    type = ndb.StringProperty(required=True, indexed=True)
    # an overlay is optionally associated with an image
    image_key = ndb.KeyProperty(kind=Image, required=False)

    @staticmethod
    def create(overlay_position, overlay_type, image_key=None):
        if (overlay_position in overlay_positions) and (overlay_type in overlay_types):
            if overlay_type == "LOGO":
                if image_key == None:
                    raise ValueError("You must provide an image_key if you are creating an overlay logo")

            overlay = Overlay(
                position=overlay_position,
                type=overlay_type,
                image_key=image_key
            )
            overlay.put()
            return overlay

        else:
            raise ValueError("Unexpected overlay_position or overlay_type")


@ae_ndb_serializer
class DeviceOverlayAssociation(ndb.Model):
    device_key = ndb.KeyProperty(kind=ChromeOsDevice, required=True)
    overlay_key = ndb.KeyProperty(kind=Overlay, required=True)

    @staticmethod
    def create_association(device_key, overlay_key):
        association = DeviceOverlayAssociation(
            device_key=device_key,
            overlay_key=overlay_key
        )

        association.put()
        return association

    @staticmethod
    def overlays_with_device_key(device_key):
        return [
            entity.overlay_key.get()
            for entity in
            DeviceOverlayAssociation.query(DeviceOverlayAssociation.device_key == device_key).fetch()
            ]
