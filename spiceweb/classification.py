import os
import simplejson
import numpy

import cherrypy
from cherrypy.lib.static import serve_file

import spiceweb
from project import Project

class Classification:

    SCORE_NAMES = {
        'roc_auc': 'AUROC', 'f1': 'F1-score', 'recall': 'Recall',
        'average_precision': 'Avg. precision', 'precision': 'Precision',
        'accuracy': 'Accuracy'
    }
    CL_NAMES = {
        'lda': 'Linear Distcriminant Analysis classifier',
        'qda': 'Quadratic Discriminant Analysis classifier',
        'nc': 'Nearest Centroid classifier',
        'kn_uniform': 'k-Nearest Neighbor classifier (uniform weights)',
        'kn_distance': 'k-Nearest Neighbor classifier (dist.-based weights)',
        'linearsvc': 'Linear Support Vector Machine (SVM) classifier',
        'svc_rbf': 'RBF-kernel Support Vector Machine (SVM) classifier',
        'gnb': 'Gaussian Naive Bayes classifier',
        'mnb': 'Multinomial Naive Bayes classifier',
        'bnb': 'Bernoulli naive bayes',
        'dtree': 'Decision Tree classifier',
        'rforest': 'Random Forest classifier'
    }

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

    # Duplicate method in feature.py
    def no_project_selected(self):
        kw_args = self.get_template_args(0)
        template_f = 'no_project_selected.html'
        return spiceweb.get_template(template_f, **kw_args)

    def no_such_classifier(self):
        kw_args = self.get_template_args(0)
        template_f = 'no_such_classifier.html'
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

        kw_args = self.get_template_args(smi)
        template_f = self.get_template_f(smi)

        return spiceweb.get_template(template_f, **kw_args)

    @cherrypy.expose
    def new(self, cl_type=None, n_fold_cv=None, labeling_name=None,
            class_ids=None, feat_ids=None):

        smi = 1
        self.fetch_session_data()

        if(self.project_id is None):
            return self.no_project_selected()

        error_msg = None

        # start classification job if required arguments from form are there
        if not(cl_type is None or n_fold_cv is None):

            pm = self.project_manager

            # check the number of class ids
            if(len(class_ids) < 2):
                error_msg = 'At least two classes should be provided.'
            elif(len(feat_ids) < 1):
                error_msg = 'No features selected.'
            else:
                pm.run_classification(cl_type, n_fold_cv, labeling_name,
                                      class_ids, feat_ids)

            # redirect to classifier list page
            raise cherrypy.HTTPRedirect(self.get_url(0))

        # show form otherwise
        else:
            kw_args = self.get_template_args(smi)
            kw_args['fe'] = self.project_manager.get_feature_extraction()
            kw_args['show_filter'] = True
            kw_args['error_msg'] = error_msg

            template_f = self.get_template_f(smi)

            return spiceweb.get_template(template_f, **kw_args)

    @cherrypy.expose
    def details(self, cl_id):

        smi = 2
        self.fetch_session_data()

        pm = self.project_manager

        if(self.project_id is None):
            return self.no_project_selected()

        if not(cl_id in pm.get_classifier_ids()):
            return self.no_such_classifier()

        kw_args = self.get_template_args(smi)
        kw_args['cl_id'] = cl_id

        if(self.project_manager.get_classifier_finished(cl_id)):
            cv_results, avg_results = pm.get_classifier_result(cl_id)
            kw_args['cv_results'] = cv_results
            kw_args['avg_results'] = avg_results
            kw_args['cl_settings'] = pm.get_classifier_settings(cl_id)
            kw_args['cl_names'] = self.CL_NAMES
            roc_f = pm.get_roc_f(cl_id)
            if(roc_f and os.path.exists(roc_f)):
                kw_args['roc_url'] = '%s%s%s/%s' % (self.root_url, self.mm_url,
                                                    'roc', cl_id)
            else:
                kw_args['roc_url'] = None

        template_f = self.get_template_f(smi)

        return spiceweb.get_template(template_f, **kw_args)

    ###########################################################################
    # ajax calls
    ###########################################################################

    # TODO this is a copy of the function in feature.py! 
    # Maybe create a parent class, some other methods can be inherited as well
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
    def result_tables(self):

        self.fetch_session_data()
        cherrypy.response.headers['Content-Type'] = 'application/json'

        def uri_details(cl_id):
            return '%s/%s' % (self.get_url(2), cl_id)

        # use project manager to fetch classification results
        cl_all_results = self.project_manager.get_all_classifier_results()

        # create result table if there are any results
        if(len(cl_all_results) > 0):

            score_names = sorted(cl_all_results.values()[0]
                .values()[0]['cv_results'].keys())

            sel_str = '<div id="score_select">\n'
            sel_str = '<label for="score">Score measure:</label>\n'
            sel_str = '<select id="score">\n'
            for sname in score_names:
                sel_str += '<option value="%s">%s</option>\n' % (sname, sname)
            sel_str += '</select>\n'
            sel_str += '</div>\n'

            str_data = '<div id="classifier_results">'
            for class_ids, cl_dict in cl_all_results.iteritems():

                # table title
                class_ids_str = ', '.join([' '.join(c.split('_')).capitalize()
                        for c in class_ids])
                str_data += '<h4>Classes: %s</h4>\n' % (class_ids_str)

                # sort classifier by id
                cl_ids = sorted(cl_dict.keys())

                str_data += '<table id="classResults" class="tablesorter">\n'
                str_data += '<thead>\n'
                str_data += '<tr>\n'
                str_data += '<th>job id</th>\n'
                str_data += '<th>classifier</th>\n'
                str_data += '<th># features</th>\n'
                str_data += '<th># CV-loops</th>\n'
                for sname in score_names:
                    str_data += '<th class="score" id="%s">%s</th>\n'\
                            % (sname, self.SCORE_NAMES[sname])
                str_data += '</tr>\n'
                str_data += '</thead>\n'
                str_data += '<tbody>\n'

                for cl_id in cl_ids:
                    cl_result = cl_dict[cl_id]['cv_results']
                    cv_scores = [cl_result[sname] for sname in score_names]
                    cl_settings = cl_dict[cl_id]['cl_settings']
                    str_data += '<tr>\n'
                    str_data += '<td><a href="%s">%s</a></td>\n' %\
                            (uri_details(cl_id), cl_id)
                    str_data += '<td>%s</td>\n' %\
                            (cl_settings['classifier_name'].split('.')[-1])
                    str_data += '<td class="n">%s</td>\n' %\
                            (len(cl_settings['feature_names']))
                    str_data += '<td class="n">%s</td>\n' %\
                            (cl_settings['n_fold_cv'])
                    for index, cv_score in enumerate(cv_scores):
                        if(cv_score[0] == -1.0):
                            score_str = 'n/a'
                        else:
                            score_str = '%.2f' % (numpy.mean(cv_score))
                        str_data += '<td class="score n" id="%s">%s</td>\n' %\
                                (score_names[index], score_str)
                    str_data += '</tr>\n'
                str_data += '</tbody>\n'
                str_data += '</table>\n\n'
                str_data += '</div>\n'

        # otherwise return emtpy table string
        else:
            str_data = '<div id="classifier_results">' +\
                    'No classification results available yet.</div>'
            sel_str = ''

        return simplejson.dumps(dict(result_tables=str_data,
                                score_select=sel_str))

    @cherrypy.expose
    def status_table(self):

        self.fetch_session_data()
        cherrypy.response.headers['Content-Type'] = 'application/json'

        def date_string(text):
            year = text[:4]
            month = text[4:6]
            day = text[6:8]
            h = text[9:11]
            m = text[11:13]
            s = text[13:15]
            return '%s-%s-%s %s:%s:%s' % (day, month, year, h, m, s)

        def uri_details(cl_id):
            return '%s/%s' % (self.get_url(2), cl_id)

        job_files = self.project_manager.fetch_job_files('classification')

        s = '<table id="sortTable" class="tablesorter">\n'
        s += '<thead>\n'
        s += '<tr>\n'
        s += '<th id="status"></th>\n'
        s += '<th>job id</th>\n'
        s += '<th>submitted</th>\n'
        s += '</tr>\n'
        s += '</thead>\n'
        s += '<tbody>\n'

        for row_i in xrange(len(job_files)):
            s += '<tr id="$row_i}">\n'
            s += '<td id="status" class="%s"></td>\n' % (job_files[row_i][2])
            if job_files[row_i][2] == 'done':
                s += '<td>%s</td>\n' % (job_files[row_i][0])
            else:
                s += '<td><a href="%s">%s</a></td>\n' %\
                        (uri_details(job_files[row_i][0]), job_files[row_i][0])
            s += '<td>%s</td>\n' % (date_string(job_files[row_i][0]))
            s += '</tr>\n'
        s += '</tbody>\n'
        s += '</table>\n'
        return simplejson.dumps(dict(status_table=s))

    @cherrypy.expose
    def progress(self, cl_id):

        self.fetch_session_data()
        cherrypy.response.headers['Content-Type'] = 'application/json'

        progress_txt = self.project_manager.get_classifier_progress(cl_id)
        error_txt = self.project_manager.get_classifier_error(cl_id)
        finished = self.project_manager.get_classifier_finished(cl_id)

        return simplejson.dumps(
            dict(progress=progress_txt, error=error_txt, finished=finished))

    @cherrypy.expose
    def roc(self, cl_id):    
        
        self.fetch_session_data()
        pm = self.project_manager

        filetype = 'image/png'
        filepath = pm.get_roc_f(cl_id)

        # serve the file
        return serve_file(filepath, filetype, 'attachment')
