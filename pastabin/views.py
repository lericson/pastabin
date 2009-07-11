import logging

from werkzeug.utils import redirect
from werkzeug.exceptions import MethodNotAllowed
from werkzeug.routing import Rule
from pygments.lexers import guess_lexer
from pygments.lexers import ClassNotFound as LexerNotFound

from pastabin.db import Pasta
from pastabin.utils import local, JinjaResponse

class BaseView(object):
    def __new__(cls, request, *args, **kwds):
        self = super(BaseView, cls).__new__(cls, request)
        self.__init__(request)
        view_meth = getattr(self, request.method.lower())
        if view_meth:
            return view_meth(*args, **kwds)
        else:
            raise MethodNotAllowed(getattr(self, "allowed_methods", None))

    def __init__(self, request):
        self.request = request

    @classmethod
    def create_rule(cls, *args, **kwds):
        allowed_methods = getattr(cls, "allowed_methods", None)
        kwds.setdefault("endpoint", cls)
        kwds.setdefault("methods", allowed_methods)
        return Rule(*args, **kwds)

class PastaCreateView(BaseView):
    allowed_methods = "GET", "POST"
    logger = logging.getLogger("pastabin.views.create")

    def post(self):
        form = self.request.form
        lexer = form.get("lexer", "guess")
        code = form.get("code")
        errors = []
        error = lambda *a: errors.append(a)
        if not lexer:
            error("missing-lexer", "No lexer name given.")
        if not code:
            error("missing-code", "No code given.")
        if lexer == "guess":
            try:
                lexer = guess_lexer(code)
            except LexerNotFound, e:
                error("lexer-not-found", e.args[0])
        if not errors:
            pasta = Pasta(author_ip=self.request.remote_addr,
                          lexer=lexer, code=code)
            try:
                pasta.hilight()
            except LexerNotFound, e:
                error("lexer-not-found", e.args[0])
            else:
                self.logger.info("created pasta %s", pasta)
                pasta.put()
                return redirect("/p/" + pasta.pasta_id + "/")
        context = {"errors": errors,
                   "lexer": form.get("lexer"),
                   "code": form.get("code")}
        return JinjaResponse("new_pasta.html", context)

    def get(self):
        return JinjaResponse("new_pasta.html")

class PastaShowView(BaseView):
    allowed_methods = "GET",

    def get(self, pasta_id):
        pasta = Pasta.all().filter("pasta_id =", pasta_id).get()
        return JinjaResponse("show_pasta.html", {"pasta": pasta})
