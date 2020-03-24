import inspect
from copy import deepcopy
from functools import wraps


def _get_parameter_value_dict(specs, args, kwargs):
    parameters = kwargs.copy()
    for arg_value, parameter in zip(args, specs.args):
        parameters[parameter] = arg_value
    if specs.defaults:
        for default_parameter, default_value in zip(
                specs.args[len(specs.args) - len(specs.defaults):], specs.defaults
        ):
            if default_parameter in parameters:
                continue
            parameters[default_parameter] = default_value
    if specs.kwonlydefaults:
        for default_parameter, default_value in specs.kwonlydefaults.items():
            if default_parameter in parameters:
                continue
            parameters[default_parameter] = default_value
    return parameters


def _get_wrapper(f: callable, specs: inspect.FullArgSpec, validations: dict = None):
    if validations is None:
        validations = specs.annotations

    @wraps(f)
    def wrapper(*args, **kwargs):
        parameters = _get_parameter_value_dict(specs, args, kwargs)
        for parameter, annotation in validations.items():
            if not hasattr(annotation, "_parameter_validation"):
                continue
            annotation(parameters[parameter], parameter)

        return f(*args, **kwargs)

    def parameter_validation_mock(pseudo_validation_function: callable):
        mock = deepcopy(pseudo_validation_function)
        mock._parameter_validation = True
        return mock

    def mock_validations(mocks: dict):
        valid_mocks = {p: parameter_validation_mock(v) for p, v in mocks.items()}
        return _get_wrapper(f, specs, {**validations, **valid_mocks})
    wrapper.mock_validations = mock_validations
    wrapper.skip_validations = lambda: f

    return wrapper


def validate_parameters(func):
    """
    Decorator to apply validations in the parameters type hints before executing the
    decorated function.

    >>> from parameters_validation import non_empty, no_whitespaces
    ...
    ... @validate_parameters
    ... def foo(ans: no_whitespaces(non_empty(str))):
    ...     print(ans)
    ...
    ... foo("valid-parameter")  # valid, not empty and no whitespaces
    ... foo("white spaced")     # invalid, contains whitespaces
    ... foo("")                 # invalid, empty
    ... foo(None)               # invalid, none

    Validations can be skipped with `.skip_validations()`:

    >>> from parameters_validation import non_blank
    ...
    ... @validate_parameters
    ... def foo(s: non_blank(str)):
    ...     pass
    ...
    ... foo.skip_validations()("")  # does not throw since validations are skipped

    Validations can be mocked for testing purposes with `.mock_validations({...})`:

    >>> from parameters_validation import non_blank
    ...
    ... @validate_parameters
    ... def foo(s: non_blank(str)):
    ...     pass
    ...
    ... foo.mock_validations({"s": lambda *_: print("mocked")})("")  # prints "mocked"

    :param func: decorated function
    :return: wrapped function
    """
    specs = inspect.getfullargspec(func)
    return _get_wrapper(func, specs)
