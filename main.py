import webapp2
import cgi
import re

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")

def valid_username(username):
	return USER_RE.match(username)

def valid_password(password):
	return PASS_RE.match(password)

def valid_email(email):
	return EMAIL_RE.match(email)

header = """
	<!DOCTYPE html>
	<html>
	    <head>
	        <style>
	            .error {
	                color: red;
	            }
	        </style>
	    </head>
	    <body>
	    	<h1>Signup</h1>
"""

footer = """
		</body>
	</html>
"""

full_form ="""
	        <form method="post">
	            <table>
	                <tr>
	                    <td><label for="username">Username</label></td>
	                    <td>
	                        <input name="username" type="text" value="{4}" required>
	                        <span class="error">{0}</span>
	                    </td>
	                </tr>
	                <tr>
	                    <td><label for="password">Password</label></td>
	                    <td>
	                        <input name="password" type="password" required>
	                        <span class="error">{1}</span>
	                    </td>
	                </tr>
	                <tr>
	                    <td><label for="verify">Verify Password</label></td>
	                    <td>
	                        <input name="verify" type="password" required>
	                        <span class="error">{2}</span>
	                    </td>
	                </tr>
	                <tr>
	                    <td><label for="email">Email (optional)</label></td>
	                    <td>
	                        <input name="email" type="email" value="{5}">
	                        <span class="error">{3}</span>
	                    </td>
	                </tr>
	            </table>
	            <input type="submit">
	        </form>
	        """

class Index(webapp2.RequestHandler):

	def write_form(self, username_error="", password_error="", verification_error="", email_error="", username="", email=""):
		content = header + full_form.format(username_error, password_error, verification_error, email_error, username, email) + footer
		self.response.out.write(content)

	def get(self):
		self.write_form()

	def post(self):
		username = self.request.get("username")
		password = self.request.get("password")
		verify = self.request.get("verify")
		email = self.request.get("email")

		username_validate = valid_username(username)
		password_validate = valid_password(password)
		verify_validate = password == verify
		email_validate = valid_email(email)

		username_error = ""
		password_error = ""
		verification_error = ""
		email_error = ""

		if username_validate and password_validate and verify_validate and ((not email) or (email and email_validate)):
			self.redirect("/add?username=" + username)

		if not username_validate:
			username_error = "{0} is not a valid username!".format(cgi.escape(username, quote=True))

		if not password_validate:
			password_error = "Not a valid password!"

		if not verify_validate:
			verification_error = "Your passwords do not match!"
		
		if email and not email_validate:
			email_error = "{0} is not a valid email!".format(cgi.escape(email, quote=True))

		self.write_form(username_error, password_error, verification_error, email_error, username, email)

class AddUser(webapp2.RequestHandler):

	def get(self):
		username = self.request.get("username")
		self.response.out.write("Welcome, {0}!".format(username))

app = webapp2.WSGIApplication([
    ('/', Index),
    ('/add', AddUser)
], debug=True)
