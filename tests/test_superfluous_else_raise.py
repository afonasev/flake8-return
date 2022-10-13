import pytest
from flake8_plugin_utils import assert_error, assert_not_error

from flake8_return.errors import SuperfluousElseRaise
from flake8_return.visitors import ReturnVisitor

from . import ids

superfluous_else = (
    """
    def foo1(x, y, z):
        if x:  # [no-else-raise]
            a = 1
            raise Exception(y)
        else:
            b = 2
            raise Exception(z)
    """,
    """
    def foo3(x, y, z):
        if x:
            a = 1
            if y:  # [no-else-raise]
                b = 2
                raise Exception(y)
            else:
                c = 3
                raise Exception(x)
        else:
            d = 4
            raise Exception(z)
    """,
    """
    def foo4(x, y):
        if x: # [no-else-raise]
            if y:
                a = 4
            else:
                b = 2
            raise Exception(x)
        else:
            c = 3
        raise Exception(y)
    """,
    """
    def foo6(x, y):
        if x:
            if y:   # [no-else-raise]
                a = 4
                raise Exception(x)
            else:
                b = 2
        else:
            c = 3
        raise Exception(y)
    """,
    """
    def bar4(x):
        if x:  # [no-else-raise]
            raise Exception(True)
        else:
            try:
                raise Exception(False)
            except ValueError:
                raise Exception(None)
    """,
)


@pytest.mark.parametrize('src', superfluous_else, ids=ids(superfluous_else))
def test_superfluous_else_raise(src):
    assert_error(ReturnVisitor, src, SuperfluousElseRaise)


error_not_exists = (
    """
    def bar1(x, y, z):
        if x:
            raise Exception(y)
        raise Exception(z)
    """,
    """
    def bar2(w, x, y, z):
        if x:
            raise Exception(y)
        if z:
            a = 1
        else:
            raise Exception(w)
        raise Exception(None)
    """,
    """
    def bar3(x, y, z):
        if x:
            if z:
                raise Exception(y)
        else:
            raise Exception(z)
        raise Exception(None)
    """,
)


@pytest.mark.parametrize('src', error_not_exists, ids=ids(error_not_exists))
def test_error_not_exists(src):
    assert_not_error(ReturnVisitor, src)
