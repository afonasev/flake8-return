import pytest
from flake8_plugin_utils import assert_error, assert_not_error

from flake8_return import (
    ImplicitReturn,
    ImplicitReturnValue,
    ReturnVisitor,
    UnnecessaryReturnNone,
)


def _ids(values):
    return [str(i) for i, _ in enumerate(values)]


error_not_exists = (
    # without return value
    """
    def x(y):
        if not y:
            return
        return
    """,
    """
    def x(y):
        if y:
            return
        print()
    """,
    # with return value
    """
    def x(y):
        if not y:
            return 1
        return 2
    """,
    """
    def x(y):
        if not y:
            return 1
        else:
            return 2
    """,
    """
    def x(y):
        if not y:
            return 1
        elif y - 10:
            return 2
        else:
            return 3
    """,
    """
    def x(y):
        for i in range(10):
            if i > 100:
                return i
        else:
            return 1
    """,
    """
    def x(y):
        try:
            return 1
        except:
            return 2
    """,
    """
    def x(y):
        try:
            return 1
        finally:
            return 2
    """,
    # inner function
    """
    def x(y):
        if not y:
            return 1
        def inner():
            return
        return 2
    """,
    """
    def x(y):
        if not y:
            return
        def inner():
            return 1
    """,
    # raise as last return
    """
    def x(y):
        if not y:
            return 1
        raise Exception
    """,
    # last line in while loop
    """
    def x(y):
        while True:
            if y > 0:
                return 1
            y += 1
    """,
)


@pytest.mark.parametrize('src', error_not_exists, ids=_ids(error_not_exists))
def test_error_not_exists(src):
    assert_not_error(ReturnVisitor, src)


implicit_return_value = (
    """
    def x(y):
        if not y:
            return
        return 1
    """,
)


@pytest.mark.parametrize(
    'src', implicit_return_value, ids=_ids(implicit_return_value)
)
def test_implicit_return_value(src):
    assert_error(ReturnVisitor, src, ImplicitReturnValue)


unnecessary_return_none = (
    """
    def x(y):
        if not y:
            return
        return None
    """,
)


@pytest.mark.parametrize(
    'src', unnecessary_return_none, ids=_ids(unnecessary_return_none)
)
def test_unnecessary_return_none(src):
    assert_error(ReturnVisitor, src, UnnecessaryReturnNone)


implicit_return = (
    """
    def x(y):
        if not y:
            return 1
    """,
    """
    def x(y):
        if not y:
            print()
        else:
            return 2
    """,
    """
    def x(y):
        if not y:
            return 1
        elif y - 100:
            print()
        else:
            return 2
    """,
    """
    def x(y):
        if not y:
            return 1
        else:
            print()
    """,
)


@pytest.mark.parametrize('src', implicit_return, ids=_ids(implicit_return))
def test_implicit_return(src):
    assert_error(ReturnVisitor, src, ImplicitReturn)
