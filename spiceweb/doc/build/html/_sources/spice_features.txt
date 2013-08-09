.. _spice_features:

==============
SPiCE features
==============

Once you have initiated a new project with a set of protein sequences, you can
use the *Calculate* button under the  *Features* tab to calculate a range of
sequence-based features.

.. image:: img/featcalc0.png
   :width: 550px
   :align: center

The following sections will bescribe the different feature categories that are
offered by the SPiCE website. Some of these features were used in our previous
research :cite:`vandenberg2010`, :cite:`vandenberg2012`. The rest of the
features are based on those offered by the PROFEAT website :cite:`li2006`,
:cite:`rao2011`, who extracted their features from different sequence-based
studies.



----------------------
Amino acid composition
----------------------

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



---------------------
Dipeptide composition
---------------------



---------------------------
Prime-side amino acid count
---------------------------

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



---------------
Sequence length
---------------

This category calculates only one feature, the length of the amino acid
sequence.



------------------------------------------------------
Property Composition / Transition / Distribution (CTD)
------------------------------------------------------

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



---------------
Autocorrelation
---------------

The autocorrelation feature is derived from :cite:`li2006`. 



--------------
Signal average
--------------

This feature uses an amino acid scale to tranform an amino acid into a
(smoothed) property profile (Fig.1A & Fig.1C) and uses the average value of the
resulting profile as feature value.

.. image:: img/featcalc3.png
   :width: 550px
   :align: center

Amino acid scales relate to different amino acid properties, such as
hydropathicity. The average value of such a scale therefore provides an
indication of the global hydropathicity of the protein.



-----------------
Signal peaks area
-----------------

The same as the previous feature, this feature uses an amino acid scale to
transform an amino acid sequence into a (smoothed) property profile / signal.
Instead of taking the average profile value, this feature calculates the area
under the profile curve under some given threshold (Fig.1C).

.. image:: img/featcalc4.png
   :width: 550px
   :align: center



-----------------------------
Pseudo amino acid composition
-----------------------------



--------------------------------
Quasi sequence-order descriptors
--------------------------------



-------------------------------
Secondary structure composition
-------------------------------



----------------------------------------------
Per secondary structure amino acid composition
----------------------------------------------



---------------------------------
Solvent accessibility composition
---------------------------------



------------------------------------------------------
Per solvent accessibility class amino acid composition
------------------------------------------------------



-----------------
Codon composition
-----------------



-----------
Codon usage
-----------



----------
References
----------

.. bibliography:: refs.bib
