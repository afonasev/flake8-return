import ast
from typing import List

from flake8_plugin_utils import Error, Plugin, Visitor

__version__ = '0.1.1'


class UnnecessaryReturnNone(Error):
    code = 'R501'
    message = (
        'you shouldn`t add None at any return '
        'if function havn`t return value except None'
    )


class ImpliciteReturnValue(Error):
    code = 'R502'
    message = (
        'you should add explicite value at every return '
        'if function have return value except None'
    )


class ImpliciteReturn(Error):
    code = 'R503'
    message = (
        'you should add explicite return at end of the function '
        'if function have return value except None'
    )


class ReturnVisitor(Visitor):
    def __init__(self) -> None:
        super().__init__()
        self._func_returns_stack: List[List[ast.Return]] = []

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._func_returns_stack.append([])
        self.generic_visit(node)
        returns = self._func_returns_stack.pop()
        if not returns:
            return
        self._check_returns(returns, node.body[-1])

    def visit_Return(self, node: ast.Return) -> None:
        self._func_returns_stack[-1].append(node)

    def _check_returns(
        self, returns: List[ast.Return], last_node: ast.AST
    ) -> None:
        without_value_returns: List[ast.Return] = []
        with_none_returns: List[ast.Return] = []

        result_exists = False
        for node in returns:
            value = node.value

            if value is None:
                without_value_returns.append(node)
            elif isinstance(value, ast.NameConstant) and value.value is None:
                with_none_returns.append(node)
            else:
                result_exists = True

        if result_exists:
            for node in without_value_returns:
                self.error_from_node(ImpliciteReturnValue, node)

            if not isinstance(last_node, ast.Return):
                self.error_from_node(ImpliciteReturn, last_node)

        else:
            for node in with_none_returns:
                self.error_from_node(UnnecessaryReturnNone, node)


class ReturnPlugin(Plugin):
    name = 'flake8-return'
    version = __version__
    visitors = [ReturnVisitor]
