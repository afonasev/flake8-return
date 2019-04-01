import pytest
from flake8_plugin_utils import assert_error, assert_not_error

from flake8_return.errors import ImplicitReturn
from flake8_return.visitors import ReturnVisitor

from . import ids

implicit_return = (
    # if/elif/else
    """
    def x(y):
        if not y:
            return 1
        # error
    """,
    """
    def x(y):
        if not y:
            print()  # error
        else:
            return 2
    """,
    """
    def x(y):
        if not y:
            return 1
        elif y - 100:
            print()  # error
        else:
            return 2
    """,
    """
    def x(y):
        if not y:
            return 1
        else:
            print()  # error
    """,
    # for
    """
    def x(y):
        for i in range(10):
            if i > 10:
                return i
        # error
    """,
    """
    def x(y):
        for i in range(10):
            if i > 10:
                return i
        else:
            print()  # error
    """,
)


@pytest.mark.parametrize('src', implicit_return, ids=ids(implicit_return))
def test_implicit_return(src):
    assert_error(ReturnVisitor, src, ImplicitReturn)


error_not_exists = (
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
    # exclude empty functions
    """
    def x(y):
        return None
    """,
    # return inner with statement
    """
    def x(y):
        with y:
            return 1
    """,
    # assert as last return
    """
    def x(y):
        if not y:
            return 1
        assert False, 'Sanity check'
    """,
)


@pytest.mark.parametrize('src', error_not_exists, ids=ids(error_not_exists))
def test_error_not_exists(src):
    assert_not_error(ReturnVisitor, src)