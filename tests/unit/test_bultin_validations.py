import pytest
from typing import List
from parameters_validation import validate_parameters, non_blank, non_null, \
    non_empty, no_whitespaces, non_negative, strongly_typed


@validate_parameters
def foo(
    a: non_blank(),
    b: non_null(),
    c: non_empty(),
    d: no_whitespaces(),
    e: non_negative(),
    f: strongly_typed(List),
):
    return a, b, c, d, e, f


@validate_parameters
def bar(a: strongly_typed()):
    return a


class TestBuiltinValidations:
    def test_success(self):
        foo("non-blank", "", [None], "", 42, [1])

    def test_non_blank(self):
        with pytest.raises(ValueError):
            foo(" ", "", [None], "", 42, [1])

    def test_non_null(self):
        with pytest.raises(ValueError):
            foo("non-blank", None, [None], "", 42, [1])

    def test_non_empty(self):
        with pytest.raises(ValueError):
            foo("non-blank", "", [], "", 42, [1])

    def test_no_whitespaces(self):
        with pytest.raises(ValueError):
            foo("non-blank", "", [None], "white spaced", 42, [1])

    def test_non_negative(self):
        with pytest.raises(ValueError):
            foo("non-blank", "", [None], "", -42, [1])

    def test_strongly_typed(self):
        with pytest.raises(TypeError):
            foo("non-blank", "", [None], "", 42, 7)

    def test_strongly_typed_incorrect_usage(self):
        with pytest.raises(RuntimeError):
            bar("")

    def test_unable_to_validate_non_blank(self):
        with pytest.raises(RuntimeError):
            foo(42, "", [None], "", 42, [1])

    def test_unable_to_validate_non_empty(self):
        with pytest.raises(RuntimeError):
            foo("non-blank", "", None, "", 42, [1])

    def test_unable_to_validate_no_whitespaces(self):
        with pytest.raises(RuntimeError):
            foo("non-blank", "", [None], None, 42, [1])

    def test_unable_to_validate_non_negative(self):
        with pytest.raises(RuntimeError):
            foo("non-blank", "", [None], "", None, [1])
