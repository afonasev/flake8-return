import pytest
from flake8_plugin_utils import assert_error, assert_not_error

from flake8_return.errors import ImplicitReturnValue
from flake8_return.visitors import ReturnVisitor

from . import ids

implicit_return_value = (
    """
    def x(y):
        if not y:
            return  # here
        return 1
    """,
)


@pytest.mark.parametrize(
    'src', implicit_return_value, ids=ids(implicit_return_value)
)
def test_implicit_return_value(src):
    assert_error(ReturnVisitor, src, ImplicitReturnValue)


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
)


@pytest.mark.parametrize('src', error_not_exists, ids=ids(error_not_exists))
def test_error_not_exists(src):
    assert_not_error(ReturnVisitor, src)
