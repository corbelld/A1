from google.appengine.ext import ndb

class Message(ndb.Model):
	message = ndb.StringProperty(required=True)

class Profile(ndb.Model):
	userID = ndb.StringProperty(required=True)
	city = ndb.StringProperty(required=True)
	state = ndb.StringProperty(required=True)
	team = ndb.StringProperty(required=True)
	age = ndb.IntegerProperty(required=True)
	agree = ndb.BooleanProperty(default=False)

class Afavor(ndb.Model):
	pokemon = ndb.StringProperty(required=True)
	favorite = ndb.StringProperty(repeated=True)