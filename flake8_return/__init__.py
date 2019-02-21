import ast
from typing import List, Optional

from flake8_plugin_utils import Error, Plugin, Visitor

__version__ = '0.2.0'


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


class ReturnVisitor(Visitor):
    def __init__(self) -> None:
        super().__init__()
        self._returns_stack: List[List[ast.Return]] = []

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._returns_stack.append([])
        self.generic_visit(node)
        return_nodes = self._returns_stack.pop()

        if not return_nodes:
            return

        if self._result_exists(return_nodes):
            self._check_implicit_return_value(return_nodes)
            self._check_implicit_return(node.body[-1])

        else:
            self._check_unnecessary_return_none(return_nodes)

    def visit_Return(self, node: ast.Return) -> None:
        self._returns_stack[-1].append(node)

    def _result_exists(self, nodes: List[ast.Return]) -> bool:
        for node in nodes:
            value = node.value
            if value and not _is_none(value):
                return True
        return False

    def _check_implicit_return_value(self, nodes: List[ast.Return]) -> None:
        for node in nodes:
            if not node.value:
                self.error_from_node(ImplicitReturnValue, node)

    def _check_unnecessary_return_none(self, nodes: List[ast.Return]) -> None:
        for node in nodes:
            if _is_none(node.value):
                self.error_from_node(UnnecessaryReturnNone, node)

    def _check_implicit_return(self, last_node: ast.AST) -> None:
        if isinstance(last_node, ast.If):
            if not last_node.body or not last_node.orelse:
                self.error_from_node(ImplicitReturn, last_node)
                return

            self._check_implicit_return(last_node.body[-1])
            self._check_implicit_return(last_node.orelse[-1])
            return

        if isinstance(last_node, ast.For) and last_node.orelse:
            self._check_implicit_return(last_node.orelse[-1])
            return

        if not isinstance(
            last_node, (ast.Return, ast.Raise, ast.While, ast.Try)
        ):
            self.error_from_node(ImplicitReturn, last_node)


def _is_none(node: Optional[ast.AST]) -> bool:
    return isinstance(node, ast.NameConstant) and node.value is None


class ReturnPlugin(Plugin):
    name = 'flake8-return'
    version = __version__
    visitors = [ReturnVisitor]
