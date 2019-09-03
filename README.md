<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**

- [Cigar Aligner](#cigar-aligner)
  - [Implementation](#implementation)
  - [Installation](#installation)
  - [Setup](#setup)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Cigar Aligner

[CIGAR] string decompression can be implemented to retrieve paired strand coordinates from a transcript read to a reference genome from SAM/BAM format.

__Included features__
* Automated data generation as a convenient executable within `setup.py`
* Retrieval of coordinates (or mapped coordinate ranges) under the following conditions:
    - Forward strand (5'➜3') and reversed strand orientation (3'➜5')
    - Inverted alignment (reference genome aligned to transcript read)
* Documentation across all features
* Unit testing to indicate input constraints and functionality of:
    - Data generation methods within `setup.py`
    - CIGAR array implementation
    - Algorithm functionality for alignment
    - Main task executation
    - Results output format

## Implementation
A CIGAR representation of SAM-formatted alignment can be decompressed to range elements and operations, respectively (i.e. `(11, 'M')` from `11M`). Coordinate operations in this exercise may either be read-consuming (M, I, S) or reference-consuming (M, D). Other operations exist in real-world CIGAR encoding. The read index start site begins at a known non-zero coordinate of the reference index. The CIGAR string may be reversed.

| Operation | Description |
| --------- | ----------- |
| M | Match or mismatch, index contains identical or different letters |
| I | Insertion, gap in query reference sequence |
| D | Deletion, gap in target read sequence |
| S | Segment of query sequence soft-clipped from alignment |

```python
import utils from Utils
cigar = '8M7D6M2I2M11D7M'

# Cigar in forward 5'->3' orientation
Utils(cigar, direction='F')._groups()
>>> [(8, 'M'), (7, 'D'), (6, 'M'), (2, 'I'), (2, 'M'), (11, 'D'), (7, 'M')]

# Cigar in reversed 3'->5' orientation
Utils(cigar, direction='R')._groups()
>>> [(7, 'M'), (11, 'D'), (2, 'M'), (2, 'I'), (6, 'M'), (7, 'D'), (8, 'M')]

# Read and references arrays created with a specified site
c = Utils(cigar, direction='F', start_site=3)
c.index('read')
>>> [0, 8, 0, 6, 2, 2, 0, 7]
c.index('reference')
>>> [3, 8, 7, 6, 0, 2, 11, 7]
```
[Prefix sums] allows for counting in [*O(n)* time complexity] and the storage of sums of contiguous elements in an array. For the purpose of this exercise, the input arrays contain the numeric range elements from either the read or reference indices encoded within the CIGAR grouping. Resulting arrays may be created using the `Map.prefix_sums(A)` class method. The arrays are stored in a tuple for optional inversion of the template. 

```python
# Read and references arrays (summed and stored)
read = [0, 0, 8, 8, 14, 16, 18, 18, 25]
reference = [0, 3, 11, 18, 24, 24, 26, 37, 44] 
inverted = (read, reference)[::-1]
```

The complimentary strand coordinate may be queried with a value less than the maximum of the template strand. Map conditions apply within the alignment function as the `read` and `reference` arrays are reversed or inverted. A single coordinate of a range of coordinates may be queried.

```python
from map import Map

m = Map(cf, direction='R', start_site=3, inverted=False)
m.align(14)
>>> 26

m.map_ranger(start=7, end=13)
>>> [(7, 10), (8, 22), (9, 23), (10, None), (11, None), (12, 24), (13, 25)]
```

__Orientation resource table__

| Type| Forward (5'➜3') | Reverse (3'➜5') |
|---------| --------------- | --------------- |
| CIGAR | 8M7D6M2I2M11D7M | 7M11D2M2I6M7D8M |
| Reference  | `012345678901234567890123--45678901234567890123` | `012345678901234567890123--45678901234567890123` | `---012345678-------9012345678-----------901234` |
| Read | `---01234567-----------8901234567-------8901234` | `---012345678-------9012345678-----------901234` |

[CIGAR]: https://drive5.com/usearch/manual/cigar.html "CIGAR stands for Concise Idiosyncratic Gapped Alignment Report"
[Prefix sums]: https://codility.com/media/train/3-PrefixSums.pdf "Codility exercise: Prefix sums"
[*O(n)* time complexity]: http://williamrjribeiro.com/?p=132 "Prefix Sums – Time Complexity"

## Installation

1. Create a virtual [conda] (Python 3) environment called `cigar-env` with Python and pip

```bash
➜  conda create --name cigar-env python=3.6 pip
➜  source activate cigar-env
(cigar-env) ➜
```
[conda]: https://docs.anaconda.com/anaconda/install/ "Anaconda Installation"

2. Clone the repository and install package requirements.

```bash
(cigar-env) ➜ git clone https://github.com/foadgr/cigar_task.git
(cigar-env) ➜ cd cigar_task
(cigar-env) ➜ python setup.py install
```

## Setup
1. Execute the `create_data` setup command to create the tab-delimited data files necessary for the main specification and tests.

```bash
(cigar-env) ➜ python setup.py create_data
(cigar-env) ➜ ls -R
```

2. Run the main specification alongside bells and whistles. Note: these will write results to a tab-delimited file in the relative path. `ls -R` to view results output in directory tree.

```bash
(cigar-env) ➜ python cigar_task/task.py
(cigar-env) ➜ ls -R
```

__Output__

```bash
./cigar_task/data/main_spec:
input_01.tsv    input_02.tsv    output_{output_type}.tsv

./cigar_task/data/tests:
input_01.tsv    input_02.tsv    output_{output_type}.tsv
```

3. Run unit tests on main specification and bells and whistles.
```bash
(cigar-env) ➜ python cigar_task/test_task.py
```

__Output__

```bash
..
----------------------------------------------------------------------
Ran 2 tests in 0.029s

OK
```
