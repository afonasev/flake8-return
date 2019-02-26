import pytest
from flake8_plugin_utils import assert_error

from flake8_return.errors import UnnecessaryReturnNone
from flake8_return.visitors import ReturnVisitor

from . import ids

unnecessary_return_none = (
    """
    def x(y):
        if not y:
            return
        return None  # here
    """,
)


@pytest.mark.parametrize(
    'src', unnecessary_return_none, ids=ids(unnecessary_return_none)
)
def test_unnecessary_return_none(src):
    assert_error(ReturnVisitor, src, UnnecessaryReturnNone)
