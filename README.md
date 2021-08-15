# flake8-return

[![pypi](https://badge.fury.io/py/flake8-return.svg)](https://pypi.org/project/flake8-return)
[![Python: 3.6+](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://pypi.org/project/flake8-return)
[![Downloads](https://img.shields.io/pypi/dm/flake8-return.svg)](https://pypistats.org/packages/flake8-return)
[![Build Status](https://travis-ci.org/Afonasev/flake8-return.svg?branch=master)](https://travis-ci.org/Afonasev/flake8-return)
[![Code coverage](https://codecov.io/gh/afonasev/flake8-return/branch/master/graph/badge.svg)](https://codecov.io/gh/afonasev/flake8-return)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://en.wikipedia.org/wiki/MIT_License)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Flake8 plugin that checks return values.

## Installation

```bash
pip install flake8-return
```

## Errors

* R501 do not explicitly return None in function if it is the only possible return value.

```python
def x(y):
    if not y:
        return
    return None  # error!
```

* R502 do not implicitly return None in function able to return non-None value.

```python
def x(y):
    if not y:
        return  # error!
    return 1
```

* R503 missing explicit return at the end of function able to return non-None value.

```python
def x(y):
    if not y:
        return 1
    # error!
```

* R504 unnecessary variable assignment before return statement.

```python
def x():
    a = 1
    # some code that not using `a`
    print('test')
    return a  # error!
```

Returns in asyncio coroutines also supported.

## For developers

### Show help

    make help

### Create venv and install deps

    make init

### Install git precommit hook

    make precommit

### Run linters, autoformat, tests etc.

    make pretty lint test

### Bump new version

    make bump_major
    make bump_minor
    make bump_patch

## Change Log

Unreleased
-----

* ...

1.1.3 - 2021-05-05
-----

* Error clarifications (#77) Clément Robert
* fix linting (migrate to black 20.0b1) (#78) Clément Robert

1.1.2 - 2020-07-09
-----

* Make R504 visitors handle while loops (#56) Frank Tackitt
* Rename allows-prereleases to allow-prereleases (#55) Frank Tackitt
* Fix typo: havn't → haven't (#24) Jon Dufresne

1.1.1 - 2019-09-21
-----

* fixed [#3](https://github.com/afonasev/flake8-return/issues/3) The R504 doesn't detect that the variable is modified in loop
* fixed [#4](https://github.com/afonasev/flake8-return/issues/4) False positive with R503 inside async with clause

1.1.0 - 2019-05-23
-----

* update flask_plugin_utils version to 1.0

1.0.0 - 2019-05-13
-----

* skip assign after unpacking while unnecessary assign checking "(x, y = my_obj)"

0.3.2 - 2019-04-01
-----

* allow "assert False" as last function return

0.3.1 - 2019-03-11
-----

* add pypi deploy into travis config
* add make bump_version command

0.3.0 - 2019-02-26
-----

* skip functions that consist only `return None`
* fix false positive when last return inner with statement
* add unnecessary assign error
* add support tuple in assign or return expressions
* add suppport asyncio coroutines

0.2.0 - 2019-02-21
-----

* fix explicit/implicit
* add flake8-plugin-utils as dependency
* allow raise as last function return
* allow no return as last line in while block
* fix if/elif/else cases

0.1.1 - 2019-02-10
-----

* fix error messages

0.1.0 - 2019-02-10
-----

* initial
