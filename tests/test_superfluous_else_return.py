import pytest
from flake8_plugin_utils import assert_error, assert_not_error

from flake8_return.errors import SuperfluousElseReturn
from flake8_return.visitors import ReturnVisitor

from . import ids

superfluous_else = (
    """
    def foo1(x, y, z):
        if x:  # [no-else-return]
            a = 1
            return y
        else:
            b = 2
            return z
    """,
    """
    def foo3(x, y, z):
        if x:
            a = 1
            if y:  # [no-else-return]
                b = 2
                return y
            else:
                c = 3
                return x
        else:
            d = 4
            return z
    """,
    """
    def foo4(x, y):
        if x:   # [no-else-return]
            if y:
                a = 4
            else:
                b = 2
            return
        else:
            c = 3
        return
    """,
    """
    def foo6(x, y):
        if x:
            if y:   # [no-else-return]
                a = 4
                return
            else:
                b = 2
        else:
            c = 3
        return
    """,
    """
    def bar4(x):
        if x:  # [no-else-return]
            return True
        else:
            try:
                return False
            except ValueError:
                return None
    """,
)


@pytest.mark.parametrize('src', superfluous_else, ids=ids(superfluous_else))
def test_superfluous_else_return(src):
    assert_error(ReturnVisitor, src, SuperfluousElseReturn)


error_not_exists = (
    """
    def bar1(x, y, z):
        if x:
            return y
        return z
    """,
    """
    def bar2(w, x, y, z):
        if x:
            return y
        if z:
            a = 1
        else:
            return w
        return None
    """,
    """
    def bar3(x, y, z):
        if x:
            if z:
                return y
        else:
            return z
        return None
    """,
)


@pytest.mark.parametrize('src', error_not_exists, ids=ids(error_not_exists))
def test_error_not_exists(src):
    assert_not_error(ReturnVisitor, src)
