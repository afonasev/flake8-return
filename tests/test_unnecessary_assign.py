import pytest
from flake8_plugin_utils import assert_error, assert_not_error

from flake8_return.errors import UnnecessaryAssign
from flake8_return.visitors import ReturnVisitor

from . import ids

unnecessary_assign = (
    """
    def x():
        a = 1
        return a  # error
    """,
    """
    def x():
        b, a = 1, 2
        print(b)
        return a  # error
    """,
    """
    def x():
        a = 1
        print()
        return a  # error
    """,
    """
    def x():
        a = 1
        print(a)
        a = 2
        return a  # error
    """,
    """
    def x():
        a = 1
        if True:
            return a  # error
        a = 2
        print(a)
        return a
    """,
)


@pytest.mark.parametrize(
    'src', unnecessary_assign, ids=ids(unnecessary_assign)
)
def test_unnecessary_assign(src):
    assert_error(ReturnVisitor, src, UnnecessaryAssign)


error_not_exists = (
    """
    def x(y):
        a = 1
        print(a)
        return a
    """,
    """
    def x():
        a = 1
        if y:
            return a
        a = a + 2
        print(a)
        return a
    """,
    """
    def x():
        a = {}
        a['b'] = 2
        return a
    """,
    """
    def x():
        a = []
        a.append(2)
        return a
    """,
    """
    def x():
        a = lambda x: x
        a()
        return a
    """,
    # ignore unpacking
    """
    def x():
        b, a = [1, 2]
        return a
    """,
)


@pytest.mark.parametrize('src', error_not_exists, ids=ids(error_not_exists))
def test_error_not_exists(src):
    assert_not_error(ReturnVisitor, src)
