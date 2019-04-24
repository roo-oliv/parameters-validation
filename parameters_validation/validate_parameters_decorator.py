import inspect
from functools import wraps


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

    :param func: decorated function
    :return: wrapped function
    """
    specs = inspect.getfullargspec(func)
    @wraps(func)
    def wrapper(*args, **kwargs):
        parameters = kwargs.copy()
        for arg_value, parameter in zip(args, specs.args):
            parameters[parameter] = arg_value

        for parameter, annotation in specs.annotations.items():
            if not hasattr(annotation, "_parameter_validation"):
                continue
            annotation(parameters[parameter], parameter)

        func(*args, **kwargs)

    return wrapper
