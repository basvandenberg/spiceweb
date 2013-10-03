.. _command_line_tools:

==================
Command line tools
==================

SPiCE can also be used locally using the command line using Python package
``_spice``. This package contains a feature extraction (``featext``) module that
can be used for features calculation, a ``classification`` module to train
classifiers and a ``classify`` module to test a trained classifier.

.. _spice: https://github.com/basvandenberg/spice

----------
featext.py
----------

-----------------
classification.py
-----------------

-----------
classify.py
-----------

Downloaded classification results contain, desides performance scores and used
settings, a Scikit-learn classifier that was trained on the entire data set:
``classifier.joblib.pkl``. This file is pickled using the ``joblib`` module
which is offered as part of the ``scikit-learn`` package.

Loading and running this classifier could be done with a python script like the
following:

.. code-block:: python

    from sklearn.externals import joblib
    clf = joblib.load('path/to/classifier.joblib.pkl')

    '''
    data = use featext to calculate features for your proteins, this should
           be the same features as those used for training the classifier.
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

