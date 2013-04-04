import os
import datetime

import cherrypy

from mako.lookup import TemplateLookup

from cherrypy_auth import auth

from spica import project_management
from spica import job_management

import project
import feature
import classification
import news

# settings that need to be changed
# TODO these paths should be in tools settings...
root_url = 'http://localhost:8080/spica/'
root_dir = '/home/bastiaan/Develop/spicaweb_test/'
projects_dir = os.path.join(root_dir, 'projects')
config_f = os.path.join(root_dir, 'spica.cfg')
auth_config_f = os.path.join(root_dir, 'auth.cfg')
news_dir = os.path.join(root_dir, 'news')

# path to template directory
data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
tmpl_dir = os.path.join(data_dir, 'templates')
# TODO fetch from config or something...
auth_tmpl_dir = '/home/bastiaan/Develop/cherrypy_auth/' +\
        'cherrypy_auth/template/mako'

def authenticate():
    '''
    Authentication decorator, redirect to login if user is not logged in.
    '''
    user = cherrypy.session.get(auth.Auth.SESSION_USER_KEY, None)
    if(user is None):
        raise cherrypy.HTTPRedirect('%slogin' % (root_url))

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
# Temlpate stuff
###############################################################################

# create global template lookup object
mylookup = TemplateLookup(directories=[tmpl_dir, auth_tmpl_dir],
                          module_directory='/tmp/mako/')


# function to obtain templates
def get_template(name, **kwargs):
    t = mylookup.get_template(name)
    return t.render(**kwargs)


# get default template arguments dictionary
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
            'root_url': root_url,
            'show_filter': False}

###############################################################################
# The Root class
###############################################################################


class Root:

    def __init__(self):
        
        # create authentication object
        a = auth.Auth(get_template, get_template_args(), root_url,
                auth_config_f)

        # authentication links (because I want them in root, not /auth/login)
        self.login = a.login
        self.alogin = a.alogin
        self.register = a.register
        self.aregister = a.aregister
        self.forgot_password = a.forgot_password
        self.aforgot_password = a.aforgot_password
        self.change_password = a.change_password
        self.achange_password = a.achange_password
        self.activate_account = a.activate_account
        self.logout = a.logout
        # the following are only accessible by authenticated users
        self.account = a.account
        self.change_password_once = a.change_password_once
        self.achange_password_once = a.achange_password_once
        self.delete_account = a.delete_account
        self.adelete_account = a.adelete_account

        # links to the app, documentation and news page
        self.app = App(a)
        self.news = news.News()

        # the other static data page links are the functions in this class.

    @cherrypy.expose
    def index(self, project_id=None):

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
        url = '%s%sindex.html' % (root_url, header_menu[1][1])
        raise cherrypy.HTTPRedirect(url)

    @cherrypy.expose
    def software(self, project_id=None):
        hmi = 2
        kw_args = get_template_args(header_menu_index=hmi)
        template_f = '%s.html' % (header_menu[hmi][0])
        return get_template(template_f, **kw_args)

    @cherrypy.expose
    def about(self, project_id=None):
        hmi = 3
        kw_args = get_template_args(header_menu_index=hmi)
        template_f = '%s.html' % (header_menu[hmi][0])
        return get_template(template_f, **kw_args)

    @cherrypy.expose
    def contact(self, project_id=None):
        hmi = 4
        kw_args = get_template_args(header_menu_index=hmi)
        template_f = '%s.html' % (header_menu[hmi][0])
        return get_template(template_f, **kw_args)


@cherrypy.tools.authenticate()
class App:
    def __init__(self, authentication):

        pm = project_management.ProjectManager(projects_dir)

        self.projects = project.Project(authentication, pm, root_url,
                main_menu, 1, sub_menus[1])

        self.features = feature.Feature(authentication, pm, root_url,
                main_menu, 2, sub_menus[2])

        self.classification = classification.Classification(authentication, pm,
                root_url, main_menu, 3, sub_menus[3])

    @cherrypy.expose()
    def index(self):
        url = '%sapp/projects/list' % (root_url)
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

    def timestamp_str(self):
        return datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:-3]
