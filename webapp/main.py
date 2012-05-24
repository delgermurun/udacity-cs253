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
# avfpdempuvmbymfr
from os import path
import webapp2
import cgi
import jinja2
import re

template_dir =  path.join(path.dirname(__file__), 'templates')
jenv = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)


def render_str(template, **params):
    t = jenv.get_template(template)
    return t.render(params)

form = """
<form method="POST">
    <label> Enter text:<br> 
        <textarea name="text">%(text)s</textarea>
    </labe><br>
    <input type="submit" value="Submit"/>
</form>
"""


class BaseHandler(webapp2.RequestHandler):
    def render(self, template, **params):
        self.response.out.write(render_str(template, **params))

    def write(self, text):
        self.response.out.write(text)


class SignUpHandler(BaseHandler):
    def get(self):
        value = error = {}
        return self.render('signup.html', value=value, error=error)
    
    def is_valid(self):
        get = self.request.get
        data = {'username': get('username'),
                'email'   : get('email')}
        password = get('password')
        verify = get('verify')
        error = {}

        USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,9}$")
        if not USER_RE.match(data['username']):
            error['username'] = 'Not valid username'

        PASS_RE = re.compile(r"^.{3,20}$")
        if not PASS_RE.match(password):
            error['password'] = 'Not valid password'
        elif password != verify:
            error['verify'] = 'Password don"t match.'

        EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
        if not EMAIL_RE.match(data['email']):
            error['email'] = 'Not valid email'
        return data, error

    def post(self):
        data, error = self.is_valid()
        if error:
            return self.render('signup.html', value=data, error=error)
        else:
            self.redirect('/unit2/signup/welcome?username=%s' % data['username'])



class WelcomeHandler(BaseHandler):
    def get(self):
        self.response.out.write('Welcome, %s' % self.request.get('username', ''))


class Rot13Handler(BaseHandler):
    def get(self):
        self.response.out.write(form % {'text': ''})

    def post(self):
        text = self.request.get('text')
        out_text = ''
        for ch in text:
            o = ord(ch)
            if 64 < o < 91:
                o = o + 13
                o = 65 * (o / 91) + o % 91
                out_text += chr(o)
            elif 96 < o < 123:
                o = o + 13
                o = 97 * (o / 123) + o % 123
                out_text += chr(o)
            else:
                out_text += ch

        self.response.out.write(form % {'text': cgi.escape(out_text)})


class MainHandler(BaseHandler):
    def get(self):
        self.response.out.write(form)

    def post(self):
        self.response.out.write(', Udacity!')

app = webapp2.WSGIApplication([
    ('/', MainHandler), 
    ('/unit2/rot13', Rot13Handler),
    ('/unit2/signup', SignUpHandler),
    ('/unit2/signup/welcome', WelcomeHandler),
], debug=True)
