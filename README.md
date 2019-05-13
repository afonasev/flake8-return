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

* R501 you shouldn\`t add None at any return if function havn\`t return value except None

```python
def x(y):
    if not y:
        return
    return None  # error!
```

* R502 you should add explicit value at every return if function have return value except None

```python
def x(y):
    if not y:
        return  # error!
    return 1
```

* R503 you should add explicit return at end of the function if function have return value except None

```python
def x(y):
    if not y:
        return  # error!
    return 1
```

* R504 you shouldn`t assign value to variable if it will be use only as return value

```python
def x():
    a = 1
    # some code that not using `a`
    print('test')
    return a  # error!
```

Returns in asyncio coroutines also supported.

## License

MIT

## Change Log

### 1.0.0 - 2019-05-13

* skip assign after unpacking while unnecessary assign checking "(x, y = my_obj)"

### 0.3.2 - 2019-04-01

* allow "assert False" as last function return

### 0.3.1 - 2019-03-11

* add pypi deploy into travis config
* add make bump_version command

### 0.3.0 - 2019-02-26

* skip functions that consist only `return None`
* fix false positive when last return inner with statement
* add unnecessary assign error
* add support tuple in assign or return expressions
* add suppport asyncio coroutines

### 0.2.0 - 2019-02-21

* fix explicit/implicit
* add flake8-plugin-utils as dependency
* allow raise as last function return
* allow no return as last line in while block
* fix if/elif/else cases

### 0.1.1 - 2019-02-10

* fix error messages

### 0.1.0 - 2019-02-10

* initial
