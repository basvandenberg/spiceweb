import os
import simplejson
import zipfile

import cherrypy
from cherrypy.lib.static import serve_file

from spice import featmat
from biopy import sequtil
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

        # retrieve logged in user
        self.user_id = self.auth.get_user()

        # if no logged in user, request unregistered user id from cookie
        if(self.user_id is None):
            self.user_id = cherrypy.request.cookie['spice.session'].value

        # fetch current project id from session data
        self.project_id = self.get_project_id()

        if not(self.project_id is None):

            # fetch project ids for current user
            existing_projects = [p[0] for p in
                                 self.project_manager.get_projects()]

            # if user does not have project with project id
            if not(self.project_id in existing_projects):

                # reset session project id to None
                cherrypy.session[Project.SESSION_PROJECT_KEY] = None

                # set project id to None
                self.project_id = None

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
        fe = pm.get_feature_extraction()

        kw_args = self.get_template_args(smi)
        kw_args['fe'] = fe

        if not(featcat_id is None):

            proteins = fe.protein_data_set.proteins
            featcat = fe.PROTEIN_FEATURE_CATEGORIES[featcat_id.split('_')[0]]
            missing_data = []

            # check if data required for feature calculation is available
            for get_data_func, all_objects in featcat.required_data:
                name = ' '.join(get_data_func.__name__.split('_')[1:])
                if(all_objects):
                    if not(all([get_data_func(p) for p in proteins])):
                        missing_data.append(name)
                else:
                    if not(any([get_data_func(p) for p in proteins])):
                        missing_data.append(name)
            if(len(missing_data) > 0):
                kw_args['msg'] = '<p>Required data is missing: %s</p>' %\
                    (', '.join(missing_data))

            # check if this feature category is already in the feature matrix
            elif(featcat_id in fe.available_protein_featcat_ids()):
                kw_args['msg'] = 'This feature category has ' +\
                    'already been calculated'

            else:
                # put job in queue
                pm.run_feature_extraction([featcat_id])

                # redirect to feature list page
                raise cherrypy.HTTPRedirect(self.get_url(0))

        kw_args['aaindex_scale_ids'] = sequtil.aaindex_scale_ids
        kw_args['pseaac_scale_ids'] = sequtil.pseaac_scale_ids

        template_f = self.get_template_f(smi)
        return spiceweb.get_template(template_f, **kw_args)

    @cherrypy.expose
    def upload(self, object_ids_f=None, feature_matrix_f=None):

        smi = 2

        self.fetch_session_data()

        if(self.project_id is None):
            return self.no_project_selected()

        pm = self.project_manager
        fe = pm.get_feature_extraction()

        kw_args = self.get_template_args(smi)
        kw_args['fe'] = fe

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
    def download(self):
        '''
        This functions returns the current feature matrix (zipped)
        '''

        self.fetch_session_data()
        pm = self.project_manager

        filetype = 'application/zip'
        filepath = os.path.join(pm.user_dir,
                                '%s_feature_matrix.zip' % (self.project_id))

        with zipfile.ZipFile(filepath, 'w') as fout:
            first = True
            for root, dirs, files in os.walk(pm.fm_dir):
                # only add root dir files, skipping labels and images dir
                if first:
                    first = False
                    rootroot = os.path.dirname(root)
                    arcroot = os.path.relpath(root, rootroot)
                    for file in files:
                        fout.write(os.path.join(root, file),
                                   arcname=os.path.join(arcroot, file))

        return serve_file(filepath, filetype, 'attachment')

    @cherrypy.expose
    def delete(self, featcat_id):
        '''
        This function handles an ajax call to delete feature category.
        '''
        self.fetch_session_data()
        
        fm = self.project_manager.get_feature_matrix()

        num_fc_items = len(featcat_id.split('_'))

        remove_feat_ids = []
        for feat_id in fm.feature_ids:
            if('_'.join(feat_id.split('_')[:num_fc_items]) == featcat_id):
                remove_feat_ids.append(feat_id)

        fm.remove_features(remove_feat_ids)
        fm.save_to_dir(self.project_manager.fm_dir)

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

        # create html table
        str_data = ''
        for index, (tval, pval) in enumerate(ttest_data):

            fid = fm.feature_ids[index]

            tokens = fid.split('_')
            if(len(tokens) == 2):
                fcat_id, feat_id = tokens
                params = ''
            else:
                fcat_id, params, feat_id = tokens

            cusfeat = featmat.FeatureMatrix.CUSTOM_FEAT_PRE
            if fcat_id[:len(cusfeat)] == cusfeat:
                featcat_name = 'custom feature'
                feat_param = ''
                feat_name = fid
            else:
                featcat = fe.PROTEIN_FEATURE_CATEGORIES[fcat_id]
                id_to_name = featcat.feat_id_name_dict(params)

                featcat_name = featcat.fc_name
                feat_param = featcat.param_str(params)
                feat_name = id_to_name[feat_id]

            str_data += '<tr id=%s>\n' % (fid)
            str_data += '    <td>%s</td>\n' % (fid)
            str_data += '    <td>%s</td>\n' % (featcat_name)
            str_data += '    <td>%s</td>\n' % (feat_param)
            str_data += '    <td>%s</td>\n' % (feat_name)
            str_data += '    <td class="n">%.2f</td>\n' % (tval)
            str_data += '    <td class="n">%.05e</td>\n' % (pval)
            str_data += '</tr>\n'

        return simplejson.dumps(dict(ttest_table=str_data))

    @cherrypy.expose
    def ahistogram(self, feat_ids, labeling_name, class_ids):

        class_ids = [l.strip() for l in class_ids.split(',')]
        pm = self.project_manager
        fm = pm.get_feature_matrix()
        fm_root_dir = pm.fm_dir
        fe = pm.get_feature_extraction()

        tokens = feat_ids.split('_')

        if(len(tokens) == 3):
            fc, param, fid = tokens
            featcat = fe.PROTEIN_FEATURE_CATEGORIES[fc]
            param_s = featcat.param_str(param)
            title = '%s (%s)' % (featcat.fc_name, param_s)
        else:
            fc, fid = tokens
            title = 'Custom feature category %s' % (fc)

        num_bins = 40
        if(len(class_ids) > 2):
            num_bins = 30

        return fm.histogram_json(feat_ids, labeling_name, class_ids=class_ids,
                                 title=title, num_bins=num_bins)

    def ahistogram2(self, feat_ids, labeling_name, class_ids, figtype='png'):

        class_ids = [l.strip() for l in class_ids.split(',')]
        pm = self.project_manager
        fm = pm.get_feature_matrix()
        fm_root_dir = pm.fm_dir
        fe = pm.get_feature_extraction()

        tokens = feat_ids.split('_')

        if(len(tokens) == 3):
            fc, param, fid = tokens
            featcat = fe.PROTEIN_FEATURE_CATEGORIES[fc]
            param_s = featcat.param_str(param)
            title = '%s (%s)' % (featcat.fc_name, param_s)
        else:
            fc, fid = tokens
            title = 'Custom feature category %s' % (fc)

        if(figtype == 'svg'):
            filetype = 'image/svg+xml'
            filepath = fm.save_histogram(feat_ids, labeling_name=labeling_name,
                                         class_ids=class_ids, img_format='svg',
                                         root_dir=fm_root_dir, title=title)
        else:
            filetype = 'image/png'
            filepath = fm.save_histogram(feat_ids, labeling_name=labeling_name,
                                         class_ids=class_ids,
                                         root_dir=fm_root_dir, title=title)

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
        
        tokens0 = feat_ids[0].split('_')
        tokens1 = feat_ids[1].split('_')

        if(len(tokens0) == 3):
            fc0, param0, fid0 = tokens0
            featcat0 = fe.PROTEIN_FEATURE_CATEGORIES[fc0]
            param_s0 = featcat0.param_str(param0)
            lab0 = '%s (%s)' % (featcat0.fc_name, param_s0)
        else:
            lab0, _ = tokens0

        if(len(tokens1) == 3):
            fc1, param1, fid1 = tokens1
            featcat1 = fe.PROTEIN_FEATURE_CATEGORIES[fc1]
            param_s1 = featcat1.param_str(param1)
            lab1 = '%s (%s)' % (featcat1.fc_name, param_s1)
        else:
            lab1, _ = tokens1

        if(figtype == 'svg'):
            filetype = 'image/svg+xml'
            filepath = fm.save_scatter(feat_ids[0], feat_ids[1],
                                       labeling_name=labeling_name,
                                       class_ids=class_ids, img_format='svg',
                                       root_dir=fm_root_dir, feat0_pre=lab0,
                                       feat1_pre=lab1)
        else:
            filetype = 'image/png'
            filepath = fm.save_scatter(feat_ids[0], feat_ids[1],
                                       labeling_name=labeling_name,
                                       class_ids=class_ids, img_format='png',
                                       root_dir=fm_root_dir, feat0_pre=lab0,
                                       feat1_pre=lab1)

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
        objs = pm.get_feature_matrix().filtered_object_indices(labeling_name,
                                                               class_ids)

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
