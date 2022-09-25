import pytest
from flake8_plugin_utils import assert_error

from flake8_return.errors import SuperfluousElseReturn
from flake8_return.visitors import ReturnVisitor

from . import ids

superfluous_elif = (
    """
    def foo2(x, y, w, z):
        if x:  # [no-else-return]
            a = 1
            return y
        elif z:
            b = 2
            return w
        else:
            c = 3
            return z
    """,
    """
    def foo5(x, y, z):
        if x:   # [no-else-return]
            if y:
                a = 4
            else:
                b = 2
            return
        elif z:
            c = 2
        else:
            c = 3
        return
    """,
    """
    def foo2(x, y, w, z):
        if x:
            a = 1
        elif z:
            b = 2
        else:
            c = 3

        if x:  # [no-else-return]
            a = 1
            return y
        elif z:
            b = 2
            return w
        else:
            c = 3
            return z
    """
)


@pytest.mark.parametrize('src', superfluous_elif, ids=ids(superfluous_elif))
def test_superfluous_elif_return(src):
    assert_error(ReturnVisitor, src, SuperfluousElseReturn)
