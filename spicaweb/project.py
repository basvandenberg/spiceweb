import os
import re
import zipfile
import traceback

import cherrypy
from cherrypy.lib.static import serve_file

import spicaweb


class Project:

    SESSION_PROJECT_KEY = 'project_id'

    EXAMPLE_DIR = 'example_projects'
    EXAMPLES = [
        ('localization', 'protein.fsa', 'prot_seq', 'localization.txt'),
        ('production', 'orf.fsa', 'orf_seq', 'production.txt')
    ]

    def __init__(self, auth, project_manager, root_url, main_menu,
                 main_menu_index, sub_menu):

        self.auth = auth
        self.project_manager = project_manager
        self.root_url = root_url

        self.mmi = main_menu_index
        self.mm_name, self.mm_url = main_menu[self.mmi]
        self.sub_menu = sub_menu

    def get_project_id(self):
        return cherrypy.session.get(self.SESSION_PROJECT_KEY, None)

    def fetch_session_data(self):
        self.user_id = self.auth.get_user()
        self.project_id = self.get_project_id()
        self.project_manager.set_user(self.user_id)
        self.project_manager.set_project(self.project_id)
    
    def get_url(self, smi):
        return '%s%s%s' % (self.root_url, self.mm_url, self.sub_menu[smi])

    def get_template_f(self, smi):
        return '%s_%s.html' % (self.mm_name, self.sub_menu[smi])

    def get_template_args(self, smi):
        return spicaweb.get_template_args(main_menu_index=self.mmi,
                                          sub_menu_index=smi)

    @cherrypy.expose
    def index(self):
        raise cherrypy.HTTPRedirect(self.get_url(0))

    @cherrypy.expose
    def list(self):

        self.fetch_session_data()
        smi = 0

        projects = self.project_manager.get_projects()

        kw_args = self.get_template_args(smi)
        kw_args['projects'] = projects

        template_f = self.get_template_f(smi)

        return spicaweb.get_template(template_f, **kw_args)

    @cherrypy.expose
    def new(self, project_id=None, fasta_file=None, sequence_type=None):

        self.fetch_session_data()
        smi = 1

        kw_args = self.get_template_args(smi)

        error_msg = None

        # start a new project
        if((fasta_file and sequence_type) and project_id):

            if(fasta_file.file is None):
                error_msg = 'No fasta file provided'
            elif(len(project_id) < 4):
                error_msg = 'Project id should be at least 4 characters long'
            elif(' ' in project_id):
                error_msg = 'Spaces are not allowed in the project id'
            elif not(re.match('^[A-Za-z0-9_-]*$', project_id)):
                error_msg = 'Only characters, digits, dashes, and ' +\
                            'underscores are allowed in a project id'
            else:
                try:
                    # initiate new project
                    error_msg = self.project_manager.start_new_project(
                            project_id, fasta_file, sequence_type)
                except:
                    print(traceback.format_exc())
                    error_msg = 'Error creating new project'

            if(error_msg == ''):
                
                # store project id in session
                cherrypy.session[self.SESSION_PROJECT_KEY] = project_id

                # redirect to project list page
                url = self.get_url(0)
                raise cherrypy.HTTPRedirect(url)

            else:
                kw_args['msg'] = error_msg

        template_f = self.get_template_f(smi)

        return spicaweb.get_template(template_f, **kw_args)

    @cherrypy.expose
    def details(self, project_id, msg_data=None, msg_labeling=None):

        self.fetch_session_data()
        smi = 2
        
        # first check if the provided project_id excists
        existing_projects = [p[0] for p in self.project_manager.get_projects()]
        if not(project_id in existing_projects):
            kw_args = self.get_template_args(smi)
            template_f = 'no_such_project.html'
            return spicaweb.get_template(template_f, **kw_args)

        # store project id in session
        cherrypy.session[self.SESSION_PROJECT_KEY] = project_id

        # reset the session data, using the new project id
        self.fetch_session_data()

        # TODO try this, except no project, than redirect...?
        fe = self.project_manager.get_feature_extraction()

        kw_args = self.get_template_args(smi)
        kw_args['fe'] = fe
        kw_args['data_sources'] = ['prot_seq', 'orf_seq', 'ss_seq', 'sa_seq']
        kw_args['msg_data'] = msg_data
        kw_args['msg_labeling'] = msg_labeling

        template_f = self.get_template_f(smi)

        return spicaweb.get_template(template_f, **kw_args)

    @cherrypy.expose
    def load_example(self, example_number):

        self.fetch_session_data()
        smi = 1

        try:
            example_number = int(example_number)
        except ValueError:
            example_number = -1

        if(example_number < 0 or example_number >= len(self.EXAMPLES)):
            kw_args = self.get_template_args(smi)
            template_f = 'no_such_example.html'
            print template_f
            return spicaweb.get_template(template_f, **kw_args)
        
        pm = self.project_manager
        (pid, seq_f, seq_type, labeling_f) = self.EXAMPLES[example_number]

        root_d = spicaweb.spicaweb_dir
        seq_f = os.path.join(root_d, self.EXAMPLE_DIR, pid, seq_f)
        labeling_f = os.path.join(root_d, self.EXAMPLE_DIR, pid, labeling_f)
        error_msg = pm.start_example_project(pid, seq_f, seq_type, labeling_f)
        
        if(error_msg == ''):
            
            # store project id in session
            cherrypy.session[self.SESSION_PROJECT_KEY] = pid

            # redirect to project list page
            url = self.get_url(0)
            raise cherrypy.HTTPRedirect(url)

        else:
            print
            print 'This should not happen...'
            print error_msg
        
        url = self.get_url(0)
        raise cherrypy.HTTPRedirect(url)

    #
    # ajax methods
    #

    @cherrypy.expose
    def download(self, data_type='project', data_name=None):

        self.fetch_session_data()
        pm = self.project_manager

        if(data_type == 'project'):

            filetype = 'application/zip'
            filepath = os.path.join(pm.user_dir, '%s.zip' % (self.project_id))

            with zipfile.ZipFile(filepath, 'w') as fout:
                first = True
                for root, dirs, files in os.walk(pm.project_dir):
                    if first:
                        rootroot = os.path.dirname(root)
                        first = False
                    arcroot = os.path.relpath(root, rootroot)
                    for file in files:
                        fout.write(os.path.join(root, file),
                                arcname=os.path.join(arcroot, file))

        elif(data_type == 'data_source'):
            filetype = 'text/plain'
            fe = pm.get_feature_extraction()
            filepath = fe.protein_data_set.ds_dict[data_name].get_data_path()

        elif(data_type == 'labeling'):
            filetype = 'text/plain'
            fm = pm.get_feature_matrix()
            filepath = os.path.join(fm.labels_dir, '%s.txt' % (data_name))

        return serve_file(filepath, filetype, 'attachment')

    # handle upload of data file, redirect to project details
    @cherrypy.expose
    def upload(self, data_type, data_name, data_file):

        # TODO get_feature_extraction() get called twice, which could be a bit
        # expensive for larger data sets... check this, improve

        smi = 2

        self.fetch_session_data()
        pm = self.project_manager

        msg_data = ''
        msg_labeling = ''

        if(data_type == 'data_source'):
            if(data_file.file == None):
                msg_data = 'No file provided.'
            else:
                msg_data = pm.add_data_source(data_name, data_file.file)
        elif(data_type == 'labeling'):
            if(data_file.file == None):
                msg_labeling = 'No file provided.'
            else:
                msg_labeling = pm.add_labeling(data_name, data_file.file)
        else:
            msg_data = 'Unexpected upload error.'

        if(len(msg_labeling) > 100):
            msg_labeling = msg_labeling[:100] + '...' 

        # redirect to the project details page
        url = '%s/%s?msg_data=%s&msg_labeling=%s' %\
            (self.get_url(smi), pm.project_id, msg_data, msg_labeling)
        raise cherrypy.HTTPRedirect(url)

    @cherrypy.expose
    def delete(self, project_id):
        '''
        This function handles an ajax call to delete a project.
        '''
        self.fetch_session_data()
        self.project_manager.delete_project(project_id)

        # remove project id from session if it is the currently active one
        if(cherrypy.session[self.SESSION_PROJECT_KEY] == project_id):
            cherrypy.session[self.SESSION_PROJECT_KEY] = None
