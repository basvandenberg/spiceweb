========
Features
========

Once you have initiated a new project with a set of protein sequences, you can
use the *Calculate* button under the  *Features* tab to calculate a range of
sequence-based features.

.. image:: img/featcalc0.png
   :width: 550px
   :align: center

------------
Introduction
------------

Before explaining about the available feature categories on the SPiCE website,
some topics will be introduced first. The first two sub-sections shortly
introduce what sequence-based features are and how they can be used to form a
feature matrix. Then the use of so called amino acid scales is introduced,
which are used for the calculation of some of the feature categories. Finally,
the last sub-section explains about the use of feature ids in the SPiCE system.

^^^^^^^^^^^^^^^^^^^^^^^
Sequence-based Features
^^^^^^^^^^^^^^^^^^^^^^^

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

^^^^^^^^^^^^^^
Feature matrix
^^^^^^^^^^^^^^

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

^^^^^^^^^^^^^^^^^
Amino acid scales
^^^^^^^^^^^^^^^^^

Amino acid scales are mappings from amino acids to property values and are used
for the calculation of some feature categories. An often used example is the
Kyte & Doolittle :cite:`kyte1982` hydropathicity scale in which the values
indicates how hydrophobic/hydrophilic amino acids are::

    Ala:  1.800  
    Arg: -4.500  
    Asn: -3.500  
    Asp: -3.500  
    Cys:  2.500  
    Gln: -3.500  
    Glu: -3.500  
    Gly: -0.400  
    His: -3.200  
    Ile:  4.500  
    Leu:  3.800  
    Lys: -3.900  
    Met:  1.900  
    Phe:  2.800  
    Pro: -1.600  
    Ser: -0.800  
    Thr: -0.700  
    Trp: -0.900  
    Tyr: -1.300  
    Val:  4.200  

Mapping a protein sequence to the corresponding hydrophaticity values results
in a raw hydropathicity profile (Figure 1A). A convolution filter (Figure 1B)
can be used to smooth the profile (Figure 1C), thereby capturing the
hydropathicity over a sequence window. Both raw and smoothed profiles are used
for several feature categories.

.. figure:: img/hydro_signals.png
    :width: 650px
    :align: left
    :alt: test

    **Figure 1: A)** Raw hydropathicity profile. **B)** Convolution filter
    used to smooth the raw profile. **C)** Smoothed hydropathicity profile. The
    thresholds can be used to determine areas under the curve above a certain
    threshold, in order to capture the occurence of profile peaks.

There are many amino acid scales described in literature, most of which are
collected in the AAIndex_ data base, with version9.1_ containing 544 amino acid
scales. 

Since many of these amino acid scales are highly correlated, multiple
efforts have been done (using PCA or similar techniques) to capture the data of
all the scales into a limited set of uncorrelated scales. 

.. _AAIndex: http://www.genome.jp/aaindex
.. _version9.1: http://www.genome.jp/aaindex/AAindex/list_of_indices

A. Georgiev :cite:`georgiev2009` used Varimax to identify 19 uncorrelated
scales that show good correlation with published scales, this in order to
retain interpretability. This set of 19 scales, and all the separate scales in
the AAIndex_ data base are available for feature calculation on the SPiCE
website.

^^^^^^^^^^^
Feature ids
^^^^^^^^^^^

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



------------------------
SPiCE feature categeries
------------------------

The following sections will bescribe the different feature categories that are
offered by the SPiCE website. Some of these features were used in our previous
research :cite:`vandenberg2010`, :cite:`vandenberg2012`. The rest of the
features are based on those offered by the PROFEAT website :cite:`li2006`,
:cite:`rao2011`, who extracted their features from different sequence-based
studies.



^^^^^^^^^^^^^^^^^^^^^^
Amino acid composition
^^^^^^^^^^^^^^^^^^^^^^

The same as in the example given in the introduction, the amino acids
composition calculates the fraction of each amino acid in a protein sequence.

.. image:: img/featcalc1.png
   :width: 550px
   :align: center

Having 20 amino acids, this will result in 20 features. If a sequence contains
any other than the 20 unambiguous amino acid letters will be ignored.

To illustrate this, consider the following (unrealistic) protein sequence,
which contains two occurences of each amino acid in which each amino acid
obtains the value 0.05::

    >>aac_test
    MMAARRNNDDCCEEQQGGHHIILLKKFFPPSSTTWWYYVV

will result in a amino acid feature vector::

    aac_1_A1    aac_1_R1    ...     aac_1_V1
    0.05        0.05        ...     0.05

As a parameter, users can specify in how many (equal sized) segments a protein
should be divided, before calculating the amino acid composition of each
segmente separately. The number of features will therefore be the number of
segments times 20.

With 2 as number of segments parameter, the sequence will be split in two::

    segment 1              segment2
    MMAARRNNDDCCEEQQGGHH | IILLKKFFPPSSTTWWYYVV

The amino acid composition of both segments is calculated which together
results in a feature vector with 40 features::

    aac_2_A1   ...     aac_2_V1    ...     aac_2_A2    aac_2_V2
    0.10       ...     0.00                0.0         0.10

^^^^^^^^^^^^^^^^^^^^^^^^^^^
Prime-side amino acid count
^^^^^^^^^^^^^^^^^^^^^^^^^^^

This feature category returns the amino acid counts of a fixed length sequence
end, either using the 5` or the 3` side.

.. image:: img/featcalc2.png
   :width: 550px
   :align: center

To illustrate this, consider the following (unrealistic) protein sequence,

    >>aac_test
    MMAARRNNDDCCEEQQGGHHIILLKKFFPPSSTTWWYYVV

The 5' amino acid count for length 10 will result in this feature vector in
which the counts for M, A, R, N, and D are set to 2, while the remaining 15
features are set to 0.

^^^^^^^^^^^^^^
Signal average
^^^^^^^^^^^^^^

This feature uses an amino acid scale to tranform an amino acid into a
(smoothed) property profile (Fig.1A & Fig.1C) and uses the average value of the
resulting profile as feature value.

.. image:: img/featcalc3.png
   :width: 550px
   :align: center

Amino acid scales relate to different amino acid properties, such as
hydropathicity. The average value of such a scale therefore provides an
indication of the global hydropathicity of the protein.

^^^^^^^^^^^^^^^^^
Signal peaks area
^^^^^^^^^^^^^^^^^

The same as the previous feature, this feature uses an amino acid scale to
transform an amino acid sequence into a (smoothed) property profile / signal.
Instead of taking the average profile value, this feature calculates the area
under the profile curve under some given threshold (Fig.1C).

.. image:: img/featcalc4.png
   :width: 550px
   align: center

^^^^^^^^^^^^^^^
Autocorrelation
^^^^^^^^^^^^^^^

The autocorrelation feature is derived from :cite:`li2006`. 

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Property Composition / Transition / Distribution (CTD)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The Composition, Transition, Distribution feature is derived from
:cite:`li2006`. 

For these features, the protein sequence is first translated
from the 20 letter amino acid alphabet to a 3 letter alphabet, in which the 20
amino acids are devided over the three letters based on some property. The
properties and corresponding subdivision of the amino acids are::

    property                letter A            letter B            letter C
    ---------------------------------------------------------------------------
    hydrophobicity          RKEDQN              GASTPHY             CLVIMFW

    normalized v.d. Waal    GACSTPD             NVEQIL              MHKFRYW

    polarity                LIFWCMVY            PATGS               HQRKNED

    polarizability          GASDT               CPNVEQIL            KMHFRYW

    charge                  KR                  ANCQGHILMFPSTWYV    DE

    secondary structure     EALMQKRH            VIYCWFT             GNPSD

    solvent accessibility   ALFCGIVW            PKQEND              MRSTHY

To illustrate this, using charge as property, an amino acid sequence will be
mapped to a three letter charge alphabet as follows::

    MPMDQSISSPLFPMEKDIDIPLDATPLAQSSSLQLFIHLAEPVVFLQGFDPQKTEYPSVVLRGCLVVRIL
       |          |:| |   |                 |        |  : |      :     :  
    BBBCBBBBBBBBBBCACBCBBBCBBBBBBBBBBBBBBBBBCBBBBBBBBCBBABCBBBBBBABBBBBABB

For the mapped sequence, three types of features are calculated. First the
letter composition::

    composition A:  4 / 70 = 0.057
    composition B: 58 / 70 = 0.114
    composition C:  8 / 70 = 0.829

Secondly the letter relative transition occurances, which is the number of
transitions from A to B and from B to A divided by the sequence length - 1::

    transition A-B B-A:  6 / 69 = 0.087
    transition A-C C-A:  2 / 69 = 0.029
    transition B-C C-B: 14 / 69 = 0.203

Finally the distributation of the letters over the sequence is captured by 5
features per letter. If we consider letter C, the first feature is the
(procentual) sequence position where the first occurance of the C is::

    distribution C first:  4 / 70 = 0.057

The following 4 features are the (procentual) sequence positions where
respectively 25%, 50%, 75%, and 100% of the letters C is on and before this
position::

    distribution C  25%: 15/70 = 0.214
    distribution C  50%: 19/70 = 0.271
    distribution C  75%: 41/70 = 0.586
    distribution C 100%: 55/70 = 0.786

The same five features are calculated for letters A and B as well. In total the
CTD feature category provides 3 + 3 + 5 x 3 = 21 features for a given property.

^^^^^^^^^^^^^^
Protein length
^^^^^^^^^^^^^^

This category calculates only one feature, the length of the protein sequence.

----------
References
----------

.. bibliography:: refs.bib
