#!/usr/bin/env python

from os import path
from werkzeug import Request
from werkzeug.exceptions import HTTPException
from werkzeug.routing import Map, Rule
from jinja2 import Environment, FileSystemLoader

from pastabin import views
from pastabin.utils import local, local_mgr

def R(view, url): return view.create_rule(url)

url_map = Map([
    R(views.PastaCreateView, "/"),
    R(views.PastaShowView, "/p/<pasta_id>/"),
    R(views.PastaShowTextView, "/p/<pasta_id>/text/"),
    R(views.PastaShowAttachmentView, "/p/<pasta_id>/attachment/"),
    R(views.PastaDeleteView, "/p/<pasta_id>/delete/"),
])

template_dir = path.join(path.dirname(path.dirname(__file__)), "templates")
jinja_env = Environment(loader=FileSystemLoader(template_dir))

@local_mgr.middleware
def pastabin_app(environ, start_response):
    local.jinja_env = jinja_env
    local.adapter = url_map.bind_to_environ(environ)
    local.reverse = local.adapter.build
    local.request = Request(environ)
    try:
        endpoint, kwds = local.adapter.match()
        response = endpoint(local.request, **kwds)
    except HTTPException, e:
        response = e
    return response(environ, start_response)
