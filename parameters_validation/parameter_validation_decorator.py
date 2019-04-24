import inspect
from functools import wraps


def parameter_validation(func):
    """
    Decorator to make the function to be applied as parameter validation when used
    together with the :meth:`parameter_validation.validate_parameters` decorator.

    >>> @parameter_validation
    ... def within_bounds(param: int, arg_name: str, arg_type: str):
    ...     if param < 0 or param > 100:
    ...         raise ValueError("`{n} <{t}>: {v}` is out of allowed bounds [0,100]".format(n=arg_name, t=arg_type, v=param))
    ...
    ... from parameters_validation import validate_parameters
    ... @validate_parameters
    ... def foo(x: within_bounds(int)):
    ...     print(x)
    ...
    ... foo(5)    # validation will succeed
    ... foo(400)  # validation will fail

    :param func: decorated function
    :return: wrapped function
    """
    @wraps(func)
    def validation(parameter, arg_name: str, arg_type: type):
        func_specs = inspect.getfullargspec(func)
        func_parameters = func_specs.args + func_specs.kwonlyargs
        kwargs = {}
        if "arg_name" in func_parameters:
            kwargs["arg_name"] = arg_name
        if "arg_type" in func_parameters:
            kwargs["arg_type"] = arg_type
        return func(parameter, **kwargs)

    def func_partial(arg_type: type = None):
        def validation_partial(parameter, arg_name: str):
            nonlocal arg_type
            if hasattr(arg_type, "_parameter_validation"):
                nested_validation = arg_type
                arg_type = nested_validation._arg_type
                nested_validation(parameter, arg_name)
            validation(parameter, arg_name, arg_type)

        validation_partial._parameter_validation = True
        validation_partial._arg_type = arg_type
        return validation_partial

    return func_partial
