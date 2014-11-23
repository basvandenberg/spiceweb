import os
import shutil
import ConfigParser
import cherrypy
from mako.lookup import TemplateLookup

from cherrypy_auth import auth
from spice import project_management

import project
import feature
import classification
import news

###############################################################################
# Paths
###############################################################################

# path to spiceweb module
spiceweb_dir = os.path.dirname(os.path.abspath(__file__))

# path to template directories
tmpl_d = os.path.join(spiceweb_dir, 'templates')
auth_tmpl_d = os.path.join(os.path.dirname(os.path.abspath(auth.__file__)),
                           'template/mako')

# config file name
CONFIG_FILE = 'spiceweb.cfg'

# read root url from config
config = ConfigParser.ConfigParser()
config.read(CONFIG_FILE)
ROOT_URL = config.get('spiceweb', 'root_url')
NEWS_F = config.get('spiceweb', 'news_f')

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
    ('projects', 'app/projects/'),
    ('features', 'app/features/'),
    ('classification', 'app/classification/')
]

# sub menu items
sub_menus = [
    [],
    ['list', 'new', 'details'],
    ['list', 'calculate', 'upload', 'ttest', 'histogram', 'scatter',
     'heatmap'],
    ['list', 'new', 'details', 'run']
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
        if(user_id is None):
            #user_id = cherrypy.session.id
            try:
                user_id = cherrypy.request.cookie['spice.session'].value
            except KeyError:
                user_id = None
    else:
        user_id = None

    # retrieve project id from cookie
    if(user_id and hasattr(cherrypy, 'session')):
        project_id = cherrypy.session.get(project.Project.SESSION_PROJECT_KEY,
                None)

        # HACK added to obtain project ids...
        config = ConfigParser.ConfigParser()
        config.read(CONFIG_FILE)
        project_dir = config.get('spiceweb', 'project_dir')
        ref_data_dir = config.get('spiceweb', 'ref_data_dir')
        pm = project_management.ProjectManager(project_dir, ref_data_dir)
        # first check if there is a user?
        pm.set_user(user_id)
        all_project_ids = pm.get_projects()

    else:
        project_id = None
        all_project_ids = None

    return {'user_id': user_id,
            'project_id': project_id,
            'all_project_ids': all_project_ids,
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

        # read spiceweb config file
        config = ConfigParser.ConfigParser()
        config.read(CONFIG_FILE)
        self.project_dir = config.get('spiceweb', 'project_dir')
        self.ref_data_dir = config.get('spiceweb', 'ref_data_dir')
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
        self.register = self.a.register
        self.aregister = self.a.aregister
        self.forgot_password = self.a.forgot_password
        self.aforgot_password = self.a.aforgot_password
        self.change_password_once = self.a.change_password_once
        self.achange_password_once = self.a.achange_password_once
        self.activate_account = self.a.activate_account
        # the following are only accessible by authenticated users
        self.account = self.a.account
        self.delete_account = self.a.delete_account
        self.change_password = self.a.change_password
        self.achange_password = self.a.achange_password

        self.app = App(self.a, ROOT_URL, self.project_dir, self.ref_data_dir)

    # wrapper around logout to remove active project from session data
    @cherrypy.expose
    def logout(self):
        cherrypy.session[project.Project.SESSION_PROJECT_KEY] = None
        return self.a.logout()

    # wrapper around login to remove active project from session data, this
    # should not happen, because these are removed during logout in the
    # function above
    @cherrypy.expose
    def alogin(self, username, password):
        cherrypy.session[project.Project.SESSION_PROJECT_KEY] = None
        return self.a.alogin(username, password)

    # wrapper arount delete account, to delete its project data as well
    @cherrypy.expose
    def adelete_account(self, username, password):
        # delete project dir (after password verification)
        if(self.a.udb.verify_password(username, password)):
            pm = project_management.ProjectManager(self.project_dir,
                                                   self.ref_data_dir)
            pm.set_user(username)
            shutil.rmtree(pm.user_dir)
            cherrypy.session[project.Project.SESSION_PROJECT_KEY] = None
        # delete account
        return self.a.adelete_account(username, password)

    # info pages
    @cherrypy.expose
    def index(self):
        
        n = news.News(NEWS_F)
        news_items = n.parse(number_of_items=3)

        kw_args = get_template_args()
        kw_args['news_items'] = news_items
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
    def news(self):
        hmi = 0

        n = news.News(NEWS_F)
        news_items = n.parse()

        kw_args = get_template_args(header_menu_index=hmi)
        kw_args['news_items'] = news_items

        template_f = '%s.html' % (header_menu[hmi][0])
        return get_template(template_f, **kw_args)

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
    def __init__(self, authentication, root_url, projects_dir, ref_data_dir):

        pm = project_management.ProjectManager(projects_dir, ref_data_dir)
        self.root_url = root_url

        self.projects = project.Project(authentication, pm, self.root_url,
                main_menu, 1, sub_menus[1])

        self.features = feature.Feature(authentication, pm, self.root_url,
                main_menu, 2, sub_menus[2])

        self.classification = classification.Classification(authentication, pm,
                self.root_url, main_menu, 3, sub_menus[3])

    @cherrypy.expose()
    def index(self):
        url = '%sapp/projects/list' % (self.root_url)
        raise cherrypy.HTTPRedirect(url)
