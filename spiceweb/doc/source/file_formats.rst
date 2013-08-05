.. _file_formats:

============
File Formats
============

This section explains about the different file formats used on the SPiCE
website.

------------------------------
Protein sequences (FASTA file)
------------------------------

When creating a new project, a set of protein sequences should be uploaded as a
FASTA file. In this file format, each sequence should start with a ``>``
character followed by the sequence id (*without a space in between*). The
sequence itself should be on the following lines::

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

- Duplicate sequence ids are not allowed. Each sequence will become an object
  in the feature matrix and each object must have a unique id.
- Empty sequences are not allowed.
- Sequences must be upper case.
- For protein (amino acid) sequences the following letters are allowed::

    unambiguous amino acids: ARNDCEQGHILKMFPSTWYV
    ambiguous amino acids: BJZX
    special amino acids: UO
    terminal character: *

- For ORF (nucleotide) sequences the following letters are allowed::

    unambiguous nucleotides: TCAG
    ambiguous nucleotides: MRWSYKVHDBN

**Note:** Only the unambiguous amino acids and unambiguous nucleotides are
considered for most calculated features, the other characters are ignored in
this case.

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

Besides calculating the features that are offered by SPiCE, you can also upload
your own features in the form of a feature matrix. The feature matrix should be
in text format with the features as columns and the objects (proteins) as rows.

The python module numpy_ reads the matrix using the loadtxt_ function with
default parameters.  If you use python to generate your feature matrix, you can
use the numpy savetxt_ function to save your feature matrix in text format.

.. _numpy: http://www.numpy.org/
.. _loadtxt: http://docs.scipy.org/doc/numpy/reference/generated/numpy.loadtxt.html
.. _savetxt: http://docs.scipy.org/doc/numpy/reference/generated/numpy.savetxt.html

A feature matrix with 4 features and 10 objects (proteins) is given below::

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

Each row gives the feature values of one protein, each column gives all the
values of one feature.

**NOTE:** In this case, the string format ``%.4e`` was used to store the
feature values. The default format used by the savetxt_ function is
``%.18e``.

An additional file with protein ids should be uploaded to indicate the order of
the proteins (rows) in the feature matrix. The file with protein ids should
contain one id per line::

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

Feature values must be provided for all the proteins in your project, which
means that all ids in your FASTA file must also be in the protein ids file. The
number of rows in the feature matrix should also correspond to the number of
proteins in your data set.
