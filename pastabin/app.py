#!/usr/bin/env python

from os import path
from werkzeug import Request
from werkzeug.exceptions import HTTPException
from werkzeug.routing import Map, Rule
from jinja2 import Environment, FileSystemLoader

from pastabin.views import (PastaCreateView, PastaShowView,
                            PastaShowTextView, PastaShowAttachmentView)
from pastabin.utils import local, local_mgr

url_map = Map([
    PastaCreateView.create_rule("/"),
    PastaShowView.create_rule("/p/<pasta_id>/"),
    PastaShowTextView.create_rule("/p/<pasta_id>/text/"),
    PastaShowAttachmentView.create_rule("/p/<pasta_id>/attachment/"),
])

template_dir = path.join(path.dirname(path.dirname(__file__)), "templates")
jinja_env = Environment(loader=FileSystemLoader(template_dir))

@local_mgr.middleware
def pastabin_app(environ, start_response):
    local.jinja_env = jinja_env
    local.adapter = url_map.bind_to_environ(environ)
    local.request = Request(environ)
    try:
        endpoint, kwds = local.adapter.match()
        response = endpoint(local.request, **kwds)
    except HTTPException, e:
        response = e
    return response(environ, start_response)
