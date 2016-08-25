import webapp2
import re
import cgi

page_header="""
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
    <h1>Signup Page</h1>
"""
signupform="""
        <form method="post">
            <table>
                <tr>
                    <td><label for="username">Username</label></td>
                    <td>
                        <input name="username" type="text" value="%(u)s">
                        <span class="error">%(er1)s</span>
                    </td>
                </tr>
                <tr>
                    <td><label for="password">Password</label></td>
                    <td>
                        <input name="password" type="password" value="">
                        <span class="error">%(er2)s</span>
                    </td>
                </tr>
                <tr>
                    <td><label for="verify">Verify Password</label></td>
                    <td>
                        <input name="verify" type="password" value="">
                        <span class="error">%(er3)s</span>
                    </td>
                </tr>
                <tr>
                    <td><label for="email">Email (optional)</label></td>
                    <td>
                        <input name="email" type="email" value="%(e)s">
                        <span class="error">%(er4)s</span>
                    </td>
                </tr>
            </table>
            <input type="submit">
        </form>
"""
page_footer="""
    </body>
</html>
"""

def escape_html(s):
    return cgi.escape(s, quote = True)

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PW_RE = re.compile(r"^.{3,20}$")
EM_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

def valid_username(username):
    return username and USER_RE.match(username)

def valid_password(password):
    return password and PW_RE.match(password)

def valid_verify(verify):
    return verify and PW_RE.match(verify)

def valid_email(email):
    return email and EM_RE.match(email)

error1 = "That's not a valid username"
error2 = "That not a valid password"
error3 = "Your passwords didn't match"
error4 = "That's not a valid email"

class MainHandler(webapp2.RequestHandler):

    def write_form(self, u="", e="", er1="", er2="", er3="", er4=""):
        self.response.out.write(page_header + signupform %{"u": escape_html(u),
                                             "e": escape_html(e),
                                             "er1": er1,
                                             "er2": er2,
                                             "er3": er3,
                                             "er4": er4} + page_footer)

    def get(self):
        self.write_form()

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')
        nameError, pwError, emailError, verifyError = False, False, False, False
        er1, er2, er3, er4 = "", "", "", ""

        if not valid_username(username):
            nameError = True
        if not valid_password(password):
            pwError = True
        if not valid_email(email) and email:
            emailError = True
        if not valid_verify(verify):
            verifyError = True

        if password == verify:
            pwMatch = True
        else:
            pwMatch = False

        if (not nameError and not pwError and not emailError and not verifyError) and pwMatch:
            self.redirect('/welcome?username=' + username)
        else:
            if nameError:
                er1 = error1
            if pwError:
                er2 = error2
            if not pwMatch:
                er3 = error3
            if emailError:
                er4 = error4

        self.write_form(username, email, er1, er2, er3, er4)

class Welcome(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')
        if valid_username(username):
            self.response.out.write('Great to see you, %s' %username)
        else:
            self.redirect('/')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', Welcome)
], debug=True)
