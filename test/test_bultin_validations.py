import pytest

from parameters_validation import validate_parameters, non_blank, non_null, \
    non_empty, no_whitespaces, non_negative


@validate_parameters
def foo(
    a: non_blank(),
    b: non_null(),
    c: non_empty(),
    d: no_whitespaces(),
    e: non_negative(),
):
    return a, b, c, d, e


class TestBuiltinValidations:
    def test_success(self):
        foo("non-blank", "", [None], "", 42)

    def test_non_blank(self):
        with pytest.raises(ValueError):
            foo(" ", "", [None], "", 42)

    def test_non_null(self):
        with pytest.raises(ValueError):
            foo("non-blank", None, [None], "", 42)

    def test_non_empty(self):
        with pytest.raises(ValueError):
            foo("non-blank", "", [], "", 42)

    def test_no_whitespaces(self):
        with pytest.raises(ValueError):
            foo("non-blank", "", [None], "white spaced", 42)

    def test_non_negative(self):
        with pytest.raises(ValueError):
            foo("non-blank", "", [None], "", -42)
