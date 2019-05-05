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

import time
import webapp2
from google.appengine.api import users
from webapp2_extras import jinja2
from Vote import Vote
from main import MainHandler


class VoteHandler(webapp2.RequestHandler):

    def get(self):
        user = users.get_current_user()
        if user == None:
            self.redirect("/")

        else:
            jinja = jinja2.get_jinja2(app=self.app)
            book_id = int(self.request.get('book_id'))
            votes = Vote.query(Vote.book_id == book_id);

            vote_list = []

            for vote in votes:
                vote_list.append({
                    'comment': vote.comment,
                    'stars': vote.stars,
                    'user': vote.user
                })

            template_values = {'votes': vote_list}

            self.response.write(jinja.render_template("book.html", **template_values))

    def post(self):
        user = users.get_current_user()

        if user:

            book_id = int(self.request.get('book_id'))

            if self.request.get('deleting'):
                votes = Vote.query(Vote.book_id == book_id and Vote.user == user.email());

                for vote in votes:
                    vote.key.delete()

            else:
                stars = int(self.request.get('stars'))
                comment = self.request.get('comment')

                votes = Vote.query(Vote.book_id == book_id and Vote.user == user.email());

                for vote in votes:
                    vote.key.delete()

                vote = Vote(book_id=book_id, stars=stars,
                            comment=comment, user=user.email());

                vote.put();

            # Para darle tiempo al recargar a que coja el nuevo comentario
            time.sleep(1)

            self.redirect('/book?book_id={}'.format(book_id))

        else:
            greeting = str.format(
                "<a href=\"{0}\">Sign in or register</a>.",
                users.create_login_url('/'))

            self.response.out.write(
                str.format("<html><body>{0}</body></html>", greeting))


app = webapp2.WSGIApplication(
    [('/', MainHandler), ('/vote', VoteHandler)],
    debug=True)
