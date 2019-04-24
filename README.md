# parameters-validation
Easy &amp; clean function parameters validation

[![Build Status](https://travis-ci.org/allrod5/parameters-validation.svg?branch=master)](https://travis-ci.org/allrod5/parameters-validation) [![Coverage Status](https://coveralls.io/repos/github/allrod5/parameters-validation/badge.svg?branch=master)](https://coveralls.io/github/allrod5/parameters-validation?branch=master) [![Supported Python Versions](https://img.shields.io/pypi/pyversions/parameters-validation.svg)](https://pypi.org/project/parameters-validation/) [![Latest Version](https://img.shields.io/pypi/v/parameters-validation.svg)](https://pypi.org/project/parameters-validation/) [![License](https://img.shields.io/github/license/allrod5/parameters-validation.svg)](https://github.com/allrod5/parameters-validation/blob/master/LICENSE)

## Usage

Decorate your function with `@validate_parameters` and define validations to
each parameter.

```python
from parameters_validation import no_whitespaces, non_blank, non_empty, non_negative, validate_parameters

@validate_parameters
def register(
    name: non_blank(str),
    age: non_negative(int),
    nickname: no_whitespaces(non_empty(str)),
    bio: str,
):
    # do register
```

Then at every function call parameters passed will be validated before actually
executing it and raise a `ValueError` or do anything else in case of
custom-defined validations.

### Install

```bash
pip install parameters-validation
```

## Custom validations

Creating your own validations is as easy as decorating the validation function
with `@parameter_validation`:

```python
from pandas import dataframe
from parameters_validation import parameter_validation, validate_parameters

@parameter_validation
def has_id_column(df: dataframe):
    if "id" not in df:
        raise ValueError("Dataframe must contain an `id` column")

@validate_parameters
def ingest(df: has_id_column(dataframe)):
    # ingest
```

You can use a custom validation for other purposes too but keep in mind that
validation functions cannot alter the actual parameter value:

```python
import logging
from parameters_validation import parameter_validation, validate_parameters

@parameter_validation
def log_to_debug(param: str, arg_name: str):
    logging.debug("{arg} = {value}".format(arg=arg_name, value=param))

@validate_parameters
def foo(df: log_to_debug(str)):
    # ingest
```
