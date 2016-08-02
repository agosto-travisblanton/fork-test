from google.appengine.ext import ndb

from restler.decorators import ae_ndb_serializer


@ae_ndb_serializer
class Image(ndb.Model):
    svg_rep = ndb.TextProperty(required=True, indexed=False)

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
