from werkzeug import LocalManager, Local, Response

local = Local()
local_mgr = LocalManager([local])

class JinjaResponse(Response):
    default_mimetype = "text/html"

    def __init__(self, template_name, context={}, **kwds):
        tmpl = local.jinja_env.get_template(template_name)
        data = tmpl.render(context)
        super(JinjaResponse, self).__init__(data, **kwds)
        self.template_name = template_name
        self.context = context
