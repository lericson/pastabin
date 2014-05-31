import datetime
import string
import random

from google.appengine.ext import db, deferred
import pygments
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name

touch_minimum_elapsed = datetime.timedelta(days=1)

def _update_accessed(key, accessed):
    pasta = Pasta.get(key)
    pasta.accessed = accessed
    pasta.put()

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
            elapsed = accessed - self.accessed
            if elapsed < touch_minimum_elapsed:
                return False

        deferred.defer(_update_accessed, self.key(), accessed)
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
