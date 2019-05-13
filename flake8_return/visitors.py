import ast
from collections import defaultdict
from typing import Any, Dict, List, Optional, Union

from flake8_plugin_utils import Visitor

from .errors import (
    ImplicitReturn,
    ImplicitReturnValue,
    UnnecessaryAssign,
    UnnecessaryReturnNone,
)
from .utils import is_false, is_none

NameToLines = Dict[str, List[int]]
Function = Union[ast.AsyncFunctionDef, ast.FunctionDef]

ASSIGNS = 'assigns'
REFS = 'refs'
RETURNS = 'returns'


class ReturnVisitor(Visitor):
    def __init__(self) -> None:
        super().__init__()
        self._stack: List[Any] = []

    @property
    def assigns(self) -> NameToLines:
        return self._stack[-1][ASSIGNS]

    @property
    def refs(self) -> NameToLines:
        return self._stack[-1][REFS]

    @property
    def returns(self) -> List[ast.Return]:
        return self._stack[-1][RETURNS]

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._visit_with_stask(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._visit_with_stask(node)

    def _visit_with_stask(self, node: Function) -> None:
        self._stack.append(
            {ASSIGNS: defaultdict(list), REFS: defaultdict(list), RETURNS: []}
        )
        self.generic_visit(node)
        self._check_function(node)
        self._stack.pop()

    def visit_Return(self, node: ast.Return) -> None:
        self.returns.append(node)
        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign) -> None:
        if not self._stack:
            return

        self.generic_visit(node.value)

        target = node.targets[0]
        if isinstance(target, ast.Tuple) and not isinstance(
            node.value, ast.Tuple
        ):
            # skip unpacking assign e.g: x, y = my_object
            return

        self._visit_assign_target(target)

    def _visit_assign_target(self, node: ast.AST) -> None:
        if isinstance(node, ast.Tuple):
            for n in node.elts:
                self._visit_assign_target(n)
            return

        if isinstance(node, ast.Name):
            self.assigns[node.id].append(node.lineno)
            return

        # get item, etc.
        self.generic_visit(node)

    def visit_Name(self, node: ast.Name) -> None:
        if self._stack:
            self.refs[node.id].append(node.lineno)

    def _check_function(self, node: Function) -> None:
        if not self.returns or not node.body:
            return

        if len(node.body) == 1 and isinstance(node.body[-1], ast.Return):
            # skip functions that consist only `return None`
            return

        if not self._result_exists():
            self._check_unnecessary_return_none()
            return

        self._check_implicit_return_value()
        self._check_implicit_return(node.body[-1])

        for n in self.returns:
            if n.value:
                self._check_unnecessary_assign(n.value)

    def _result_exists(self) -> bool:
        for node in self.returns:
            value = node.value
            if value and not is_none(value):
                return True
        return False

    def _check_implicit_return_value(self) -> None:
        for node in self.returns:
            if not node.value:
                self.error_from_node(ImplicitReturnValue, node)

    def _check_unnecessary_return_none(self) -> None:
        for node in self.returns:
            if is_none(node.value):
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

        if isinstance(last_node, ast.With):
            self._check_implicit_return(last_node.body[-1])
            return

        if isinstance(last_node, ast.Assert) and is_false(last_node.test):
            return

        if not isinstance(
            last_node, (ast.Return, ast.Raise, ast.While, ast.Try)
        ):
            self.error_from_node(ImplicitReturn, last_node)

    def _check_unnecessary_assign(self, node: ast.AST) -> None:
        if not isinstance(node, ast.Name):
            return

        var_name = node.id
        return_lineno = node.lineno

        if var_name not in self.assigns:
            return

        if var_name not in self.refs:
            self.error_from_node(UnnecessaryAssign, node)
            return

        if self._has_refs_before_next_assign(var_name, return_lineno):
            return

        self.error_from_node(UnnecessaryAssign, node)

    def _has_refs_before_next_assign(
        self, var_name: str, return_lineno: int
    ) -> bool:
        before_assign = 0
        after_assign: Optional[int] = None

        for lineno in sorted(self.assigns[var_name]):
            if lineno > return_lineno:
                after_assign = lineno
                break

            if lineno <= return_lineno:
                before_assign = lineno

        for lineno in self.refs[var_name]:
            if lineno == return_lineno:
                continue

            if after_assign:
                if before_assign < lineno <= after_assign:
                    return True

            elif before_assign < lineno:
                return True

        return False
