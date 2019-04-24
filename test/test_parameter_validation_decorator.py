import pytest

from parameters_validation import parameter_validation, validate_parameters


@parameter_validation
def even(param: int, arg_name: str, arg_type: str):
    """
    Validation to reject odd numbers
    """
    validation_error = None
    arg = arg_name
    if arg_type is not None:
        arg += " <{t}>".format(t=arg_type.__name__)
    try:
        if param % 2 != 0:
            validation_error = ValueError(
                "Parameter `{arg}` is not even".format(arg=arg))
    except Exception as e:
        validation_error = RuntimeError(
            "Unable to validate parameter `{arg}`: {error_name}{error}".format(
                arg=arg, error_name=e.__class__.__name__, error=e), e)
    if validation_error:
        raise validation_error


@validate_parameters
def foo(x: even(int)):
    return x / 2


class TestParameterValidationDecorator:
    def test_for_success(self):
        foo(0)
        foo(2)
        foo(-4)
        foo(42)

    def test_for_failure(self):
        with pytest.raises(ValueError):
            foo(1)
        with pytest.raises(ValueError):
            foo(-1)
        with pytest.raises(ValueError):
            foo(7)
        with pytest.raises(ValueError):
            foo(20000001)

