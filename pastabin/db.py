import string
import random

from google.appengine.ext import db
import pygments
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name

class PastaID(db.StringProperty):
    def default_value(self):
        return "".join(random.sample(string.letters, 6))

class Pasta(db.Model):
    pasta_id = PastaID()
    created = db.DateTimeProperty(auto_now_add=True)
    author = db.UserProperty(auto_current_user_add=True)
    author_ip = db.StringProperty()
    lexer = db.StringProperty()
    code = db.TextProperty()
    code_html = db.TextProperty()

    def __str__(self):
        shortened_code = repr(self.code)
        if len(shortened_code) > 13:
            shortened_code = shortened_code[:10] + "..."
        args = (self.__class__.__name__, self.pasta_id,
                self.author_ip, self.author or "anonymous",
                self.lexer, shortened_code)
        return "<%s %s for %s (%s) in %s (%s)>" % args

    def make_formatter(self):
        return HtmlFormatter(cssclass="source", linenospecial=5)

    def hilight(self, store=True):
        """Hilight the code in *self.code*.

        Returns the generated HTML, and sets self.code_html to that value
        (unless store=False is given).
        """
        formatter = self.make_formatter()
        lexer = get_lexer_by_name(self.lexer)
        self.code_html = pygments.highlight(self.code, lexer, formatter)
        return self.code_html

# TODO Potential pasta salad.
