import cherrypy

import spica

class Doc:

    @cherrypy.expose
    def index(self):
        hmi = 1
        kw_args = spica.get_template_args(header_menu_index=hmi)
        template_f = '%s.html' % (spica.header_menu[hmi][0])
        return spica.get_template(template_f, **kw_args)
