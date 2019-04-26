# parameters-validation
Easy &amp; clean function parameters validation

[![Build Status](https://travis-ci.org/allrod5/parameters-validation.svg?branch=master)](https://travis-ci.org/allrod5/parameters-validation) [![Coverage Status](https://coveralls.io/repos/github/allrod5/parameters-validation/badge.svg?branch=master)](https://coveralls.io/github/allrod5/parameters-validation?branch=master) [![Supported Python Versions](https://img.shields.io/pypi/pyversions/parameters-validation.svg)](https://pypi.org/project/parameters-validation/) [![Latest Version](https://img.shields.io/pypi/v/parameters-validation.svg)](https://pypi.org/project/parameters-validation/) [![License](https://img.shields.io/github/license/allrod5/parameters-validation.svg)](https://github.com/allrod5/parameters-validation/blob/master/LICENSE)

## Usage

Decorate your function with `@validate_parameters` and define validations to
each parameter.

```python
from parameters_validation import no_whitespaces, non_blank, non_empty, non_negative, strongly_typed, validate_parameters

from  my_app.auth import AuthToken

@validate_parameters
def register(
    token: strongly_typed(AuthToken),
    name: non_blank(str),
    age: non_negative(int),
    nickname: no_whitespaces(non_empty(str)),
    bio: str,
):
    # do register
```

Then at every function call parameters passed will be validated before actually
executing it and raise an error or do anything else in case of custom-defined
validations.

### Install

```bash
pip install parameters-validation
```

## Custom validations

Creating your own validation is as easy as decorating the validation function
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
    # do something
```

## When to validate parameters

It is a pythonic convention follow the [EAFP](https://docs.python.org/3/glossary.html#term-eafp) principle whenever possible. There are cases however that skipping validations leads to silent errors and big headaches. Let's use an illustrative example:

```python
from pyspark.sql import DataFrame

def persist_to_s3(df: DataFrame, path: str):
    df.write.parquet(path)
```

This code is perfectly fine but assume that there is a business requirement that all persisted dataframes contain a `ts` column with the data timestamp.

Blindly following [EAFP](https://docs.python.org/3/glossary.html#term-eafp) the code is left unchanged but other developers can write dataframes without the `ts` column and no error will be logged. In the worst case it can lead to tons of data being saved wrong and rendered useless.

[EAFP](https://docs.python.org/3/glossary.html#term-eafp) works well when code is still able to deal with exception scenarios where it will eventually break. In the example above a validation to the dataframe is appropriate:

```python
from pyspark.sql import DataFrame

def persist_to_s3(df: DataFrame, path: str):
    if "ts" not in df.columns:
        raise ValueError("dataframe is missing a `ts` column")
    df.write.parquet(path)
```

`parameters-validation` package helps you being more declarative in your validations stating them right at the function's signature and avoiding polution of your function's body with validation code:

```python
from pyspark.sql import DataFrame
from parameters_validation import parameter_validation, validate_parameters

@parameter_validation
def with_ts_column(df: DataFrame):
     if "ts" not in df.columns:
        raise ValueError("dataframe is missing a `ts` column")

@validate_parameters
def persist_to_s3(df: with_ts_column(DataFrame), path: str):
    df.write.parquet(path)
```
