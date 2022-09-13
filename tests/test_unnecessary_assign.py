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

    # Incorrect false positives - can be refactored

    # https://github.com/afonasev/flake8-return/issues/47#issuecomment-1122571066
    """
    def get_bar_if_exists(obj):
        result = ""
        if hasattr(obj, "bar"):
            result = str(obj.bar)
        return result
    """,

    # https://github.com/afonasev/flake8-return/issues/47#issue-641117366
    """
    def x():
        formatted = _USER_AGENT_FORMATTER.format(format_string, **values)
        # clean up after any blank components
        formatted = formatted.replace('()', '').replace('  ', ' ').strip()
        return formatted
    """,

    # https://github.com/afonasev/flake8-return/issues/47#issue-641117366
    """
    def user_agent_username(username=None):

        if not username:
            return ''

        username = username.replace(' ', '_')  # Avoid spaces or %20.
        try:
            username.encode('ascii')  # just test, but not actually use it
        except UnicodeEncodeError:
            username = quote(username.encode('utf-8'))
        else:
            # % is legal in the default $wgLegalTitleChars
            # This is so that ops know the real pywikibot will not
            # allow a useragent in the username to allow through a hand-coded
            # percent-encoded value.
            if '%' in username:
                username = quote(username)
        return username
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
    """
    def x():
        val = ''
        for i in range(5):
            val = val + str(i)
        return val
    """,
    """
    def x():
        val = ''
        i = 5
        while i:
            val = val + str(i)
            i = i - x
        return val
    """,

    # Test cases for using value for assignment then returning it
    # See:https://github.com/afonasev/flake8-return/issues/47
    """
    def resolve_from_url(self, url: str) -> dict:
        local_match = self.local_scope_re.match(url)
        if local_match:
            schema = get_schema(name=local_match.group(1))
            self.store[url] = schema
            return schema
        raise NotImplementedError(...)
    """,
    """
    my_dict = {}

    def my_func():
        foo = calculate_foo()
        my_dict["foo_result"] = foo
        return foo
    """,

    # Refactored incorrect false positives
    # See test cases above marked: "Incorrect false positives - can be refactored"

    # https://github.com/afonasev/flake8-return/issues/47#issuecomment-1122571066
    """
    def get_bar_if_exists(obj):
        if hasattr(obj, "bar"):
            return str(obj.bar)
        return ""
    """,

    # https://github.com/afonasev/flake8-return/issues/47#issue-641117366
    """
    def x():
        formatted = _USER_AGENT_FORMATTER.format(format_string, **values)
        # clean up after any blank components
        return formatted.replace('()', '').replace('  ', ' ').strip()
    """,

    # https://github.com/afonasev/flake8-return/issues/47#issue-641117366
    """
    def user_agent_username(username=None):

        if not username:
            return ''

        username = username.replace(' ', '_')  # Avoid spaces or %20.
        try:
            username.encode('ascii')  # just test, but not actually use it
        except UnicodeEncodeError:
            username = quote(username.encode('utf-8'))
        else:
            # % is legal in the default $wgLegalTitleChars
            # This is so that ops know the real pywikibot will not
            # allow a useragent in the username to allow through a hand-coded
            # percent-encoded value.
            if '%' in username:
                return quote(username)
        finally:
            return username
    """,
)


@pytest.mark.parametrize('src', error_not_exists, ids=ids(error_not_exists))
def test_error_not_exists(src):
    assert_not_error(ReturnVisitor, src)
