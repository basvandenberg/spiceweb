.. _features:

========
Features
========

Here we shortly introduce what features are. The first section introduces
sequence-based protein features and the second section explains how calculated
features form a feature matrix. Finally, the third section explains how SPiCE
uses ids for identifying features.

-------------------------------
Sequence-based protein features
-------------------------------

A sequence-based feature is basically a mapping from a sequence to a number.
For example, if we have a sequence::

    >test0
    AAAAABBBBBBBBBBCCCCC

Then we could calculate what the relative fraction of occurrence of ``A``'s in
this sequence is by taking the number of ``A``'s and dividing that number by
the total length of the sequence::

    fraction A:  5 / 20 = 0.25

This number can be used as a feature of the sequence ``test0``. Similarly, the
relative fraction of occurrences of the other letters can be calculated::

    fraction B: 10 / 20 = 0.5

    fraction C:  5 / 20 = 0.25

This way, we obtained two more sequence-based features for sequence ``test0``.

It would make sense to combine these three features into a *feature category*
which we could call the *letter composition*. This way, we can map a sequence
to a list of three values that captures some sequence property/characteristic.

Similarly, one could calculate these features for a protein's primary
structure, the amino acid sequence, by calculating the relative fraction of
occurrence of each amino acid in the protein sequence. This feature category
is called the *amino acid composition*. 

--------------
Feature matrix
--------------

When calculating features, a so called feature matrix is build. As an example,
let's consider the following set of sequences::

    >test0
    AAAAABBBBBBBBBBCCCCC

    >test1
    BCBCBCBCBC

    >test2
    AAAAAAAAAAAAAAAAAAAAAAAAAAAAAB

Calculating the *letter composition* for each of these sequences will result in
the following feature matrix::

    .       fraction A      fraction B      fraction C

    test0      0.25            0.50            0.25

    test1      0.00            0.50            0.50

    test2      0.97            0.03            0.00

In this matrix, each row gives the feature values of one sequence (also called
a feature vector), and each column is one feature.

.. _feature_ids:

-----------
Feature ids
-----------

SPiCE assigns an id to each feature it calculates. This id is composed of three
parts: the *feature category id*, *parameter settings*, and *feature id*. These
three components are separated by an underscore character (_). For feature
categories that do not require parameters to be set, the parameter settings
component is left out.

A feature of the *amino acid composition* could have the following id::
    
    aac_1_F1

The first part,  ``aac``, is the id of the amino acid composition category.

The second part, ``1``, specifies a parameter that sets number of segments in
which the sequence should be split before returning the amino acid composition
of each of the segments. Since this value is one, the sequence will not be
split and the amino acid composition of the full sequence will be returned.

Finally, the third part, ``F1`` identifies the feature within the feature
category. In this case it indicates that this feature is the relative frequency
of occurrence of phenylalanine (F) in the first (and this case only) segment.

Multiple parameters can be specified, in which case they are separated using a
dash (``-``)::

    ac_moran-gg-20_gg4

For this example, the first part, ``ac``, is the id of the *autocorrelation*
feature category.

The second part ``moran-gg-20`` specifies the three parameters that can be
set for the calculation of the feature category. In this case ``moran`` is type
of autocorrelation function, ``gg`` indicates that the Georgiev amino acid
scales are used, and ``20`` is the lag parameter.

The third part ``gg4`` indicates that this is the feature value for the
4th amino acid scale in the set of Georgiev scales.

^^^^^^^^^^^^^^^^^^^^
Feature category ids
^^^^^^^^^^^^^^^^^^^^

The following table lists the feature category ids as used in SPiCE.

+------------+----------------------------------------------------------------+
| id         | Feature category                                               |
+============+================================================================+
| aac        | Amino acid composition                                         |
+------------+----------------------------------------------------------------+
| dc         | Dipeptide composition                                          |
+------------+----------------------------------------------------------------+
| teraac     | Terminal end amino acid counts                                 |
+------------+----------------------------------------------------------------+
| ssc        | Secondary structure composition                                |
+------------+----------------------------------------------------------------+
| ssaac      | Per secondary struct. class amino acid composition             |
+------------+----------------------------------------------------------------+
| sac        | Solvent accessibility composition                              |
+------------+----------------------------------------------------------------+
| saaac      | Per solvent accessibility class amino acid composition         |
+------------+----------------------------------------------------------------+
| cc         | Codon composition                                              |
+------------+----------------------------------------------------------------+
| cu         | Codon usage                                                    |
+------------+----------------------------------------------------------------+
| len        | Protein length                                                 |
+------------+----------------------------------------------------------------+
| ctd        | Property composition/transition/distribution                   |
+------------+----------------------------------------------------------------+
| sigavg     | Property signal average                                        |
+------------+----------------------------------------------------------------+
| sigpeak    | Property signal peak areas                                     |
+------------+----------------------------------------------------------------+
| ac         | Autocorrelation                                                |
+------------+----------------------------------------------------------------+
| paac1      | Pseudo amino acid composition type I                           |
+------------+----------------------------------------------------------------+
| paac2      | Pseudo amino acid composition type II                          |
+------------+----------------------------------------------------------------+
| qso        | Quasi sequence order descriptors                               |
+------------+----------------------------------------------------------------+

