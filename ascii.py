import os
import webapp2
import cgi
import jinja2
from google.appengine.api import users
from google.appengine.ext import db
import time 

template_dir = os.path.join(os.path.dirname(__file__))
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),autoescape = True)


class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template,**kw):
		self.write(self.render_str(template, **kw))

class Art(db.Model):
	title = db.StringProperty(required = True)
	art = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)


class MainPage(Handler):
	def render_front(self, title ="", art ="", error=""): #function used to display data on the webpage
		
		arts = db.GqlQuery("SELECT * from Art ORDER BY created DESC") # gql command used to fetch data from the database
		self.render("front.html", title=title, art=art, error=error, arts = arts) #calls function to print data with resp parame


	def get(self):
		
		self.render_front()

	def post(self):
		title = self.request.get("title")
		art = self.request.get("art")
		delete = self.request.get("delete")

		if delete:
			identity = self.request.get('id')
			key = db.Key.from_path('Art',int(identity))
			post = db.get(key)
			db.delete(post)
			time.sleep(0.5)
			self.redirect('/')
					
		if title and art:
			a = Art(title = title, art = art)
			a.put()		
			time.sleep(0.5)
			self.redirect('/')
		
		else:
			if title:
				error = "Ooops..Not again, u missed the art"
				self.render_front(title, art, error)

			elif art:
				error = "What about the title??"
				self.render_front(title, art, error)


			else:
				error = "We need both the title and the art"
				self.render_front(title, art, error)


application = webapp2.WSGIApplication([('/',MainPage),
], debug=True)
