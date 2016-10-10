import webapp2

config = {'default-group':'base-data'}

application = webapp2.WSGIApplication([
  ('/edit', 'edit.Edit'),
  ('/view.html', 'base_page.View'),
  ('/', 'base_page.Dynamic'),
], debug=True, config=config)
