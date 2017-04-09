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


class Index(webapp2.RequestHandler):
    """ Handles requests coming in to '/' (the root of our site)
        e.g. www.user-signup.com/
    """

    def get(self):
        form = """
        <form action="/welcome" method="get">
            <table>
                <tr><td>Username</td><td><input type="text" name="username"/></td></tr>
                <tr><td>Password</td><td><input type="text" name="password"/></td></tr>
                <tr><td>Verify Password</td><td><input type="text" name="verify"/></td></tr>
                <tr><td>Email (optional)</td><td><input type="text" name="email"/></td></tr>
            </table>
            <input type="submit" value="Submit"/>
        </form>
        """

        content = page_header + form + page_footer
        self.response.write(content)

class Welcome(webapp2.RequestHandler):
    """ Handles requests coming in to '/welcome'
        e.g. www.user-signup.com/welcome
    """

    def get(self):
        # look inside the request to figure out what the user typed
        user_name = self.request.get("username")

        user_name = cgi.escape(user_name, quote=True)

        # build response content
        sentence = "<strong>Welcome, " + user_name + "</strong>"

        content = page_header + "<p>" + sentence + "</p>" + page_footer
        self.response.write(content)

app = webapp2.WSGIApplication([
    ('/', Index),
    ('/welcome', Welcome)
], debug=True)
