from google.appengine.ext import ndb


class Book(ndb.Model):
    src = ndb.BlobProperty(required=True)
    title = ndb.StringProperty(required=True)
    description = ndb.StringProperty(required=True)
    time = ndb.DateTimeProperty(auto_now_add=True)
    user = ndb.StringProperty(required=True)
