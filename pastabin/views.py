import uuid
import logging

from werkzeug import Response, redirect
from werkzeug.exceptions import NotFound, MethodNotAllowed
from werkzeug.routing import Rule
from pygments.lexers import guess_lexer
from pygments.lexers import ClassNotFound as LexerNotFound

from pastabin.db import Pasta
from pastabin.utils import JinjaResponse, valid_uuid

class BaseView(object):
    uuid_cookie = "uuid"

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

    def getset_uuid(self):
        """Get or set the UUID for the current client."""
        curr_uuid = self.request.cookies.get(self.uuid_cookie)
        if curr_uuid and valid_uuid(curr_uuid):
            return curr_uuid
        return str(uuid.uuid4())

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
                return self.store_pasta(pasta)
        context = {"errors": errors,
                   "lexer": form.get("lexer"),
                   "code": form.get("code")}
        return JinjaResponse("new_pasta.html", context)

    def store_pasta(self, pasta):
        pasta.uuid = self.getset_uuid()
        pasta.put()
        self.logger.info("created pasta %s", pasta)
        resp = redirect("/p/" + pasta.pasta_id + "/")
        resp.set_cookie(self.uuid_cookie, pasta.uuid)
        return resp

    def get(self):
        return JinjaResponse("new_pasta.html")

class PastaShowView(BaseView):
    allowed_methods = "GET",

    def pasta_from_id(self, pasta_id):
        pasta = Pasta.all().filter("pasta_id =", pasta_id).get()
        if pasta is None:
            raise NotFound(pasta_id)
        pasta.touch()
        return pasta

    def get(self, pasta_id):
        pasta = self.pasta_from_id(pasta_id)
        return JinjaResponse("show_pasta.html", {"pasta": pasta})

class PastaShowTextView(PastaShowView):
    def get(self, pasta_id):
        pasta = self.pasta_from_id(pasta_id)
        return Response(pasta.code, mimetype="text/plain")

class PastaShowAttachmentView(PastaShowView):
    def get(self, pasta_id):
        pasta = self.pasta_from_id(pasta_id)
        lexer = pasta.make_lexer()
        mimetype = lexer.mimetypes[0]
        fname = pasta.pasta_id + lexer.filenames[0][1:]
        headers = [("Content-Disposition", "attachment; filename=" + fname)]
        return Response(pasta.code, mimetype=mimetype, headers=headers)
