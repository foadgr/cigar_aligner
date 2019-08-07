# Cigar Task
The objective of this task is to use a [CIGAR] string to retrieve paired coordinates in (5'➜3') from a transcript read to a reference genome from SAM/BAM format.

Additional objectives for the task include the retrieval of coordinates (or mapped coordinate ranges) under the following conditions:
* Reversed strand directionality (3'➜5')
* Inverted alignment (reference is aligned to the read)


[CIGAR]: https://drive5.com/usearch/manual/cigar.html "CIGAR stands for Concise Idiosyncratic Gapped Alignment Report"


## Installation

1. Create a virtual conda (Python 3) environment called `cigar-env` with Python and pip
```bash
➜  conda create --name cigar-env python=3.6 pip
➜  source activate cigar-env
(cigar-env) ➜
```

2. Clone the repository and change to the cloned working directory.
```bash
(cigar-env) ➜ git clone https://github.com/foadgr/cigar_task.git
(cigar-env) ➜ cd cigar_task
```

## Setup

1. Execute the custom `create_data` command to create the tab-delimited data files for the main specification and tests. List recursive to view lower folder structure.
```bash
(cigar-env) ➜ python setup.py create_data
(cigar-env) ➜ ls -R
```

__Output__
```bash
./cigar_task/data/main_spec:
input_01.tsv    input_02.tsv

./cigar_task/data/tests:
input_01.tsv    input_02.tsv
```

2. Execute the main specification and tests. Note: these will write results to a tab-delimited file in the relative path.

```bash
(cigar-env) ➜ python cigar_task/task.py
(cigar-env) ➜ ls -R
```

__Output__
```bash
./cigar_task/data/main_spec:
input_01.tsv    input_02.tsv    output_00.tsv

./cigar_task/data/tests:
input_01.tsv    input_02.tsv    output_00.tsv
```

