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
* R502 you should add explicit value at every return if function have return value except None
* R503 you should add explicit return at end of the function if function have return value except None

## License

MIT

## Change Log

### 0.2.0 - 2019.02.21

* fix explicit/implicit
* add flake8-plugin-utils as dependency
* allow raise as last function return
* allow no return as last line in while block
* fix if/elif/else cases

### 0.1.1 - 2019.02.10

* fix error messages

### 0.1.0 - 2019.02.10

* initial
