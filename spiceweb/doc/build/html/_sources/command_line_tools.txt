.. _command_line_tools:

==================
Command line tools
==================

SPiCE can also be used locally using the command line. 

----------
featext.py
----------

-----------------
classification.py
-----------------

-----------
classify.py
-----------


Besides result scores and settings, the zip-file will contain a trained
Scikit-learn classifier ``classifier.joblib.pkl`` which is pickled using the
``joblib`` module which is offered as part of the ``scikit-learn`` package.

Loading and running this classifier could be done with a python script like the
following:

.. code-block:: python

    from sklearn.externals import joblib
    clf = joblib.load('path/to/classifier.joblib.pkl')

    '''
    data = load your data here, should be a numpy matrix with the features that
           where used to train the classifier as columns. 
    '''

    # prediction class labels on data set
    pred = clf.predict(data)

    # obtain class probabilities (if possible)
    if(hasattr(clf, 'predict_proba')):
        proba = clf.predict_proba(data)
        # only works for 2-class classification!
        proba = proba[:, 1]

    # obtain decision function output
    if(hasattr(clf, 'decision_function')):
        decision = clf.decision_function(data)

Our ``featext`` and ``featmat`` module that are part of the ``spice`` package
could be used to calculate the features and obtain the feature matrix ``data``
that is required to run the classification.
