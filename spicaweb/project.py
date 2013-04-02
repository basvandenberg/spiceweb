import os
import shutil
import zipfile
import simplejson

import cherrypy
from cherrypy.lib.static import serve_file

import spica


class Project:

    SESSION_PROJECT_KEY = 'project_id'

    def __init__(self, auth, project_manager, root_url, main_menu,
            main_menu_index, sub_menu):

        self.auth = auth
        self.project_manager = project_manager
        self.root_url = root_url

        self.menu_name = main_menu[main_menu_index][0]
        self.sub_menu = sub_menu

    def get_project_id(self):
        return cherrypy.session.get(self.SESSION_PROJECT_KEY, None)

    def fetch_session_data(self):
        self.user_id = self.auth.get_user()
        self.project_id = self.get_project_id()
        self.project_manager.set_user(self.user_id)
        self.project_manager.set_project(self.project_id)

    @cherrypy.expose
    def index(self):
        # TODO use some setting to get this path
        url = '%sapp/projects/list' % (self.root_url)
        raise cherrypy.HTTPRedirect(url)

    @cherrypy.expose
    def list(self):

        self.fetch_session_data()
        mmi = 1
        smi = 0
        projects = self.project_manager.get_projects()

        kw_args = spica.get_template_args(main_menu_index=mmi,
                sub_menu_index=smi)
        kw_args['projects'] = projects
        template_f = '%s_%s.html' % (spica.main_menu[mmi][0],
                spica.sub_menus[mmi][smi])

        return spica.get_template(template_f, **kw_args)

    @cherrypy.expose
    def new(self, project_id=None, fasta_file=None, sequence_type=None):

        self.fetch_session_data()
        mmi = 1
        smi = 1

        # start a new project
        if((fasta_file and sequence_type) and project_id):

            # initiate new project
            self.project_manager.start_new_project(project_id, fasta_file,
                    sequence_type)

            # if creation went well, store project id in session
            cherrypy.session['project_id'] = project_id

            # redirect to project list page TODO set project as current and go
            # to details page
            new_uri = '%s%s/%s' % (self.root_url, spica.main_menu[mmi][1],
                    spica.sub_menus[mmi][0])

            raise cherrypy.HTTPRedirect(new_uri)

        # show form
        kw_args = spica.get_template_args(main_menu_index=mmi,
                sub_menu_index=smi)
        template_f = '%s_%s.html' % (spica.main_menu[mmi][0],
                spica.sub_menus[mmi][smi])

        return spica.get_template(template_f, **kw_args)

    @cherrypy.expose
    def details(self, project_id):

        self.fetch_session_data()
        mmi = 1
        smi = 2

        # store project id in session
        cherrypy.session['project_id'] = project_id

        # set project_id as the current active project
        self.project_manager.set_project(project_id)

        # TODO try this, except no project, than redirect...?
        fe = self.project_manager.get_feature_extraction()

        kw_args = spica.get_template_args(main_menu_index=mmi,
                sub_menu_index=smi)
        kw_args['fe'] = fe

        template_f = '%s_%s.html' % (spica.main_menu[mmi][0],
                spica.sub_menus[mmi][smi])

        return spica.get_template(template_f, **kw_args)

    #
    # ajax methods
    #

    def download(self, data_type='project', data_name=None):

        if(data_type == 'project'):
            filetype = 'application/zip'
            filepath = os.path.join(self._get_user_dir(),
                    '%s.zip' % (self.project_id))
            with zipfile.ZipFile(filepath, 'w') as fout:
                first = True
                for root, dirs, files in os.walk(self._get_project_dir()):
                    if first:
                        rootroot = os.path.dirname(root)
                        first = False
                    arcroot = os.path.relpath(root, rootroot)
                    for file in files:
                        fout.write(os.path.join(root, file),
                                arcname=os.path.join(arcroot, file))

        elif(data_type == 'data_source'):
            filetype = 'text/plain'
            fe = self.get_feature_extraction()
            filepath = fe.ds_dict[data_name].get_path()

        elif(data_type == 'labeling'):
            filetype = 'text/plain'
            fm = self.get_feature_matrix()
            filepath = os.path.join(fm.labels_dir, '%s.txt' % (data_name))

        return serve_file(filepath, filetype, 'attachment')

    # handle upload of data file, redirect to project details
    def upload(self, data_type, data_name, data_file):

        fe = self.get_feature_extraction()

        if(data_type == 'data_source'):

            try:
                fe.read_data_source(data_name, data_file.file)
                fe.save()
            except Exception as e:
                print '\n%s\n%s\n%s\n' % (e, type(e), e.args)
                # TODO show error

        elif(data_type == 'labeling'):

            try:
                fe.feature_matrix.load_labels(data_name, data_file.file)
                fe.save()
            except Exception as e:
                print '\n%s\n%s\n%s\n' % (e, type(e), e.args)
                # TODO show error

        # redirect back to the project details page
        # TODO do same return as delete function
        new_uri = '%s%s/%s/%s' % (self.root_url,
                spica.main_menu[self.menu_index], self.project_id,
                spica.sub_menus[self.menu_index][self.sub_menu_index])
        raise cherrypy.HTTPRedirect(new_uri)

    @cherrypy.expose
    def delete(self, project_id):
        '''
        This function handles an ajax call to delete a project.
        '''

        self.fetch_session_data()
        cherrypy.response.headers['Content-Type'] = 'application/json'

        # let the project manager delete the project
        success = self.project_manager.delete_project(project_id)

        # return result message
        if(success):
            msg = 'Project successfully removed'
        else:
            msg = 'Unable to delete project, project does not exist'

        return simplejson.dumps(dict(msg=msg))

