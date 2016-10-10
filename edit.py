import webapp2
import os
import jinja2
import base_page
from google.appengine.ext import ndb
import db_defs

JINJA_ENVIRONMENT = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + '/templates'),
  extensions=['jinja2.ext.autoescape'],
  autoescape=True
  )
  
class Edit(base_page.DynamicPage):
	def __init__(self, request, response):
		self.initialize(request, response)
		self.template_values = {}

	def get(self):
		if self.request.get('type') == 'profile':
			profile_key = ndb.Key(urlsafe=self.request.get('key'))
			profile = profile_key.get()
			allProfiles = db_defs.Profile.query(ancestor=ndb.Key(db_defs.Profile, self.app.config.get('default-group')))
			profiles_boxes = []
			for element in allProfiles:
				profiles_boxes.append({'userID':element.userID,'city':element.city,'state':element.state,'team':element.team,'age':element.age})
				
			self.template_values['profiles'] = profiles_boxes
		self.render('edit.html',self.template_values)
	
	def render(self, page, template_values={}):
		self.template_values['userID'] = [{'userID':x.userID,'key':x.key.urlsafe()} for x in db_defs.Profile.query(ancestor=ndb.Key(db_defs.Profile, self.app.config.get('default-group'))).fetch()]
		self.template_values['city'] = [{'city':x.city,'key':x.key.urlsafe()} for x in db_defs.Profile.query(ancestor=ndb.Key(db_defs.Profile, self.app.config.get('default-group'))).fetch()]
		self.template_values['state'] = [{'state':x.state,'key':x.key.urlsafe()} for x in db_defs.Profile.query(ancestor=ndb.Key(db_defs.Profile, self.app.config.get('default-group'))).fetch()]
		self.template_values['team'] = [{'team':x.team,'key':x.key.urlsafe()} for x in db_defs.Profile.query(ancestor=ndb.Key(db_defs.Profile, self.app.config.get('default-group'))).fetch()]
		self.template_values['age'] = [{'age':x.age,'key':x.key.urlsafe()} for x in db_defs.Profile.query(ancestor=ndb.Key(db_defs.Profile, self.app.config.get('default-group'))).fetch()]

		template = JINJA_ENVIRONMENT.get_template('edit.html')
		self.response.write(template.render(self.template_values))