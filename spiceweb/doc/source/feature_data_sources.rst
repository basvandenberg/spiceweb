.. _feature_data_sources:

====================
Feature data sources
====================

-----------------
Amino acid scales
-----------------

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

-------------------
Amino acid matrices
-------------------

-------------------
Amino acid clusters
-------------------
