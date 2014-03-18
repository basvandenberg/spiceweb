.. _feature_data_sources:

====================
Feature data sources
====================

This chapter introduces some data sources and basic concepts that are used for
the calculation of several features.

.. _amino_acid_scales:
-----------------
Amino acid scales
-----------------

Amino acid scales are mappings from amino acids to property values and are used
for the calculation of some feature categories. An often used example is the
Kyte & Doolittle [1] hydropathicity scale in which the values indicates how
hydrophobic/hydrophilic amino acids are::

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
collected in the AAIndex_ data base [2], with version9.1_ containing 544 amino
acid scales. 

Since many of these amino acid scales are highly correlated, multiple
efforts have been done (using PCA or similar techniques) to capture the data of
all the scales into a limited set of uncorrelated scales. 

.. _AAIndex: http://www.genome.jp/aaindex
.. _version9.1: http://www.genome.jp/aaindex/AAindex/list_of_indices

A. Georgiev [3] used Varimax to identify 19 uncorrelated scales that show good
correlation with published scales, this in order to retain interpretability.
This set of 19 scales, and all the separate scales in the AAIndex_ data base
are available for calculation of the signal mean, signal peaks area, and
autocorrelation features.

The scales are always standardized to mean 0.0 and standard deviation 1.0
before they are used for feature calculation.

Five amino acid scales, as provided on the PseAAC webserver [4], are available
for the pseudo amino acid composition features.


-------------------
Amino acid matrices
-------------------

An amino acid distance matrix is used for to calculate the quasi-sequence-order
descriptors. This is a 20 x 20 matrix that defines distances between all amino
acids. The Schneider-Wrede amino acid distance matrix is used for the
quasi-distance-order calculation [5].

-------------------
Amino acid clusters
-------------------

The property composition/transition/distribution (CTD) feature maps protein
sequences to a reduced 3-letter property alphabet. The amino acids are therefor
clustered into three groups for different properties. The used property
clusters are extracted from the PROFEAT publication and given in the list
below.

+---------------------------------+----------------------+----------------------+----------------------+
| Property                        | Clusters A           | Cluster B            | Cluster C            |
+=================================+======================+======================+======================+
| Hydrophobicity                  | R K E D Q N          | G A S T P H Y        | C L V I M F W        |
+---------------------------------+----------------------+----------------------+----------------------+
| Normalized van der Waals volume | G A S C* T P D       | N V E Q I L          | M H K F R Y W        |
+---------------------------------+----------------------+----------------------+----------------------+
| Polarity                        | L I F W C M V Y      | P A T G S            | H Q R K N E D        |
+---------------------------------+----------------------+----------------------+----------------------+
| Polarizability                  | G A S D T            | C P N V E Q I L      | K M H F R Y W        |
+---------------------------------+----------------------+----------------------+----------------------+
| Charge                          | K R                  | ANCQGHILMFPSTWYV     | D E                  |
+---------------------------------+----------------------+----------------------+----------------------+
| Secondary structure             | E A L M Q K R H      | V I Y C W F T        | G N P S D            |
+---------------------------------+----------------------+----------------------+----------------------+
| Solvent accessibility           | A L F C G I V W      | R** K Q E N D        | M P S T H Y          |
+---------------------------------+----------------------+----------------------+----------------------+

.. [*] Added compared to original table in [6]
.. [*] Changed from P to R compared to original table in [6]

^^^^^^^^^^
References
^^^^^^^^^^

[1] J. Kyte and Russell F Doolittle. A simple method for displaying the hydropathic character of a protein. Journal of Molecular Biology, 157(1):105–132, 1982.

[2] S. Kawashima, P. Pokarowski, M. Pokarowska, A. Kolinski, T. Katayama, and M. Kanehisa. AAindex: amino acid index database, progress report 2008. Nucleic Acids Research, 36(suppl 1):D202–D205, 2008.

[3] A.G. Georgiev. Interpretable numerical descriptors of amino acid space. Journal of Computational Biology, 16(5):703–723, 2009.

[4] H.B. Shen and K.C. Chou. PseAAC: a flexible web server for generating various kinds of protein pseudo amino acid composition. Analytical Biochemistry, 373(2):386–388, 2008.

[5] G. Schneider and P. Wrede. The rational design of amino acid sequences by artificial neural networks and simulated molecular evolution: de novo design of an idealized leader peptidase cleavage site. Biophysical Journal, 66(2):335–344, 1994.

[6] Ze-Rong Li, Hong Huang Lin, LY Han, L Jiang, X Chen, and Yu Zong Chen. PROFEAT: a web server for computing structural and physicochemical features of proteins and peptides from amino acid sequence. Nucleic Acids Research, 34(suppl 2):W32–W37, 2006.
