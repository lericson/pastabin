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

def valid_uuid(v):
    """Validate that *v* is a UUID.

    >>> valid_uuid("d058177e-7700-4bb9-98fc-1b772d9dd012")
    True
    >>> valid_uuid("d058177e-HELLO-WORLD!!!-1b772d9dd012")
    False
    """
    parts = v.split("-", 4)
    if any(c not in "0123456789abcdef" for p in parts for c in p):
        return False
    elif map(len, parts) != [8, 4, 4, 4, 12]:
        return False
    return True

if __name__ == "__main__":
    import doctest
    doctest.testmod()
