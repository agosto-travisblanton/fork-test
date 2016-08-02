from google.appengine.ext import ndb

from restler.decorators import ae_ndb_serializer


@ae_ndb_serializer
class Image(ndb.Model):
    base64rep = ndb.TextProperty(required=True, indexed=False)

    @staticmethod
    def exists(base64rep):
        images = Image.query(Image.base64rep == base64rep).fetch()
        if len(images) > 0:
            return images[0]
        else:
            return False

    @staticmethod
    def create(base64rep):
        existing_image = Image.exists(base64rep=base64rep)
        if not existing_image:
            image = Image(
                base64rep=base64rep
            )
            image.put()
            return image
        else:
            return existing_image

    def _pre_put_hook(self):
        self.class_version = 1
