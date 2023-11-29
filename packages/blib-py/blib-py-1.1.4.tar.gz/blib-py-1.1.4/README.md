# Boonleng's Python Library

This is a collection of some convenient functions, color schemes, etc. for convenient coding in the future.

### Install Using the Python Package Installaer

```shell
pip install blib-py
```

### Install from Source for System-Wide Usage

Download the project from either GitHub or ARRC GitLab:

```shell
git clone https://github.com/boonleng/blib-py.git
```

or

```shell
git clone https://git.arrc.ou.edu/cheo4524/blib-py.git
```

Change directory to the project folder and install using `pip`.

```shell
cd blib-py
pip install .
```

### Use It Without Instlallation

It is possible to use this library without installation. Assuming that you downloaded the project into the folder `~/Developer/blib-py`, you can add the path to Python's search path as follows.

```python
import os
import sys

sys.path.insert(0, os.path.expanduser('~/Developer/blib-py'))

import blib
```

### Colors

![Pallete](blob/swatch-lab.png)

### Notes to Myself

My memory is no longer as good as it used to be so I'm leaving myself some notes here. Don't use them.

```shell
python setup.py sdist upload
```

or

```shell
 twine upload --repository blib dist/*
```
