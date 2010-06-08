from google.appengine.ext import db

__all__ = ('GeoCodeCache',)


class GeoCodeCache(db.Model):
    addr = db.StringProperty()
    location = db.GeoPtProperty()

