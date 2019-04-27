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
from webapp2_extras import jinja2
from Book import Book


class BookHandler(webapp2.RequestHandler):

    def get(self):
        jinja = jinja2.get_jinja2(app=self.app)
        book_id = self.request.get('book_id')
        template_values = {
            'book_id': book_id}

        self.response.write(jinja.render_template("book.html", **template_values))

    def post(self):
        src = self.request.get('src')
        title = self.request.get('title')
        description = self.request.get('description')

        book = Book(src=src, title=title,
                    description=description);

        book.put();

        self.response.write(jinja.render_template("index.html"))


app = webapp2.WSGIApplication(
    [('/book', BookHandler)],
    debug=True)
