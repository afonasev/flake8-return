import ast
from collections import defaultdict
from typing import Any, Dict, List, Optional

from flake8_plugin_utils import Visitor

from .errors import (
    ImplicitReturn,
    ImplicitReturnValue,
    UnnecessaryAssign,
    UnnecessaryReturnNone,
)

NameToLines = Dict[str, List[int]]

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

        for target in node.targets:
            if isinstance(target, ast.Name):
                self.assigns[target.id].append(node.lineno)
            else:
                # visit not Name node, e.g. d['key']
                self.generic_visit(target)

        self.generic_visit(node.value)

    def visit_Name(self, node: ast.Name) -> None:
        if self._stack:
            self.refs[node.id].append(node.lineno)

    def _check_function(self, node: ast.FunctionDef) -> None:
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
        self._check_unnecessary_assign()

    def _result_exists(self) -> bool:
        for node in self.returns:
            value = node.value
            if value and not _is_none(value):
                return True
        return False

    def _check_implicit_return_value(self) -> None:
        for node in self.returns:
            if not node.value:
                self.error_from_node(ImplicitReturnValue, node)

    def _check_unnecessary_return_none(self) -> None:
        for node in self.returns:
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

        if isinstance(last_node, ast.With):
            self._check_implicit_return(last_node.body[-1])
            return

        if not isinstance(
            last_node, (ast.Return, ast.Raise, ast.While, ast.Try)
        ):
            self.error_from_node(ImplicitReturn, last_node)

    def _check_unnecessary_assign(self) -> None:
        for node in self.returns:
            if not isinstance(node.value, ast.Name):
                continue

            var_name = node.value.id
            return_lineno = node.lineno

            if var_name not in self.assigns:
                continue

            if var_name not in self.refs:
                self.error_from_node(UnnecessaryAssign, node)
                continue

            if self._has_refs_before_next_assign(var_name, return_lineno):
                continue

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


def _is_none(node: Optional[ast.AST]) -> bool:
    return isinstance(node, ast.NameConstant) and node.value is None
