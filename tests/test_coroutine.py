import pytest
from flake8_plugin_utils import assert_error, assert_not_error

from flake8_return.errors import ImplicitReturn
from flake8_return.visitors import ReturnVisitor

from . import ids

coro_errors = (
    # if/elif/else
    """
    async def x(y):
        if not y:
            return 1
        await y # error
    """,
)


@pytest.mark.parametrize('src', coro_errors, ids=ids(coro_errors))
def test_coro_errors(src):
    assert_error(ReturnVisitor, src, ImplicitReturn)


error_not_exists = (
    """
    async def x(y):
        a = {}
        await a
        return a
    """,
)


@pytest.mark.parametrize('src', error_not_exists, ids=ids(error_not_exists))
def test_error_not_exists(src):
    assert_not_error(ReturnVisitor, src)
