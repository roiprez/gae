from google.appengine.ext import ndb


class Book(ndb.Model):
    src = ndb.StringProperty(required=True)
    title = ndb.StringProperty(required=True)
    description = ndb.StringProperty(required=True)
    time = ndb.DateTimeProperty(auto_now_add=True)
    stars = ndb.FloatProperty(required=True)
    num_votes = ndb.IntegerProperty(required=True)