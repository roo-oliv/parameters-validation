from parameters_validation import validate_parameters, parameter_validation


@parameter_validation
def custom_validation(param, arg_name, arg_type):
    raise Exception


@validate_parameters
def foo(arg: custom_validation(str)):
    pass


class TestValidateParametersDecoratorSkip:
    def test_skip_validation(self):
        foo.skip_validations()("anything")
