.. _command_line_tools:

==================
Command line tools
==================

SPiCE can also be used locally using the command line using Python package
spice_. This package contains a feature extraction (``featext``) module that
can be used for features calculation, a ``classification`` module to train
classifiers and a ``classify`` module to run a trained classifier on another
data set.

.. _spice: https://github.com/basvandenberg/spice

----------
featext.py
----------

For feature extraction, a project needs to be initialized first at a give
location (path). For example:

.. code-block:: python

    mkdir test_project
    cd test_project
    featext --root . --init

A directory protein_data_set has been created, which will contain all protein
sequence data. The directory feature_matrix_protein will contain all calculated
features in the form of a feature matrix.

Next the protein ids need to be added. These should be stored in a file that
contains exactly one (unique) protein id per line.

.. code-block:: python

    featext --root . --uniprot_ids path/to/my/ids_file.txt

The option is called uniprot_ids for historic reasons, but you can use any ids
you like. This naming will be adjusted in a following release. 

A protein_ids.txt file is now stored in the protein_data_set directory. The
next step is to add protein sequences, using a FASTA-file. This file should at
least contain a sequence for each id you just added to the project. Only these
sequences will be read and added to the projects protein data.

.. code-block:: python

    featext --root . --protein_seqeunce_data path/to/my/fasta_file.fsa

A protein.fsa file is now stored in the protein_data_set directory. This
sequence data can now be used for calculating features.

.. code-block:: python

    featext --root . --protein_features aac_1 dc_1

The protein_features options ``aac_1`` and ``dc_1`` are feature category ids
that indicate what features need to be calculated. More information about
feature ids can be found in the :ref:`feature_ids` section.

Protein labels can be set using a :ref:`labeling file`, which is required for
running classification jobs.

.. code-block:: python

    featext --root . --labels protein my_labeling path/to/my/labeling_file.txt

There are three parameters that should follow the ``--labels`` option. The
first should always be protein, the second is the name of your labeling (you
can choose any), and the third is the path to your labeling file.

-----------------
classification.py
-----------------

Classification jobs can be run using:

.. code-block:: python

    classification -f your_project_dir/feature_matrix_protein \
        -l labeling_name -c lda -n 10 -e roc_auc --classes low high \
        --features aac_1_A aac_1_C aac_1_D --standardize -o path/to/output_dir

The ``-f`` should point to the feature matrix directory within your project
dir. With the ``-l`` and ``--classes`` options you can indicate which labaling
to use, and within this labeling, which labels should be classified. The ``-c``
option indicates what classifier to use, the ``-n`` option holds the number of
CV-loops to use for performance assessment, the ``-e`` option holds the
evaluation score to use. The features to use for classification can be
indicating using the ``--features`` option. The ``-standardize`` option will
most often be used, this causes the feature matrix to be standardized. Finally,
the ``-o`` option points to the directory to which the results should be
written.

-----------
classify.py
-----------

Downloaded classification results contain, besides performance scores and used
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

