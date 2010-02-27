import datetime
import string
import random

from google.appengine.ext import db
import pygments
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name

set_accesed_delta = datetime.timedelta(days=1)

class PastaID(db.StringProperty):
    def default_value(self):
        return "".join(random.sample(string.letters, 6))

class Pasta(db.Model):
    pasta_id = PastaID()
    uuid = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    accessed = db.DateTimeProperty(auto_now_add=True)
    author = db.UserProperty(auto_current_user_add=True)
    author_ip = db.StringProperty()
    lexer = db.StringProperty()
    code = db.TextProperty()
    code_html = db.TextProperty()

    def __str__(self):
        shortened_code = repr(self.code)
        if len(shortened_code) > 13:
            shortened_code = shortened_code[:10] + "..."
        args = (type(self).__name__, self.pasta_id,
                self.author_ip, self.author or "anonymous",
                self.lexer, shortened_code)
        return "<%s %s for %s (%s) in %s (%s)>" % args

    def touch(self, accessed=None):
        """Potentially update self.accessed, depending on how far in the future
        *accessed* is.
        """
        if accessed is None:
            accessed = datetime.datetime.now()

        if self.accessed:
            accessed_delta = accessed - self.accessed
        else:
            accessed_delta = set_accesed_delta * 2

        if accessed_delta >= set_accesed_delta:
            self.accessed = accessed
            self.put()
            return True

    def make_formatter(self):
        return HtmlFormatter(cssclass="source", linenos=True, linenospecial=5)

    def make_lexer(self):
        return get_lexer_by_name(self.lexer)

    def hilight(self, store=True):
        """Hilight the code in *self.code*.

        Returns the generated HTML, and sets self.code_html to that value
        (unless store=False is given).
        """
        formatter = self.make_formatter()
        lexer = self.make_lexer()
        code_rend = pygments.highlight(self.code, lexer, formatter)
        if store:
            self.code_html = code_rend
        return self.code_html

# TODO Potential pasta salad.
