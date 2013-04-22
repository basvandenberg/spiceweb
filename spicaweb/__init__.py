import os
import ConfigParser
import cherrypy
from mako.lookup import TemplateLookup

from cherrypy_auth import auth
from spica import project_management
#from spica import job_management

import project
import feature
import classification
#import news

###############################################################################
# Paths
###############################################################################

# path to spicaweb module
spicaweb_dir = os.path.dirname(os.path.abspath(__file__))

# path to template directories
tmpl_d = os.path.join(spicaweb_dir, 'templates')
auth_tmpl_d = os.path.join(os.path.dirname(os.path.abspath(auth.__file__)),
                           'template/mako')

# config file name
CONFIG_FILE = 'spicaweb.cfg'

# read root url from config
config = ConfigParser.ConfigParser()
config.read(CONFIG_FILE)
ROOT_URL = config.get('spicaweb', 'root_url')

###############################################################################
# Authentication decorator
###############################################################################

def authenticate():
    '''
    Authentication decorator, redirect to login if user is not logged in.
    '''
    user = cherrypy.session.get(auth.Auth.SESSION_USER_KEY, None)
    if(user is None):
        raise cherrypy.HTTPRedirect('%slogin' % (ROOT_URL))

# add the authentication decorator as a tool
cherrypy.tools.authenticate = cherrypy.Tool('before_handler', authenticate)

###############################################################################
# Menus
###############################################################################

# menu items
main_menu = [('home', ''),
    ('projects', 'app/projects'),
    ('features', 'app/features'),
    ('classification', 'app/classification')
]

# sub menu items
sub_menus = [
    [],
    ['list', 'new', 'details'],
    ['list', 'ttest', 'histogram', 'scatter', 'heatmap'],
    ['list', 'new', 'details']
]

# static menu items
header_menu = [
        ('news', 'news/'),
        ('documentation', 'doc/'),
        ('software', 'software/'),
        ('about', 'about/'),
        ('contact', 'contact/')]

###############################################################################
# Temlpate functions
###############################################################################

# create global template lookup object
tmpl_dirs = [tmpl_d, auth_tmpl_d]
mylookup = TemplateLookup(directories=tmpl_dirs, module_directory='/tmp/mako/')


def get_template(name, **kwargs):
    t = mylookup.get_template(name)
    return t.render(**kwargs)


def get_template_args(main_menu_index=0, sub_menu_index=-1,
        header_menu_index=-1):
    '''
    Returns a dict with default template parameters.
    '''

    # retrieve user id from session data
    if(hasattr(cherrypy, 'session')):
        user_id = cherrypy.session.get(auth.Auth.SESSION_USER_KEY, None)
    else:
        user_id = None

    # retrieve project id from cookie
    if(hasattr(cherrypy, 'session')):
        project_id = cherrypy.session.get(project.Project.SESSION_PROJECT_KEY,
                None)
    else:
        project_id = None

    return {'user_id': user_id,
            'project_id': project_id,
            'header_menu': header_menu,
            'header_menu_index': header_menu_index,
            'main_menu': main_menu,
            'main_menu_index': main_menu_index,
            'sub_menu': sub_menus[main_menu_index],
            'sub_menu_index': sub_menu_index,
            'root_url': ROOT_URL,
            'show_filter': False}


###############################################################################
# The Root class
###############################################################################


class Root:

    def __init__(self):

        # read spicaweb config file
        config = ConfigParser.ConfigParser()
        config.read(CONFIG_FILE)
        project_dir = config.get('spicaweb', 'project_dir')
        title = config.get('auth', 'title')
        db_file = config.get('sqlite', 'db_file')
        smtp_server = config.get('email', 'smtp_server')
        port = config.get('email', 'port')
        fr = config.get('email', 'from')
        user = config.get('email', 'user')
        password = config.get('email', 'password')

        self.a = auth.Auth(get_template, get_template_args(), ROOT_URL,
                           title, db_file)
        self.a.set_email_settings(smtp_server, port, fr, user, password)

        # authentication links (because I want them in root, not /auth/login)
        self.login = self.a.login
        self.alogin = self.a.alogin
        self.register = self.a.register
        self.aregister = self.a.aregister
        self.forgot_password = self.a.forgot_password
        self.aforgot_password = self.a.aforgot_password
        self.change_password_once = self.a.change_password
        self.achange_password_once = self.a.achange_password
        self.activate_account = self.a.activate_account
        self.logout = self.a.logout
        # the following are only accessible by authenticated users
        self.account = self.a.account

        self.app = App(self.a, ROOT_URL, project_dir)
        #self.news = news.News()

    # wrappers to disallow access for guest account
    @cherrypy.expose
    def delete_account(self):
        if(self.is_guest_user()):
            return self.no_guest_access()
        else:
            return self.a.delete_account()

    @cherrypy.expose
    def adelete_account(self, username, password):
        if(self.is_guest_user()):
            return None
        else:
            return self.a.adelete_account(username, password)

    @cherrypy.expose                                                            
    def change_password(self):            
        if(self.is_guest_user()):
            return self.no_guest_access()
        else:
            return self.a.change_password()
                                                                               
    @cherrypy.expose                                                            
    def achange_password(self, password):  
        if(self.is_guest_user()):
            return None
        else:
            return self.a.achange_password(password)

    def no_guest_access(self):
        kw_args = get_template_args()
        template_name = 'no_guest_access'
        return get_template('%s.html' % (template_name), **kw_args)

    def is_guest_user(self):
        guest_users = ['spica.webapp@gmail.com']
        guest_users.extend(['guest%i' % (i) for i in xrange(10)])
        user = cherrypy.session.get(auth.Auth.SESSION_USER_KEY, None)
        return not user == None and user in guest_users

    # info pages
    @cherrypy.expose
    def index(self):

        kw_args = get_template_args()
        #TODO
        kw_args['news_collection'] = []
        template_name = 'home'

        return get_template('%s.html' % (template_name), **kw_args)

    @cherrypy.expose
    def home(self):
        return self.index()

    @cherrypy.expose
    def doc(self):
        url = '%s%sindex.html' % (ROOT_URL, header_menu[1][1])
        raise cherrypy.HTTPRedirect(url)

    @cherrypy.expose
    def software(self):
        hmi = 2
        kw_args = get_template_args(header_menu_index=hmi)
        template_f = '%s.html' % (header_menu[hmi][0])
        return get_template(template_f, **kw_args)

    @cherrypy.expose
    def about(self):
        hmi = 3
        kw_args = get_template_args(header_menu_index=hmi)
        template_f = '%s.html' % (header_menu[hmi][0])
        return get_template(template_f, **kw_args)

    @cherrypy.expose
    def contact(self):
        hmi = 4
        kw_args = get_template_args(header_menu_index=hmi)
        template_f = '%s.html' % (header_menu[hmi][0])
        return get_template(template_f, **kw_args)


###############################################################################
# The App class
###############################################################################


@cherrypy.tools.authenticate()
class App:
    def __init__(self, authentication, root_url, projects_dir):

        pm = project_management.ProjectManager(projects_dir)
        self.root_url = root_url

        self.projects = project.Project(authentication, pm, self.root_url,
                main_menu, 1, sub_menus[1])

        self.features = feature.Feature(authentication, pm, self.root_url,
                main_menu, 2, sub_menus[2])

        self.classification = classification.Classification(authentication, pm,
                self.root_url, main_menu, 3, sub_menus[3])

    @cherrypy.expose()
    def index(self):
        print
        print 'App self.root_url'
        print self.root_url
        print
        url = '%sapp/projects/list' % (self.root_url)
        raise cherrypy.HTTPRedirect(url)

    # TODO check if needed... some helper functions
    def redirect_to_first_sub(self):
        new_uri = '%s%s/%s/%s' % (self.root_url, main_menu[self.menu_index],
                self.project_id, sub_menus[self.menu_index][0])
        raise cherrypy.HTTPRedirect(new_uri)

    def project_not_exist(self):
        kw_args = self.get_template_args()
        template_name = 'project_not_exist'
        return get_template('%s.html' % (template_name), **kw_args)

#app = cherrypy.tree.mount(Root(), '/spica', 'prod.cfg')
