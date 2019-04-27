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
from Vote import Vote


class VoteHandler(webapp2.RequestHandler):

    def get(self):
        jinja = jinja2.get_jinja2(app=self.app)
        book_id = self.request.get('book_id')
        votes = Vote.query(Vote.book_id == book_id);

        vote_list = []

        for vote in votes:
            vote_list.append({
                'comment': vote.comment,
                'stars': vote.stars
            })

        template_values = {'votes': vote_list}

        self.response.write(jinja.render_template("book.html", **template_values))

    def post(self):
        jinja = jinja2.get_jinja2(app=self.app)

        book_id = int(self.request.get('book_id'))
        stars = int(self.request.get('stars'))
        comment = self.request.get('comment')
        print("comment" + comment)

        vote = Vote(book_id=book_id, stars=stars,
                    comment=comment);

        vote.put();

        self.response.write(jinja.render_template("index.html"))


app = webapp2.WSGIApplication(
    [('/vote', VoteHandler)],
    debug=True)
