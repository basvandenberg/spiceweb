import simplejson

import cherrypy
from cherrypy.lib.static import serve_file

import spiceweb
from project import Project


class Feature:

    def __init__(self, auth, project_manager, root_url, main_menu,
                 main_menu_index, sub_menu):

        self.auth = auth
        self.project_manager = project_manager
        self.root_url = root_url

        self.mmi = main_menu_index
        self.mm_name, self.mm_url = main_menu[self.mmi]
        self.sub_menu = sub_menu

    def get_project_id(self):
        return cherrypy.session.get(Project.SESSION_PROJECT_KEY, None)

    def fetch_session_data(self):
        self.user_id = self.auth.get_user()
        if(self.user_id is None):
            #self.user_id = cherrypy.session.id
            self.user_id = cherrypy.request.cookie['spice.session'].value
        self.project_id = self.get_project_id()
        self.project_manager.set_user(self.user_id)
        self.project_manager.set_project(self.project_id)

    def get_url(self, smi):
        return '%s%s%s' % (self.root_url, self.mm_url, self.sub_menu[smi])

    def get_template_f(self, smi):
        return '%s_%s.html' % (self.mm_name, self.sub_menu[smi])

    def get_template_args(self, smi):
        return spiceweb.get_template_args(main_menu_index=self.mmi,
                                          sub_menu_index=smi)

    # Duplicate method in classification.py
    def no_project_selected(self):
        kw_args = self.get_template_args(0)
        template_f = 'no_project_selected.html'
        return spiceweb.get_template(template_f, **kw_args)

    @cherrypy.expose
    def index(self):
        raise cherrypy.HTTPRedirect(self.get_url(0))

    @cherrypy.expose
    def list(self):

        smi = 0

        self.fetch_session_data()

        if(self.project_id is None):
            return self.no_project_selected()

        pm = self.project_manager
        fe = pm.get_feature_extraction()

        kw_args = self.get_template_args(smi)

        kw_args['fe'] = fe
        kw_args['featcats'] = fe.PROTEIN_FEATURE_CATEGORIES
        kw_args['feat_status'] = pm.get_feat_calc_status()

        template_f = self.get_template_f(smi)

        return spiceweb.get_template(template_f, **kw_args)
    
    @cherrypy.expose
    def calculate(self, featcat_id=None):

        smi = 1

        self.fetch_session_data()

        if(self.project_id is None):
            return self.no_project_selected()
        
        pm = self.project_manager
        kw_args = self.get_template_args(smi)

        if not(featcat_id is None):
            # check if feature is allready available
            #kw_args['error_msg'] = 'These features are allready available'
            self.project_manager.run_feature_extraction([featcat_id])

        template_f = self.get_template_f(smi)
        return spiceweb.get_template(template_f, **kw_args)

    @cherrypy.expose
    def upload(self, object_ids_f=None, feature_matrix_f=None):

        smi = 2

        self.fetch_session_data()

        if(self.project_id is None):
            return self.no_project_selected()

        pm = self.project_manager
        kw_args = self.get_template_args(smi)

        # upload custom feature matrix
        error_msg = None
        if(object_ids_f and feature_matrix_f):

            if(object_ids_f.file is None):
                error_msg = 'No protein ids file selected'
            elif(feature_matrix_f.file is None):
                error_msg = 'No feature matrix file selected'
            else:
                error_msg = pm.add_custom_features(self.project_id,
                                                   object_ids_f,
                                                   feature_matrix_f)

            if(error_msg == ''):
                # redirect to feature list if no errors occured
                raise cherrypy.HTTPRedirect(self.get_url(0))

            else:
                kw_args['msg'] = error_msg

        template_f = self.get_template_f(smi)
        return spiceweb.get_template(template_f, **kw_args)

    @cherrypy.expose
    def ttest(self):
        smi = 3
        return self.show_feature_data(smi)

    @cherrypy.expose
    def histogram(self):
        smi = 4
        return self.show_feature_data(smi)

    @cherrypy.expose
    def scatter(self):
        smi = 5
        return self.show_feature_data(smi)

    @cherrypy.expose
    def heatmap(self):
        smi = 6
        return self.show_feature_data(smi)

    def show_feature_data(self, smi):

        self.fetch_session_data()

        if(self.project_id is None):
            return self.no_project_selected()

        kw_args = self.get_template_args(smi)
        kw_args['fe'] = self.project_manager.get_feature_extraction()
        #kw_args['show_filter'] = self.project_manager.get_feat_calc_status()
        kw_args['show_filter'] = True

        template_f = self.get_template_f(smi)

        return spiceweb.get_template(template_f, **kw_args)

    #
    # ajax functions
    #
    @cherrypy.expose
    def class_names(self, labeling_name):

        self.fetch_session_data()

        cherrypy.response.headers['Content-Type'] = 'application/json'

        fm = self.project_manager.get_feature_matrix()
        class_names = fm.labeling_dict[labeling_name].class_names

        str_data0 = '<ul id="labels_selected"' +\
                    'class="ui-helper-reset label_list select">\n'
        str_data1 = '<ul id="labels_unselected" ' +\
                    'class="ui-helper-reset ui-helper-clearfix label_list">\n'
        for class_name in class_names:
            str_data1 += '  <li class="class_label ui-widget-content">\n'
            str_data1 += '    <div>%s</div>\n' % (class_name)
            str_data1 += '    <a href="#" ' +\
                         'class="ui-icon ui-icon-triangle-1-w"></a>\n'
            str_data1 += '  </li>\n'

        str_data1 += '</ul>\n'

        return simplejson.dumps(dict(class_names_selected=str_data0,
                                class_names_unselected=str_data1))

    @cherrypy.expose
    def attest(self, labeling_name, class_ids):

        self.fetch_session_data()

        cherrypy.response.headers['Content-Type'] = 'application/json'

        label0, label1 = class_ids.split(',')

        # obtain table data
        fm = self.project_manager.get_feature_matrix()
        ttest_data = fm.ttest(labeling_name, label0.strip(), label1.strip())

        # obtain feature id to name and feature vector name mapping
        fe = self.project_manager.get_feature_extraction()
        featname_dict = fe.protein_feat_id_to_name_dict()

        # create html table
        str_data = ''
        for index, (tval, pval) in enumerate(ttest_data):

            fid = fm.feature_ids[index]
            fvec, fname = featname_dict[fid]

            str_data += '<tr id=%s>\n' % (fid)
            str_data += '<td>%s</td>' % (fvec.capitalize())
            str_data += '  <td>%s</td>\n' % (fname)
            str_data += '  <td class="n">%.2f</td>\n' % (tval)
            str_data += '  <td class="n">%.15f</td>\n' % (pval)
            str_data += '</tr>\n'

        return simplejson.dumps(dict(ttest_table=str_data))

    @cherrypy.expose
    def ahistogram(self, feat_ids, labeling_name, class_ids, figtype='png'):

        class_ids = [l.strip() for l in class_ids.split(',')]
        pm = self.project_manager
        fm = pm.get_feature_matrix()
        fm_root_dir = pm.fm_dir
        fe = pm.get_feature_extraction()
        featname_dict = fe.protein_feat_id_to_name_dict()
        fvec, _ = fe.protein_feat_id_to_name_dict()[feat_ids]

        if(figtype == 'svg'):
            filetype = 'image/svg+xml'
            filepath = fm.save_histogram(feat_ids, labeling_name=labeling_name,
                                         class_ids=class_ids, img_format='svg',
                                         root_dir=fm_root_dir, title=fvec)
        else:
            filetype = 'image/png'
            filepath = fm.save_histogram(feat_ids, labeling_name=labeling_name,
                                         class_ids=class_ids,
                                         root_dir=fm_root_dir, title=fvec)

        # serve the file
        return serve_file(filepath, filetype, 'attachment')

    @cherrypy.expose
    def ascatter(self, feat_ids, labeling_name, class_ids, figtype='png'):

        feat_ids = [f.strip() for f in feat_ids.split(',')]
        class_ids = [l.strip() for l in class_ids.split(',')]
        pm = self.project_manager
        fm = pm.get_feature_matrix()
        fm_root_dir = pm.fm_dir
        fe = pm.get_feature_extraction()
        featname_dict = fe.protein_feat_id_to_name_dict()
        fvec0, _ = fe.protein_feat_id_to_name_dict()[feat_ids[0]]
        fvec1, _ = fe.protein_feat_id_to_name_dict()[feat_ids[1]]

        if(figtype == 'svg'):
            filetype = 'image/svg+xml'
            filepath = fm.save_scatter(feat_ids[0], feat_ids[1],
                                       labeling_name=labeling_name,
                                       class_ids=class_ids, img_format='svg',
                                       root_dir=fm_root_dir, feat0_pre=fvec0,
                                       feat1_pre=fvec1)
        else:
            filetype = 'image/png'
            filepath = fm.save_scatter(feat_ids[0], feat_ids[1],
                                       labeling_name=labeling_name,
                                       class_ids=class_ids, img_format='png',
                                       root_dir=fm_root_dir, feat0_pre=fvec0,
                                       feat1_pre=fvec1)

        # serve the file
        return serve_file(filepath, filetype, 'attachment')

    @cherrypy.expose
    def acheck_heatmap_size(self, **data):
        
        max_proteins = 3000

        labeling_name = data['labeling_name']
        class_ids = data['class_ids[]']
        if not(isinstance(class_ids, list)):
            class_ids = [class_ids]

        pm = self.project_manager
        objs = pm.get_feature_matrix().object_indices(labeling_name, class_ids)
        
        if(len(objs) > max_proteins):
            msg = 'Heatmaps are only possible for %i proteins or less.'\
                  % (max_proteins)
        else:
            msg = ''

        cherrypy.response.headers['Content-Type'] = 'application/json'
        return simplejson.dumps(dict(msg=msg))

    @cherrypy.expose
    def aheatmap(self, feat_ids, labeling_name, class_ids, figtype='png'):

        feat_ids = [f.strip() for f in feat_ids.split(',')]
        class_ids = [l.strip() for l in class_ids.split(',')]
        
        pm = self.project_manager
        fm = pm.get_feature_matrix()
        fm_root_dir = pm.fm_dir

        filepath = fm.get_clustdist_path(feature_ids=feat_ids,
                                         labeling_name=labeling_name,
                                         class_ids=class_ids,
                                         root_dir=fm_root_dir)

        if(figtype == 'svg'):
            filetype = 'image/svg+xml'
            filepath += '.svg'
        else:
            filetype = 'image/png'
            filepath += '.png'

        # serve the file
        return serve_file(filepath, filetype, 'attachment')
