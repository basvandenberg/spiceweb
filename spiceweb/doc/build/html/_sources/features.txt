.. _features:

========
Features
========

Before explaining about the features that can be calculated on the SPiCE website,
some topics will be introduced. The first two sub-sections shortly
introduce what sequence-based features are and how they can be used to form a
feature matrix. Then the use of so called amino acid scales is introduced,
which are used for the calculation of some of the feature categories. Finally,
the last sub-section explains about the use of feature ids in the SPiCE system.

-----------------------
Sequence-based Features
-----------------------

A sequence-based feature is basically a mapping from a sequence to a number.
For example, if we have a sequence::

    >test0
    AAAAABBBBBBBBBBCCCCC

Then we could calcalate what the fraction of ``A``'s in this sequence is by
taking the number of ``A``'s and divide that number by the total length of the
sequence::

    fraction A:  5 / 20 = 0.25

This number can be used as a feature of the sequence ``test0``. Similarly, the
fraction of the other letters can be calculated::

    fraction B: 10 / 20 = 0.5

    fraction C:  5 / 20 = 0.25

This way, we obtained two more sequence-based features for sequence ``test0``.

It would make sense to combine these three features into a *feature category*
which we could call the *letter composition*. This way, we can map a sequence
to a list of three values that captures some sequence property /
charecteristic.

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
a feature vector), and each column gives the feature values of one feature.

-----------
Feature ids
-----------

Within the SPiCE system, each feature obtains an id that is build out of three
components: the feature category id, parameter settings, and feature id. These
three components are separated by an underscore character (_). For feature
categories for which no parameters can be set, the parameter settings component
is left out.

As an example, let's consider the feature id::

    ac_moran-gg-20_gg4

The first component ``ac`` is the id of the *autocorrelation* feature
category.

The second component ``moran-gg-20`` is a ``-`` separated list of feature
category parameters. In this case ``moran`` is the used type of autocorrelation
function, ``gg`` indicates that the Georgiev amino acid scales are used, and
``20`` is the used lag parameter.

The third component ``gg4`` indicates that this is the feature value for the
4th amino acid scale in the set of Georgiev scales.



