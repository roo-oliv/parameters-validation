import pytest
from pytest import fixture

from parameters_validation import validate_parameters, non_blank, non_empty, \
    no_whitespaces


@validate_parameters
def no_validations_function(a: str, b, *, c: dict, d):
    pass


@validate_parameters
def positional_args_validations_function(a: non_blank(str), b, *, c: dict, d):
    pass


@validate_parameters
def keyword_args_validations_function(a: str, b, *, c: non_empty(dict), d):
    pass


@validate_parameters
def args_validations_function(a: non_blank(str), b, *, c: non_empty(dict), d):
    pass


@validate_parameters
def multiple_validations_function(a: no_whitespaces(non_empty(str))):
    pass


class DecoratedMethods:
    @validate_parameters
    def no_validations_method(self, a: str, b, *, c: dict, d):
        pass

    @staticmethod
    @validate_parameters
    def no_validations_staticmethod(a: str, b, *, c: dict, d):
        pass

    @validate_parameters
    def positional_args_validations_method(self, a: non_blank(str), b, *, c: dict, d):
        pass

    @staticmethod
    @validate_parameters
    def positional_args_validations_staticmethod(a: non_blank(str), b, *, c: dict, d):
        pass

    @validate_parameters
    def keyword_args_validations_method(self, a: str, b, *, c: non_empty(dict), d):
        pass

    @staticmethod
    @validate_parameters
    def keyword_args_validations_staticmethod(a: str, b, *, c: non_empty(dict), d):
        pass

    @validate_parameters
    def args_validations_method(self, a: non_blank(str), b, *, c: non_empty(dict), d):
        pass

    @staticmethod
    @validate_parameters
    def args_validations_staticmethod(a: non_blank(str), b, *, c: non_empty(dict), d):
        pass


class TestValidateParametersDecoratorSuccess:
    @fixture(autouse=True)
    def _decorated_methods_fixture(self):
        self.decorate_methods_instance = DecoratedMethods()

    def test_no_validations_function_call(self):
        no_validations_function("", 0, c={}, d=[])

    def test_positional_args_validations_function_call(self):
        positional_args_validations_function("_", 0, c={}, d=[])

    def test_keyword_args_validations_function_call(self):
        keyword_args_validations_function("", 0, c={1: 1}, d=[])

    def test_args_validations_function_call(self):
        args_validations_function("_", 0, c={1: 1}, d=[])

    def test_multiple_validations_function_call(self):
        multiple_validations_function("_")

    def test_no_validations_method_call(self):
        self.decorate_methods_instance.no_validations_method("", 0, c={}, d=[])

    def test_no_validations_staticmethod_call(self):
        DecoratedMethods.no_validations_staticmethod("", 0, c={}, d=[])

    def test_positional_args_validations_method_call(self):
        self.decorate_methods_instance.positional_args_validations_method("_", 0, c={}, d=[])

    def test_positional_args_validations_staticmethod_call(self):
        DecoratedMethods.positional_args_validations_staticmethod("_", 0, c={}, d=[])

    def test_keyword_args_validations_method_call(self):
        self.decorate_methods_instance.keyword_args_validations_method("", 0, c={1: 1}, d=[])

    def test_keyword_args_validations_staticmethod_call(self):
        DecoratedMethods.keyword_args_validations_staticmethod("", 0, c={1: 1}, d=[])

    def test_args_validations_method_call(self):
        self.decorate_methods_instance.args_validations_method("_", 0, c={1: 1}, d=[])

    def test_args_validations_staticmethod_call(self):
        DecoratedMethods.args_validations_staticmethod("_", 0, c={1: 1}, d=[])


class TestValidateParametersDecoratorFailure:
    @fixture(autouse=True)
    def _decorated_methods_fixture(self):
        self.decorate_methods_instance = DecoratedMethods()

    def test_positional_args_validations_function_call(self):
        with pytest.raises(ValueError):
            positional_args_validations_function("", 0, c={}, d=[])

    def test_keyword_args_validations_function_call(self):
        with pytest.raises(ValueError):
            keyword_args_validations_function("", 0, c={}, d=[])

    def test_args_validations_function_call(self):
        with pytest.raises(ValueError):
            args_validations_function("", 0, c={}, d=[])
        with pytest.raises(ValueError):
            args_validations_function("_", 0, c={}, d=[])
        with pytest.raises(ValueError):
            args_validations_function("", 0, c={1: 1}, d=[])

    def test_multiple_validations_function_call(self):
        with pytest.raises(ValueError):
            multiple_validations_function("")
        with pytest.raises(ValueError):
            multiple_validations_function("_ ")

    def test_positional_args_validations_method_call(self):
        with pytest.raises(ValueError):
            self.decorate_methods_instance.positional_args_validations_method("", 0, c={}, d=[])

    def test_positional_args_validations_staticmethod_call(self):
        with pytest.raises(ValueError):
            DecoratedMethods.positional_args_validations_staticmethod("", 0, c={}, d=[])

    def test_keyword_args_validations_method_call(self):
        with pytest.raises(ValueError):
            self.decorate_methods_instance.keyword_args_validations_method("", 0, c={}, d=[])

    def test_keyword_args_validations_staticmethod_call(self):
        with pytest.raises(ValueError):
            DecoratedMethods.keyword_args_validations_staticmethod("", 0, c={}, d=[])

    def test_args_validations_method_call(self):
        with pytest.raises(ValueError):
            self.decorate_methods_instance.args_validations_method("", 0, c={}, d=[])
        with pytest.raises(ValueError):
            self.decorate_methods_instance.args_validations_method("_", 0, c={}, d=[])
        with pytest.raises(ValueError):
            self.decorate_methods_instance.args_validations_method("", 0, c={1: 1}, d=[])

    def test_args_validations_staticmethod_call(self):
        with pytest.raises(ValueError):
            DecoratedMethods.args_validations_staticmethod("", 0, c={}, d=[])
        with pytest.raises(ValueError):
            DecoratedMethods.args_validations_staticmethod("_", 0, c={}, d=[])
        with pytest.raises(ValueError):
            DecoratedMethods.args_validations_staticmethod("", 0, c={1: 1}, d=[])
