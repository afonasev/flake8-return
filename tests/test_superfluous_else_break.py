import pytest
from flake8_plugin_utils import assert_error, assert_not_error

from flake8_return.errors import SuperfluousElseBreak
from flake8_return.visitors import ReturnVisitor

from . import ids

superfluous_else = (
    """
    def foo1(x, y, z):
        for i in x:
            if i > y:  # [no-else-break]
                break
            else:
                a = z
    """,
    """
    def foo3(x, y, z):
        for i in x:
            if i > y:
                a = 1
                if z:  # [no-else-break]
                    b = 2
                    break
                else:
                    c = 3
                    break
            else:
                d = 4
                break
    """,
    """
    def foo4(x, y):
        for i in x:
            if i > x:  # [no-else-break]
                if y:
                    a = 4
                else:
                    b = 2
                break
            else:
                c = 3
            break
    """,
    """
    def foo6(x, y):
        for i in x:
            if i > x:
                if y:  # [no-else-break]
                    a = 4
                    break
                else:
                    b = 2
            else:
                c = 3
            break
    """,
    """
    def bar4(x):
        for i in range(10):
            if x:  # [no-else-break]
                break
            else:
                try:
                    return
                except ValueError:
                    break
    """,
)


@pytest.mark.parametrize('src', superfluous_else, ids=ids(superfluous_else))
def test_superfluous_else_break(src):
    assert_error(ReturnVisitor, src, SuperfluousElseBreak)


error_not_exists = (
    """
    def bar1(x, y, z):
        for i in x:
            if i > y:
                break
            return z
    """,
    """
    def bar2(w, x, y, z):
        for i in w:
            if i > x:
                break
            if z < i:
                a = y
            else:
                break
            return
    """,
    """
    def bar3(x, y, z):
        for i in x:
            if i > y:
                if z:
                    break
            else:
                return z
            return None
    """,
    """
    def nested1(x, y, z):
        for i in x:
            if i > x:
                for j in y:
                    if j < z:
                        break
            else:
                a = z
    """,
    """
    def nested2(x, y, z):
        for i in x:
            if i > x:
                for j in y:
                    if j > z:
                        break
                    break
            else:
                a = z
    """,
)


@pytest.mark.parametrize('src', error_not_exists, ids=ids(error_not_exists))
def test_error_not_exists(src):
    assert_not_error(ReturnVisitor, src)
