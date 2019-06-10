"""
This test covers a fix for a bug first reported in
https://github.com/allrod5/parameters-validation/issues/5

In version 1.1.1 a function annotated with decorator
@validate_parameters would crash if the builtin validation
`strongly_typed` is used for a parameter with default value
and there is a call to this function that uses the default value

This bug was fixed in version 1.1.2
"""
from parameters_validation import non_null, validate_parameters, strongly_typed


def test_strongly_typed_on_default_parameters():
    # given
    default_value = "default value"
    @validate_parameters
    def guinea_pig(a: strongly_typed(str) = default_value):
        return a

    # when
    return_value = guinea_pig()

    # then
    assert return_value == default_value
