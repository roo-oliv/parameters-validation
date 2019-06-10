"""
This test covers a fix for a bug first reported in
https://github.com/allrod5/parameters-validation/issues/5

In version 1.1.1 a function annotated with decorator
@validate_parameters would crash if the builtin validation
`strongly_typed` is used for a parameter with default value
and there is a call to this function that uses the default value

This bug was fixed in version 1.1.3
"""
from parameters_validation import validate_parameters, strongly_typed


class TestStronglyTypedOnDefaultParameters:
    def test_function_with_just_one_default_arg(self):
        # given
        default_value = "default value"
        @validate_parameters
        def just_one_default_arg(a: strongly_typed(str) = default_value):
            return a

        # when
        return_value = just_one_default_arg()

        # then
        assert return_value == default_value

    def test_function_with_just_one_default_kwonly_arg(self):
        # given
        default_value = "default value"
        @validate_parameters
        def just_one_default_kwonly_arg(*, a: strongly_typed(str) = default_value):
            return a

        # when
        return_value = just_one_default_kwonly_arg()

        # then
        assert return_value == default_value

    def test_function_with_default_arg_and_kwonly_arg(self):
        # given
        default_value = "default value"
        @validate_parameters
        def default_arg_and_kwonly_arg(
                a: strongly_typed(str) = default_value,
                b: strongly_typed(str) = default_value,
        ):
            return a, b

        # when
        return_value = default_arg_and_kwonly_arg()

        # then
        assert return_value == (default_value, default_value)

    def test_function_with_mixed_default_and_not_default_arg_and_kwonly_arg(self):
        # given
        default_value = "default value"
        @validate_parameters
        def mixed_default_and_not_default_arg_and_kwonly_arg(
                a: strongly_typed(str),
                b: strongly_typed(str) = default_value,
                *,
                c: strongly_typed(str),
                d: strongly_typed(str) = default_value
        ):
            return a, b, c, d

        # when
        return_value = mixed_default_and_not_default_arg_and_kwonly_arg(
            default_value, c=default_value
        )

        # then
        assert return_value == (
            default_value, default_value, default_value, default_value
        )

    def test_function_with_mixed_default_and_not_default_arg_and_kwonly_arg_2(self):
        # given
        default_value = "default value"
        @validate_parameters
        def mixed_default_and_not_default_arg_and_kwonly_arg(
                a: strongly_typed(str),
                b: strongly_typed(str) = default_value,
                *,
                c: strongly_typed(str),
                d: strongly_typed(str) = default_value
        ):
            return a, b, c, d

        # when
        return_value = mixed_default_and_not_default_arg_and_kwonly_arg(
            a=default_value, c=default_value
        )

        # then
        assert return_value == (
            default_value, default_value, default_value, default_value
        )

    def test_function_with_mixed_default_and_not_default_arg_and_kwonly_arg_3(self):
        # given
        default_value = "default value"
        custom_value = "custom value"
        @validate_parameters
        def mixed_default_and_not_default_arg_and_kwonly_arg(
                a: strongly_typed(str),
                b: strongly_typed(str) = default_value,
                *,
                c: strongly_typed(str),
                d: strongly_typed(str) = default_value
        ):
            return a, b, c, d

        # when
        return_value = mixed_default_and_not_default_arg_and_kwonly_arg(
            custom_value, custom_value, c=custom_value, d=custom_value
        )

        # then
        assert return_value == (
            custom_value, custom_value, custom_value, custom_value
        )
