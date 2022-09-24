from flake8_plugin_utils import Error


class UnnecessaryReturnNone(Error):
    code = 'R501'
    message = (
        'do not explicitly return None in function if '
        'it is the only possible return value.'
    )


class ImplicitReturnValue(Error):
    code = 'R502'
    message = (
        'do not implicitly return None in function able '
        'to return non-None value.'
    )


class ImplicitReturn(Error):
    code = 'R503'
    message = (
        'missing explicit return at the end of function able '
        'to return non-None value.'
    )


class UnnecessaryAssign(Error):
    code = 'R504'
    message = 'unnecessary variable assignment before return statement.'


class SuperfluousElseReturn(Error):
    code = 'R505'
    message = 'unnecessary else after return statement.'


class SuperfluousElseRaise(Error):
    code = 'R506'
    message = 'unnecessary else after raise statement.'


class SuperfluousElseContinue(Error):
    code = 'R507'
    message = 'unnecessary else after continue statement.'


class SuperfluousElseBreak(Error):
    code = 'R508'
    message = 'unnecessary else after break statement.'
