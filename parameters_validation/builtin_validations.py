from numbers import Number
from typing import Sized

from parameters_validation.parameter_validation_decorator import parameter_validation


@parameter_validation
def non_blank(string: str, arg_name: str, arg_type: type = str):
    """
    Validation to reject null, empty or blank strings.

    >>> from parameters_validation import validate_parameters
    ...
    ... @validate_parameters
    ... def foo(bar: non_blank(str)):
    ...     print(bar)
    ...
    ... foo(".")   # valid: string is not null, empty nor blank
    ... foo(None)  # invalid: string is null
    ... foo("")    # invalid: string is empty
    ... foo("  ")  # invalid: string is blank (i.e., contains just whitespaces)

    :param string: the parameter's value being validated
    :param arg_name: the argument name for this parameter (provided by the :meth:`parameter_validation` decorator)
    :param arg_type: the argument type for this parameter (provided by the :meth:`parameter_validation` decorator)
    :return: None
    :raises ValueError: invalid parameter, i.e. :param string: is either of type `NoneType`, empty (no length) or blank (contains just whitespaces)
    :raises RuntimeError: unable to validate parameter (possibly :param string: is of an unexpected type)
    """
    validation_error = None
    arg = arg_name
    if arg_type is not None:
        arg += " <{t}>".format(t=arg_type.__name__)
    try:
        if not bool(string and string.strip()):
            validation_error = ValueError(
                "Parameter `{arg}` cannot be blank nor empty".format(arg=arg))
    except Exception as e:
        validation_error = RuntimeError(
            "Unable to validate parameter `{arg}`: {error_name}{error}".format(arg=arg, error_name=e.__class__.__name__, error=e), e)
    if validation_error:
        raise validation_error


@parameter_validation
def non_null(obj: object, arg_name: str, arg_type: type = object):
    """
    Validation to reject null objects.

    >>> from parameters_validation import validate_parameters
    ...
    ... @validate_parameters
    ... def foo(bar: non_null(str)):
    ...     print(bar)
    ...
    ... foo("")    # valid: object is not null
    ... foo(False) # valid: object is not null
    ... foo(None)  # invalid: object is null

    :param obj: the parameter's value being validated
    :param arg_name: the argument name for this parameter (provided by the :meth:`parameter_validation` decorator)
    :param arg_type: the argument type for this parameter (provided by the :meth:`parameter_validation` decorator)
    :return: None
    :raises ValueError: invalid parameter, i.e. :param obj: is of type `NoneType`
    """
    arg = arg_name
    if arg_type is not None:
        arg += " <{t}>".format(t=arg_type.__name__)
    if obj is None:
        raise ValueError("Parameter `{arg}` cannot not be None".format(arg=arg))


@parameter_validation
def non_empty(obj: Sized, arg_name: str, arg_type: type = object):
    """
    Validation to reject empty objects.

    >>> from parameters_validation import validate_parameters
    ...
    ... @validate_parameters
    ... def foo(bar: non_empty(str)):
    ...     print(bar)
    ...
    ... foo(".")           # valid: object is not empty
    ... foo([None, None])  # valid: object is not empty
    ... foo("")            # invalid: object is empty
    ... foo({})            # invalid: object is empty

    :param obj: the parameter's value being validated
    :param arg_name: the argument name for this parameter (provided by the :meth:`parameter_validation` decorator)
    :param arg_type: the argument type for this parameter (provided by the :meth:`parameter_validation` decorator)
    :return: None
    :raises ValueError: invalid parameter, i.e. :param obj: has size zero (no length)
    :raises RuntimeError: unable to validate parameter (possibly the parameter is of an unexpected type)
    """
    validation_error = None
    arg = arg_name
    if arg_type is not None:
        arg += " <{t}>".format(t=arg_type.__name__)
    try:
        if len(obj) == 0:
            validation_error = ValueError("Parameter `{arg}` cannot be empty".format(arg=arg))
    except Exception as e:
        validation_error = RuntimeError(
            "Unable to validate parameter `{arg}`: {error_name}{error}".format(arg=arg, error_name=e.__class__.__name__, error=e), e)
    if validation_error:
        raise validation_error


@parameter_validation
def no_whitespaces(string: str, arg_name: str, arg_type: type = str):
    """
    Validation to reject strings with whitespaces.

    >>> from parameters_validation import validate_parameters
    ...
    ... @validate_parameters
    ... def foo(bar: no_whitespaces(str)):
    ...     print(bar)
    ...
    ... foo("sao_paulo")   # valid: string does not contain whitespaces
    ... foo("sao paulo")   # invalid: string does contain whitespaces
    ... foo("")            # valid: string does not contain whitespaces
    ... foo(" ")           # invalid: string does contain whitespaces

    :param string: the parameter's value being validated
    :param arg_name: the argument name for this parameter (provided by the :meth:`parameter_validation` decorator)
    :param arg_type: the argument type for this parameter (provided by the :meth:`parameter_validation` decorator)
    :return: None
    :raises ValueError: invalid parameter, i.e. :param string: contains one or more whitespaces
    :raises RuntimeError: unable to validate parameter (possibly :param string: is of an unexpected type)
    """
    validation_error = None
    arg = arg_name
    if arg_type is not None:
        arg += " <{t}>".format(t=arg_type.__name__)
    try:
        if " " in string:
            validation_error = ValueError(
                "Parameter `{arg}` cannot contain whitespaces".format(arg=arg))
    except Exception as e:
        validation_error = RuntimeError(
            "Unable to validate parameter `{arg}`: {error_name}{error}".format(arg=arg, error_name=e.__class__.__name__, error=e), e)
    if validation_error:
        raise validation_error


@parameter_validation
def non_negative(number: Number, arg_name: str, arg_type: type = str):
    """
    Validation to reject negative numbers.

    >>> from parameters_validation import validate_parameters
    ...
    ... @validate_parameters
    ... def foo(bar: non_negative(float)):
    ...     print(bar)
    ...
    ... foo(0.0)   # valid: number is non-negative
    ... foo(-0.1)   # invalid: number is negative

    :param number: the parameter's value being validated
    :param arg_name: the argument name for this parameter (provided by the :meth:`parameter_validation` decorator)
    :param arg_type: the argument type for this parameter (provided by the :meth:`parameter_validation` decorator)
    :return: None
    :raises ValueError: invalid parameter, i.e. :param number: contains one or more whitespaces
    :raises RuntimeError: unable to validate parameter (possibly :param number: is of an unexpected type)
    """
    validation_error = None
    arg = arg_name
    if arg_type is not None:
        arg += " <{t}>".format(t=arg_type.__name__)
    try:
        if number < 0:
            validation_error = ValueError(
                "Parameter `{arg}` cannot be negative".format(arg=arg))
    except Exception as e:
        validation_error = RuntimeError(
            "Unable to validate parameter `{arg}`: {error_name}{error}".format(arg=arg, error_name=e.__class__.__name__, error=e), e)
    if validation_error:
        raise validation_error
