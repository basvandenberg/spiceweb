.. _file_formats:

============
File Formats
============

This section explains about the different file formats used on the SPiCE
website.

----------
FASTA file
----------

FASTA files are used to store sequence data, such as a set of protein amino
acid sequences. 

In the FASTA file format that is used by SPiCE, each sequence should start with
a ``>`` character followed by the sequence id (*without a space in between*).
The sequence itself should be on the following lines::

    >YOR106W Syntaxin VAM3
    MSFFDIEAQSSKGNSQQEPQFSTNQKTKELSNLIETFAEQSRVLEKECTKIGSKRDSKELRYKIETELIP
    NCTSVRDKIESNILIHQNGKLSADFKNLKTKYQSLQQSYNQRKSLFPLKTPISPGTSKERKDIHPRTEAV
    RQDPESSYISIKVNEQSPLLHNEGQHQLQLQEEQEQQQQGLSQEELDFQTIIHQERSQQIGRIHTAVQEV
    NAIFHQLGSLVKEQGEQVTTIDENISHLHDNMQNANKQLTRADQHQRDRNKCGKVTLIIIIVVCMVVLLA
    VLS

In the example above ``YOR106W`` is the sequence id. The rest of this line
(``Syntaxin VAM3``) will be ignored. After encountering a sequence id, the
system will start reading the sequence on the following lines, until it
encounters an empty line, a new sequence id, or a line with a comment on it.

Comments are allowed in the FASTA files, but only in between the sequences.
Comments should start with a ``#`` character::

    # Some comments about the first sequence
    # Each comment line should start with a # character

    >YOR106W
    MSFFDIEAQSSKGNSQQEPQFSTNQKTKELSNLIETFAEQSRVLEKECTKIGSKRDSKELRYKIETELIP
    NCTSVRDKIESNILIHQNGKLSADFKNLKTKYQSLQQSYNQRKSLFPLKTPISPGTSKERKDIHPRTEAV
    RQDPESSYISIKVNEQSPLLHNEGQHQLQLQEEQEQQQQGLSQEELDFQTIIHQERSQQIGRIHTAVQEV
    NAIFHQLGSLVKEQGEQVTTIDENISHLHDNMQNANKQLTRADQHQRDRNKCGKVTLIIIIVVCMVVLLA
    VLS

    # Some comment about the next sequence

    >YPR061C
    MLHHKFVYPFLFKWHLSCVEKCPPQITFIAKYATANDKNGNRKLTIRDEQWPELADPTPYDIFGIPKAGS
    GNPKLDKKSLKKKYHRYVKLYHPDHSDNIQIFSSEKVTNSDSKSPLLLTSSEKLHRFKVISQAYDILCDP
    KKKIVYDTTRQGWTTSYSPRSNVNTENYQYAGSYGYHSNAQYEYWNAGTWEDANSMKNERIQENINPWTV
    IGIICGLAICIEGTALLAKIQESLSKAEFTHDESGLHLIQSYTNYGLDTDKFSRLRRFLWFRTWGLYKSK
    EDLDREAKINEEMIRKLKAAK

The FASTA file should meet the following requirements:

- Duplicate sequence ids are not allowed. Each sequence corresponds to an
  object in the feature matrix and each object must have a unique id.
- Empty sequences are not allowed.
- Sequences must be upper case.

SPiCE uses FASTA files for four types of sequences: amino acid sequences,
nucleotide sequences, secondary structure sequences, and solvent accessibility
sequences. Details per sequence type are discussed in the following
subsections.

^^^^^^^^^^^^^^^^^^^^
Amino acid sequences
^^^^^^^^^^^^^^^^^^^^

For protein (amino acid) sequences the following letters are allowed::

    unambiguous amino acids: A R N D C E Q G H I L K M F P S T W Y V
    ambiguous amino acids:   B J Z X
    special amino acids:     U O
    terminal character:      *

**Note:** Only the unambiguous amino acids are considered for most calculated
features, the other characters are ignored in this case.

^^^^^^^^^^^^^^^^^^^^
Nucleotide sequences
^^^^^^^^^^^^^^^^^^^^

For ORF (nucleotide) sequences the following letters are allowed::

    unambiguous nucleotides: T C A G
    ambiguous nucleotides:   M R W S Y K V H D B N

**Note:** Only the unambiguous nucleotides are considered for most calculated
features, the other characters are ignored in this case.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Secondary structure sequences
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For secondary structure sequences the following letters are allowed, which are
the same as used by secondary structure prediction method PSIPRED::

    helix:       H
    strand:      E
    random coil: R

**Note** A protein's secondary structure sequence should have the same length
as its amino acid sequence. However, SPiCE does not check for this when
uploading a FASTA file with secondary structures!

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Solvent accessibility sequences
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For secondary structure sequences the following letters are allowed::

    exposed: E
    buried:  B

**Note** A protein's solvent accessibility sequence should have the same length
as its amino acid sequence. However, SPiCE does not check for this when
uploading a FASTA file with solvent accessibility sequences!


.. _labeling_file:

-------------
Labeling file
-------------

After initiating a project with a set of protein sequences, one or more
labeling files can be uploaded to subdivide the proteins into different
classes.

The first line of a labeling file contains the *class names* and the following
lines contain the *labeled proteins*::

    low high
    YOR093C 0
    YJL084C 0
    YKR031C 0
    YGR277C 1
    YGR281W 1
    YNR007C 1

In the example above there are two classes: ``low`` and ``high``. The class
names should be separated by a tab or a space.

Each of the following lines contains a protein id (which should be the same as
the ones used in the FASTA file) and its label, which is the class name index.
In this example, label ``0`` refers to ``low``, and label ``1`` refers to
``high``. The sequence id and label should be separated by a tab or a space.

The labeling file should meet the following requirements:

- There must be at least one label for each class name. The following is for
  example not allowed, because none of the proteins has label 2 (middle) ::

    low high middle
    YOR093C 0
    YJL084C 0
    YKR031C 0
    YGR277C 1
    YGR281W 1
    YNR007C 1

- There must be exactly one label for each protein in your data set. So there
  must be a label for each sequence in the FASTA file that was used to initiate
  the project.

- It is allowed to have labels for proteins that are not in your data set. If,
  for example, your data set contains three proteins: ``YOR093C``, ``YJL084C``,
  and ``YNR007C``, then the following labeling file would be allowed, because
  it contains, amongst others, a label for all three proteins::

    low high
    YOR093C 0
    YJL084C 0
    YKR031C 0
    YGR277C 1
    YGR281W 1
    YNR007C 1

As a final example, the following labeling file shows a labeling in which the
proteins are subdivided into 4 classes::

    peroxisome  cytoplasm   golgi_apparatus microsome
    Q86WA8  0
    Q9UJ83  0
    O75381  0
    Q96M11  1
    O14713  1
    P01040  1
    Q9H8Y8  2
    Q8N3G9  2
    Q6ZMB0  2
    P08686  3
    Q16678  3
    P56279  3

**NOTE:** SPiCE does not support assigning proteins to multiple classes
within the same labeling.

-------------------
Feature matrix file
-------------------

Feature matrices are stored as text file in a format that is used by the python
module numpy_. This module is used for reading and writing feature matrices
using the loadtxt_ and savetxt_ functions. An example feature matrix with 4
features and 10 objects (proteins) is given below, in which each row gives the
feature values of one protein, each column gives all the values of one
feature::

    3.7621e-02 3.9442e-02 7.1602e-02 4.7937e-02
    4.3977e-02 4.5889e-02 8.9866e-02 5.6405e-02
    4.2781e-02 6.3577e-02 7.4866e-02 6.3577e-02
    4.0064e-02 4.3803e-02 7.6923e-02 6.0363e-02
    3.6904e-02 3.6904e-02 1.0531e-01 5.4005e-02
    4.4481e-02 4.7776e-02 5.6013e-02 4.6129e-02
    3.4279e-02 4.3735e-02 7.8014e-02 4.2553e-02
    5.9087e-02 1.4324e-02 5.9087e-02 4.9239e-02
    4.1727e-02 4.7482e-02 6.4748e-02 5.8993e-02
    2.8269e-02 4.2403e-02 6.3604e-02 7.1849e-02


.. _numpy: http://www.numpy.org/
.. _loadtxt: http://docs.scipy.org/doc/numpy/reference/generated/numpy.loadtxt.html
.. _savetxt: http://docs.scipy.org/doc/numpy/reference/generated/numpy.savetxt.html

**NOTE:** In this case, the string format ``%.4e`` was used to store the
feature values. The default format used by the savetxt_ function is
``%.18e``.

For annotating features and proteins, SPiCE uses two additional files. The
first contains protein ids that indicate the order of the proteins (rows) in
the feature matrix. This file contains one id per line. For the given example
feature matrix, such a file could be::

    YOR093C
    YJL084C
    YKR031C
    YLR024C
    YBL063W
    YJL100W
    YNL126W
    YNR067C
    YLR035C
    YLR057W

Similarly, the second file stores the ids of the features (columns) in the
feature matrix, for example::

    aac_1_A1
    aac_1_R1
    aac_1_N1
    aac_1_D1

**NOTE:** See :ref:`feature_ids` for more information about the used feature
ids.

For uploading your own features (`spice/app/features/upload`), both the feature
matrix file (in the described numpy format) and the file with protein ids need
to be provided. Feature values must be provided for all the proteins in your
project, which means that all ids in your FASTA file must also be in the
protein ids file.  Feature ids will automatically be assigned by the SPiCE
system.

The feature matrix with all calculated features can also be downloaded using
the ``Download feature matrix`` button on the `spice/app/features/list` page.
