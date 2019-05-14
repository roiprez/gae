import sys
import webapp2
from webapp2_extras import jinja2
from google.appengine.api import users
from models.Book import Book
from models.Vote import Vote


class MainHandler(webapp2.RequestHandler):

    def get(self):
        reload(sys)
        sys.setdefaultencoding("utf-8")

        jinja = jinja2.get_jinja2(app=self.app)

        filtered = False

        if self.request.get('category') or self.request.get('text_filter'):
            filtered = True
        else:
            filtered = False

        if self.request.get('category'):
            books = Book.query(Book.category == self.request.get('category'))
        else:
            books = Book.query()

        text_filter = self.request.get('text_filter')

        book_list = []

        for book in books:
            if text_filter.lower() in book.title.lower():
                votes = Vote.query(Vote.book_id == book.key.id())

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
                    'user': book.user,
                    'num_votes': len(ratings)
                })

        template_values = {'book_cards': book_list, 'users': users, 'filtered': filtered,
                           'category_filter': self.request.get('category'),
                           'text_filter': self.request.get('text_filter')}

        self.response.write(jinja.render_template("index.html", **template_values))
