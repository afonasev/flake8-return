import pytest
from flake8_plugin_utils import get_error

from flake8_return import (
    ImplicitReturn,
    ImplicitReturnValue,
    ReturnPlugin,
    UnnecessaryReturnNone,
)


@pytest.mark.parametrize(
    'src',
    (
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
    else:
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
        # noqa
        f"""
def x(y):
    if not y:
        return  # noqa:{ImplicitReturnValue.code}
    return 1
    """,
        f"""
def x(y):
    if not y:
        return
    return None  # noqa:{UnnecessaryReturnNone.code}
    """,
        # raise as last return
        f"""
def x(y):
    if not y:
        return 1
    raise Exception
    """,
        # last line in while loop
        f"""
def x(y):
    while True:
        if y > 0:
            return 1
        y += 1
    """,
    ),
)
def test_error_not_exists(tmpdir, src):
    assert not get_error(ReturnPlugin, tmpdir, src)


@pytest.mark.parametrize(
    'src',
    (
        f"""
def x(y):
    if not y:
        return
    return 1
    """,
    ),
)
def test_implicit_return_value(tmpdir, src):
    _assert_error(tmpdir, src, ImplicitReturnValue)


@pytest.mark.parametrize(
    'src',
    (
        f"""
def x(y):
    if not y:
        return
    return None
    """,
    ),
)
def test_unnecessary_return_none(tmpdir, src):
    _assert_error(tmpdir, src, UnnecessaryReturnNone)


@pytest.mark.parametrize(
    'src',
    (
        f"""
def x(y):
    if not y:
        return 1
    """,
        """
def x(y):
    if not y:
        print()
    else:
        return 2
    """,
        """
def x(y):
    if not y:
        return 1
    elif y - 100:
        print()
    else:
        return 2
    """,
        """
def x(y):
    if not y:
        return 1
    else:
        print()
    """,
    ),
)
def test_implicit_return(tmpdir, src):
    _assert_error(tmpdir, src, ImplicitReturn)


def _assert_error(tmpdir, src, error):
    assert get_error(ReturnPlugin, tmpdir, src).endswith(error.message)
