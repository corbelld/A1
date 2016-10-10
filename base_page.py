import webapp2
import os
import jinja2
from google.appengine.ext import ndb
import db_defs

JINJA_ENVIRONMENT = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + '/templates'),
  extensions=['jinja2.ext.autoescape'],
  autoescape=True
  )

class Dynamic(webapp2.RequestHandler):
	template_variables = {}
	
	def __init__(self, request, response):
		self.initialize(request, response)
		self.template_values = {}
		
	def get(self):
		self.template_variables['profile_contents'] = {}
		template = JINJA_ENVIRONMENT.get_template('index.html')
		for i in self.request.arguments():
			self.template_variables['profile_contents'][i] = self.request.get(i)
		self.render('index.html', self.template_variables)
	
	def post(self):
		self.template_variables['profile_contents'] = {}
		template = JINJA_ENVIRONMENT.get_template('index.html')
		for i in self.request.arguments():
			self.template_variables['profile_contents'][i] = self.request.get(i)
			
		action = self.request.get('action')
		if action == 'userin':					
			k = ndb.Key(db_defs.Profile, self.app.config.get('default-group'))
			prof = db_defs.Profile(parent=k)
			prof.userID = self.request.get('userID')
			prof.city = self.request.get('city')
			prof.state = self.request.get('state')
			prof.team = self.request.get('team')
			prof.age = int(self.request.get('age'))
			if self.request.get('agree') == u'on':
				prof.agreement = True
			prof.afavor = [ndb.Key(urlsafe=x) for x in self.request.get_all('afavor[]')]
			prof.put()
			self.template_values['message'] = 'Added profile ' + prof.userID + ' to the database.'
		elif action == 'favorite':
			k = ndb.Key(db_defs.afavor, self.app.config.get('default-group'))
			ai = db_defs.afavor(parent=k)
			ai.name = self.request.get('pokemon')
			ai.put()
			self.template_values['message'] = 'Added favorite Pokemon: ' + ai.name + ' to the database.'
		else:
			self.template_values['message'] = 'Action ' + action + ' is unknown.'
		self.template_values['userID'] = db_defs.Profile.query(ancestor=ndb.Key(db_defs.Profile, self.app.config.get('default-group')))
		self.render('index.html', self.template_variables)
		
	def render(self, page, template_values={}):
		self.template_values['userID'] = [{'userID':x.userID,'key':x.key.urlsafe()} for x in db_defs.Profile.query(ancestor=ndb.Key(db_defs.Profile, self.app.config.get('default-group'))).fetch()]
		self.template_values['city'] = [{'city':x.city,'key':x.key.urlsafe()} for x in db_defs.Profile.query(ancestor=ndb.Key(db_defs.Profile, self.app.config.get('default-group'))).fetch()]
		self.template_values['state'] = [{'state':x.state,'key':x.key.urlsafe()} for x in db_defs.Profile.query(ancestor=ndb.Key(db_defs.Profile, self.app.config.get('default-group'))).fetch()]
		self.template_values['team'] = [{'team':x.team,'key':x.key.urlsafe()} for x in db_defs.Profile.query(ancestor=ndb.Key(db_defs.Profile, self.app.config.get('default-group'))).fetch()]
		self.template_values['age'] = [{'age':x.age,'key':x.key.urlsafe()} for x in db_defs.Profile.query(ancestor=ndb.Key(db_defs.Profile, self.app.config.get('default-group'))).fetch()]
		self.template_values['afavor'] = [{'pokemon':x.pokemon,'key':x.key.urlsafe()} for x in db_defs.Afavor.query(ancestor=ndb.Key(db_defs.Afavor, self.app.config.get('default-group'))).fetch()]

		template = JINJA_ENVIRONMENT.get_template('index.html')
		self.response.write(template.render(self.template_values))
		
# class View(webapp2.RequestHandler):
	# template_variables = {}
	
	# def __init__(self, request, response):
		# self.initialize(request, response)
		# self.template_values = {}
		
	# def get(self):
		# self.template_variables['profile_contents'] = {}
		# template = JINJA_ENVIRONMENT.get_template('view.html')
		# for i in self.request.arguments():
			# self.template_variables['profile_contents'][i] = self.request.get(i)
		# self.render('view.html', self.template_variables)
	
	# def post(self):
		# self.template_variables['profile_contents'] = {}
		# template = JINJA_ENVIRONMENT.get_template('view.html')
		# for i in self.request.arguments():
			# self.template_variables['profile_contents'][i] = self.request.get(i)
		# self.render('view.html', self.template_variables)
		
	# def render(self, page, template_values={}):
		# self.template_values['userID'] = [{'userID':x.userID,'key':x.key.urlsafe()} for x in db_defs.Profile.query(ancestor=ndb.Key(db_defs.Profile, self.app.config.get('default-group'))).fetch()]
		# self.template_values['city'] = [{'city':x.city,'key':x.key.urlsafe()} for x in db_defs.Profile.query(ancestor=ndb.Key(db_defs.Profile, self.app.config.get('default-group'))).fetch()]
		# self.template_values['state'] = [{'state':x.state,'key':x.key.urlsafe()} for x in db_defs.Profile.query(ancestor=ndb.Key(db_defs.Profile, self.app.config.get('default-group'))).fetch()]
		# self.template_values['team'] = [{'team':x.team,'key':x.key.urlsafe()} for x in db_defs.Profile.query(ancestor=ndb.Key(db_defs.Profile, self.app.config.get('default-group'))).fetch()]
		# self.template_values['age'] = [{'age':x.age,'key':x.key.urlsafe()} for x in db_defs.Profile.query(ancestor=ndb.Key(db_defs.Profile, self.app.config.get('default-group'))).fetch()]
		# self.template_values['afavor'] = [{'name':x.name,'key':x.key.urlsafe()} for x in db_defs.afavor.query(ancestor=ndb.Key(db_defs.afavor, self.app.config.get('default-group'))).fetch()]

		# template = JINJA_ENVIRONMENT.get_template('view.html')
		# self.response.write(template.render(self.template_values))
