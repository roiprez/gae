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
from webapp2_extras import jinja2
from google.appengine.api import images, users
from google.appengine.ext import ndb
from Book import Book
from Vote import Vote


class BookHandler(webapp2.RequestHandler):

    def get(self):
        user = users.get_current_user()
        if user:
            jinja = jinja2.get_jinja2(app=self.app)
            book_id = self.request.get('book_id')

            book_key = ndb.Key(Book, int(book_id))

            book = book_key.get()

            votes = Vote.query(Vote.book_id == book.key.id());

            ratings = []
            for vote in votes:
                ratings.append(vote.stars)

            if ratings:
                mean = sum(ratings) / len(ratings)
                stars = round(mean * 2) / 2
            else:
                stars = 0

            template_values = {
                'book': {
                    'id': book_id,
                    'src': book.src,
                    'title': book.title,
                    'description': book.description,
                    'votes': votes
                },
                'users': users}

            self.response.write(jinja.render_template("book.html", **template_values))

        else:
            greeting = str.format(
                "<a href=\"{0}\">Sign in or register</a>.",
                users.create_login_url('/'))

            self.response.out.write(
                str.format("<html><body>{0}</body></html>", greeting))

    def post(self):
        jinja = jinja2.get_jinja2(app=self.app)

        user = users.get_current_user()

        if user:
            if self.request.get('title'):
                src = self.request.get('src')
                title = self.request.get('title')
                description = self.request.get('description')

                book = Book(title=title,
                            description=description, user=user.email());

                book.src = images.resize(src, 120, 240)

                book.put();

                # Para darle tiempo al recargar de que coja el nuevo libro
                time.sleep(1)

                self.redirect('/')
            else:
                template_values = {'users': users}
                self.response.write(jinja.render_template("add_book.html", **template_values))

        else:
            greeting = str.format(
                "<a href=\"{0}\">Sign in or register</a>.",
                users.create_login_url('/'))

            self.response.out.write(
                str.format("<html><body>{0}</body></html>", greeting))


app = webapp2.WSGIApplication(
    [('/book', BookHandler)],
    debug=True)
