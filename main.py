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

import sys
import webapp2
from webapp2_extras import jinja2
from google.appengine.api import images
from Book import Book
from Vote import Vote


class MainHandler(webapp2.RequestHandler):

    def get(self):
        reload(sys)
        sys.setdefaultencoding("utf-8")

        jinja = jinja2.get_jinja2(app=self.app)

        books = Book.query();

        book_list = []

        for book in books:
            votes = Vote.query(Vote.book_id == book.key.id());

            ratings = []
            for vote in votes:
                ratings.append(vote.stars)

            if ratings:
                mean = float(sum(ratings)) / len(ratings)
                stars = round(mean * 2) / 2
            else:
                stars = 0

            book_list.append({
                'id': book.key.id(),
                'src': book.src,
                'title': book.title,
                'stars': stars,
                'num_votes': len(ratings)
            })

        template_values = {'book_cards': book_list}

        self.response.write(jinja.render_template("index.html", **template_values))


app = webapp2.WSGIApplication(
    [('/', MainHandler)],
    debug=True)
