"""
This test covers a fix for a bug first reported in
https://github.com/allrod5/parameters-validation/issues/2

In version 1.1.0 a function annotated with decorator
@validate_parameters would return None regardless of it's actual
return value

This bug was fixed in version 1.1.1
"""
from parameters_validation import non_null, validate_parameters


def test_return_value_is_preserved():
    # given
    @validate_parameters
    def guinea_pig(front: str, back: non_null(str)):
        result = None
        if front:
            result = front + '-' + back
        return result

    # when
    return_value = guinea_pig("one", "two")

    # then
    assert return_value == "one-two"
