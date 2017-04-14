#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import re
import logging




# html boilerplate for the top of every page
page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>Signup</title>
</head>
<body>
    <h1>Signup</h1>
"""

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""

form = """
<form action="/" method="post">
    <table>
        <tr><td>Username</td>
            <td><input type="text" name="username" value="%(username)s"></td>
            <td style="color: red">%(user_error)s</td>
        </tr>
        <tr>
            <td>Password</td>
            <td><input type="password" name="password"value=""></td>
            <td style="color: red">%(pass_error)s</td>
        </tr>
        <tr>
            <td>Verify Password</td>
            <td><input type="password" name="verify" value=""></td>
            <td style="color: red">%(verify_error)s</td>
        </tr>
        <tr>
            <td>Email (optional)</td>
            <td><input type="text" name="email" value="%(email)s"></td>
            <td style="color: red">%(email_error)s</td>
        </tr>
    </table>
    <input type="submit" value="Submit">
</form>
"""
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    logging.info(username)
    logging.info(USER_RE.search(username))
    return username and USER_RE.search(username)

PASS_RE  = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE = re.compile("^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
    return not email or EMAIL_RE.match(email)


class Signup(webapp2.RequestHandler):
    """ Handles requests coming in to '/' (the root of our site)
        e.g. www.user-signup.com/
    """

    def write_form(self, username="", user_error="", pass_error="",
                   verify_error="", email_error="", email=""):
        self.response.out.write(page_header +
        form % {"username": username,
                "user_error": user_error,
                "pass_error": pass_error,
                "verify_error": verify_error,
                "email": email,
                "email_error": email_error}
        + page_footer)
        #self.response.write(page_header + form + page_footer)

    def get(self):
        #form = page_header + form + page_footer
        self.write_form()

    def post(self):
        found_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        logging.info(username)
        logging.info(password)
        logging.info(verify)
        logging.info(email)

        logging.info(found_error)
        #password = valid_password(u_password)
        #verify = valid_verify(u_verify)
        #email = valid_email(u_email)

        user_error = ""
        pass_error = ""
        verify_error = ""
        email_error = ""

        if not valid_username(username):
            user_error = "Invalid username"
            found_error = True

        if not valid_password(password):
            pass_error = "Invalid password"
            found_error = True
        elif password != verify:
            verify_error = "passwords don't match"
            found_error = True


        if not valid_email(email):
            email_error = "Invalid email"
            found_error = True

        if found_error:
            #self.response.out.write(form)
            #self.redirect('/')
            self.response.out.write(page_header +
            form % {"username": username,
                    "user_error": user_error,
                    "pass_error": pass_error,
                    "verify_error": verify_error,
                    "email": email,
                    "email_error": email_error}
            + page_footer)
        else:
            self.redirect('/welcome?username=' + username)

        #form = page_header + form + page_footer
        #self.write_form()

class Welcome(webapp2.RequestHandler):
    """ Handles requests coming in to '/welcome'
        e.g. www.user-signup.com/welcome
    """

    def get(self):
        # look inside the request to figure out what the user typed
        username = self.request.get("username")
        self.response.out.write("Welcome " + username)



        #user_name = cgi.escape(user_name, quote=True)

        # build response content
        #sentence = "<strong>Welcome, " + user_name + "</strong>"

        #content = page_header + "<p>" + sentence + "</p>" + page_footer
        #self.response.write(content)

app = webapp2.WSGIApplication([
    ('/', Signup),
    ('/welcome', Welcome)
], debug=True)
