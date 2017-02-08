import webapp2
import jinja2
import os
import re
from google.appengine.ext import db

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^(?=.*[A-Z])(?=.*[!@#$&%^*()])(?=.*[0-9])(?=.*[a-z]).{7,32}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
								autoescape = True)

def render_str(template, **params):
	t = jinja_env.get_template(template)
	return t.render(params)

def valid_username(username):
	return username and USER_RE.match(username)

def valid_password(password):
	return password and PASS_RE.match(password)

def valid_verification(password, verify):
	return (password == verify)

def valid_email(email):
	return not email or EMAIL_RE.match(email)

class BaseHandler(webapp2.RequestHandler):
	def render(self, template, **kw):
		self.response.out.write(render_str(template, **kw))

	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

class Signup(BaseHandler):

	def get(self):
		self.render("signup-form.html")

	def post(self):
		username = self.request.get("username")
		password = self.request.get("password")
		verify = self.request.get("verify")
		email = self.request.get("email")
		all_valid = True

		params = dict(username = username,
						email = email)

		if not valid_username(username):
			params["username_error"] = "{0} is not a valid username!".format(username)
			all_valid = False

		if not valid_password(password):
			params["password_error"] = "A safe password must contain one lowercase, uppercase, special character and number. It also must be between 7 and 32 characters"
			all_valid = False

		if not valid_verification(password, verify):
			params["verification_error"] = "Your passwords do not match!"
			all_valid = False
		
		if email and not valid_email(email):
			params["email_error"] = "{0} is not a valid email!".format(email)
			all_valid = False

		if all_valid:
			self.render("welcome.html", **params)
		else:
			self.render("signup-form.html", **params)

class Welcome(BaseHandler):

	def get(self):
		username = self.request.get("username")
		if valid_username(username):
			self.render("welcome.html",username)
		else:
			self.redirect("/")

app = webapp2.WSGIApplication([
    ('/', Signup),
    ('/welcome', Welcome)
], debug=True)
