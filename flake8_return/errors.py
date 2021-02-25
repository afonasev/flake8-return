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
        'missing explicit return at the  end of function able'
        'to return non-None value.'
    )


class UnnecessaryAssign(Error):
    code = 'R504'
    message = 'unecessary variable assignement before return statement.'
