from google.appengine.ext import ndb


class Vote(ndb.Model):
    book_id = ndb.IntegerProperty(required=True)
    comment = ndb.StringProperty(required=False)
    stars = ndb.IntegerProperty(required=True)