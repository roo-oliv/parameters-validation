"""
This test covers a fix for a bug first reported in
https://github.com/allrod5/parameters-validation/issues/8

In version 1.1.3 validations defined for a parameter with default a
value are always applied to the default value and not to explicit
passed values.

This bug was fixed in version 1.1.4
"""
import pytest

from parameters_validation import validate_parameters, non_blank, no_whitespaces


class TestValidationsOnParameterWithDefaultValue:
    def test_default_value_success(self):
        # given
        default_value = "default_value"

        @validate_parameters
        def guinea_pig(s: no_whitespaces(non_blank(str)) = default_value):
            return s

        # when
        return_value = guinea_pig()

        # then
        assert return_value == default_value

    def test_bad_default_value(self):
        # given
        default_value = "default value"

        @validate_parameters
        def guinea_pig(s: no_whitespaces(non_blank(str)) = default_value):
            return s

        # then
        with pytest.raises(ValueError):
            guinea_pig()

    def test_custom_value_success(self):
        # given
        default_value = "default_value"
        custom_value = "custom_value"

        @validate_parameters
        def guinea_pig(s: no_whitespaces(non_blank(str)) = default_value):
            return s

        # when
        return_value = guinea_pig(custom_value)

        # then
        assert return_value == custom_value

    def test_bad_custom_value(self):
        # given
        default_value = "default_value"
        whitespaced_string = "whitespaced string"
        blank_string = "    "
        empty_string = ""
        null_string = None

        @validate_parameters
        def guinea_pig(s: no_whitespaces(non_blank(str)) = default_value):
            return s

        # then
        with pytest.raises(ValueError):
            guinea_pig(whitespaced_string)

        # then
        with pytest.raises(ValueError):
            guinea_pig(blank_string)

        # then
        with pytest.raises(ValueError):
            guinea_pig(empty_string)

        # then
        with pytest.raises(ValueError):
            guinea_pig(null_string)
