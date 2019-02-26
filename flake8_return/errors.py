from flake8_plugin_utils import Error


class UnnecessaryReturnNone(Error):
    code = 'R501'
    message = (
        'you shouldn`t add None at any return '
        'if function havn`t return value except None'
    )


class ImplicitReturnValue(Error):
    code = 'R502'
    message = (
        'you should add explicit value at every return '
        'if function have return value except None'
    )


class ImplicitReturn(Error):
    code = 'R503'
    message = (
        'you should add explicit return at end of the function '
        'if function have return value except None'
    )


class UnnecessaryAssign(Error):
    code = 'R504'
    message = (
        'you shouldn`t assign value to variable '
        'if it will be use only as return value'
    )
