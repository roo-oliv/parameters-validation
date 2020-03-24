import pytest

from parameters_validation import validate_parameters, parameter_validation, non_blank


@parameter_validation
def type_error(*args, **kwargs):
    raise TypeError


def value_error(*args, **kwargs):
    raise ValueError


@validate_parameters
def foo(arg: type_error(str)):
    pass


@validate_parameters
def bar(arg: non_blank(str)):
    pass


class TestValidateParametersDecoratorMock:
    def test_setup(self):
        with pytest.raises(TypeError):
            foo("anything")

    def test_mock_validation_replaces_original(self):
        with pytest.raises(ValueError):
            foo.mock_validations({"arg": value_error})("anything")

    def test_unmatched_mock_raises_key_error(self):
        with pytest.raises(KeyError):
            bar.mock_validations({"unmatched": value_error})("non_blank")
