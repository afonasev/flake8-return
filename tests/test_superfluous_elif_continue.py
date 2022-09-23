import pytest
from flake8_plugin_utils import assert_error

from flake8_return.errors import SuperfluousElifContinue
from flake8_return.visitors import ReturnVisitor

from . import ids

superfluous_elif = (
    """
    def foo2(x, y, w, z):
        for i in x:
            if i < y:  # [no-else-continue]
                continue
            elif i < w:
                continue
            else:
                a = z
    """,
    """
    def foo5(x, y, z):
        for i in x:
            if i < y:  # [no-else-continue]
                if y:
                    a = 4
                else:
                    b = 2
                continue
            elif z:
                c = 2
            else:
                c = 3
            continue
    """,
)


@pytest.mark.parametrize('src', superfluous_elif, ids=ids(superfluous_elif))
def test_superfluous_elif_continue(src):
    assert_error(ReturnVisitor, src, SuperfluousElifContinue)
