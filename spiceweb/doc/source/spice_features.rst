.. _spice_features:

==============
SPiCE features
==============

Once you have initiated a new project with a set of protein sequences, you can
use the *Calculate* button under the  *Features* tab to calculate a range of
sequence-based features.

.. image:: img/featcalc0.png
   :width: 640px
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

The amino acids composition calculates the frequency of occurance for each
of the 20 amino acids in a protein sequence.

.. image:: img/featcalc1.png
   :width: 640px
   :align: center

Having 20 amino acids, this will result in 20 features. Any other than the 20
unambiguous amino acid letters will be ignored.

To illustrate this, consider the following (unrealistic) protein sequence,
which contains two occurences of each amino acid in which each amino acid
obtains the value 0.05::

    >>aac_test
    MMAARRNNDDCCEEQQGGHHIILLKKFFPPSSTTWWYYVV

will result in the following feature vector::

    .              A1          R1       ...        V1
    
    aac_test      0.05        0.05      ...       0.05

As a parameter, users can specify in how many (equal sized) segments a protein
should be divided, before calculating the amino acid composition of each
segmente separately. The number of features will therefore be the number of
segments times 20.

With 2 as number of segments parameter, the sequence will be split in two::

    segment 1              segment2
    MMAARRNNDDCCEEQQGGHH | IILLKKFFPPSSTTWWYYVV

The amino acid composition of both segments is calculated which together
results in a feature vector with 40 features::

    .              A1   ...   V1   ...   A2   ...   V2

    aac_test      0.10  ...  0.00  ...  0.00  ...  0.10



---------------------
Dipeptide composition
---------------------

Similar to the amino acid composition, the dipeptide composition calculates the
frequency of occurance of each of the 400 possible dipeptides in a protein
sequence.

.. image:: img/feat_dipep.png
   :width: 640px
   :align: center

Having 400 possible amino acid pairs (dipeptides), this will result in 400
features. Dipeptides containing any other than the 20 unambiguous amino acid
letters will be ignored.

As a parameter, users can specify in how many (equal sized) segments a protein
should be divided, before calculating the dipeptide composition of each
segmente separately. To limit the number of features and to avoid too sparse
feature matrices, the maximal number of segments is set to 2.

For an example sequence that contains 10 dipeptides::

    >>dc_test
    MAAARRNNDDC

The resulting feature vector wil be::

    .           AA      AR   ...   AV      RA      RR         VV
    
    dc_test    0.20    0.10  ...  0.00    0.00    0.10  ...  0.00



---------------------------
Prime-side amino acid count
---------------------------

This feature category returns the amino acid counts of a fixed length sequence
end, either using the 5` or the 3` side.

.. image:: img/featcalc2.png
   :width: 640px
   :align: center

For example sequence::

    >>psaac_test
    MMAARRNNDDCCEEQQGGHHIILLKKFFPPSSTTWWYYVV

the 5' amino acid count for length 10 will result in the following feature
vector::

    .           A   R   N   D   C   E   Q   G   H  ...  M  ...  V

    psaac_test  2   2   2   2   0   0   0   0   0  ...  2  ...  0

in which the counts for M, A, R, N, and D are set to 2, while the remaining 15
features are set to 0.



---------------
Sequence length
---------------

This category calculates only one feature, the length of the amino acid
sequence.

.. image:: img/feat_len.png
   :width: 640px
   :align: center

The example sequence::

    >>>len_test
    MMAARRNNDD

Will result in the following feature vector::

    .           len

    len_test     10



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
   :width: 640px
   :align: center

Amino acid scales relate to different amino acid properties, such as
hydropathicity. The average value of such a scale therefore provides an
indication of the global hydropathicity of the protein.



-----------------
Signal peaks area
-----------------

The same as the previous feature, this feature uses an amino acid scale to
transform an amino acid sequence into a (smoothed) property profile / signal
(Fig.1A & Fig.1C). Instead of taking the average profile value, this feature
calculates the area under the profile curve under some given threshold
(Fig.1C).

.. image:: img/featcalc4.png
   :width: 640px
   :align: center



------------------------------------
Pseudo amino acid composition type 1
------------------------------------

The type 1 pseudo amino acid composition calculates 20 + lambda features as
introduced in :cite:`chou2001` and provides the same calculation as provided on
the PseAAC webserver :cite:`shen2008`. 

.. image:: img/feat_pseaac1.png
   :width: 640px
   :align: center



------------------------------------
Pseudo amino acid composition type 2
------------------------------------

The type 2 pseudo amino acid composition calculates 20 + lambda features as
introduced in :cite:`chou2005` and provides the same calculation as provided on
the PseAAC webserver :cite:`shen2008`. 

.. image:: img/feat_pseaac2.png
   :width: 640px
   :align: center



--------------------------------
Quasi sequence-order descriptors
--------------------------------

.. image:: img/feat_qso.png
   :width: 640px
   :align: center


-------------------------------
Secondary structure composition
-------------------------------

.. image:: img/feat_ssc.png
   :width: 640px
   :align: center


----------------------------------------------
Per secondary structure amino acid composition
----------------------------------------------

.. image:: img/feat_ssaac.png
   :width: 640px
   :align: center


---------------------------------
Solvent accessibility composition
---------------------------------

.. image:: img/feat_sac.png
   :width: 640px
   :align: center


------------------------------------------------------
Per solvent accessibility class amino acid composition
------------------------------------------------------

.. image:: img/feat_saaac.png
   :width: 640px
   :align: center


-----------------
Codon composition
-----------------

This feature category calculates the frequence of occurancy of each of the 64
codons in a protein's ORF sequence.

.. image:: img/feat_cc.png
   :width: 640px
   :align: center



-----------
Codon usage
-----------

This feature category calculates the relative usage for each codon per amino
acid in the protein sequence.

.. image:: img/feat_cu.png
   :width: 640px
   :align: center

To illustrate this, consider the following protein amino acid sequence,
consisting of only alanines, and the
corresponding ORF sequence::

    amino acid:    A   A   A   A   A   A   A   A   A   A
           ORF:   GCC GCC GCC GCC GCC GCA GCA GCA GCT GCT

Since four different codons encode for alanine: GCT, GCC, GCA, and GCG, the
example ORF sequence can only consist of these 4 codons. The codon usage
feature calculates the relative frequency of occurance of these four codons,
resulting in the following 4 feature values::

    .       GCT    GCC    GCA    GCG
            0.2    0.5    0.3    0.0

All other codon values will be set to 0.0 in this example. In a real sequence,
containing all 20 amino acids, this proredure is done for each amino acid,
resulting in a total of 64 features, one per codon. 

TODO: special cases methionine and stop codons.

----------
References
----------

.. bibliography:: refs.bib
