import ast
import sys
from typing import Any, Dict, List, Optional, Union

from flake8_plugin_utils import Visitor

from ..errors import UnnecessaryAssign

NameToLines = Dict[str, List[int]]
BlockPosition = Dict[int, int]
Loop = Union[ast.For, ast.AsyncFor, ast.While]


class UnnecessaryAssignMixin(Visitor):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._loop_count: int = 0

    @property
    def assigns(self) -> NameToLines:
        return self._stack[-1]['assigns']

    @property
    def refs(self) -> NameToLines:
        return self._stack[-1]['refs']

    @property
    def tries(self) -> BlockPosition:
        return self._stack[-1]['tries']

    @property
    def loops(self) -> BlockPosition:
        return self._stack[-1]['loops']

    def visit_For(self, node: ast.For) -> None:
        self._visit_loop(node)

    def visit_AsyncFor(self, node: ast.AsyncFor) -> None:
        self._visit_loop(node)

    def visit_While(self, node: ast.While) -> None:
        self._visit_loop(node)

    def _visit_loop(self, node: Loop) -> None:
        if sys.version_info >= (3, 8):
            if self._stack:
                if hasattr(node, "end_lineno") and node.end_lineno is not None:
                    self.loops[node.lineno] = node.end_lineno
            self.generic_visit(node)
        else:
            self._loop_count += 1
            self.generic_visit(node)
            self._loop_count -= 1

    def visit_Assign(self, node: ast.Assign) -> None:
        if not self._stack:
            return

        if isinstance(node.value, ast.Name):
            self.refs[node.value.id].append(node.value.lineno)

        self.generic_visit(node.value)

        target = node.targets[0]
        if isinstance(target, ast.Tuple) and not isinstance(
            node.value, ast.Tuple
        ):
            # skip unpacking assign e.g: x, y = my_object
            return

        self._visit_assign_target(target)

    def visit_Name(self, node: ast.Name) -> None:
        if self._stack:
            self.refs[node.id].append(node.lineno)

    def visit_Try(self, node: ast.Try) -> None:
        if sys.version_info >= (3, 8):
            if self._stack:
                if hasattr(node, "end_lineno") and node.end_lineno is not None:
                    self.tries[node.lineno] = node.end_lineno
        self.generic_visit(node)

    def _visit_assign_target(self, node: ast.AST) -> None:
        if isinstance(node, ast.Tuple):
            for n in node.elts:
                self._visit_assign_target(n)
            return

        if sys.version_info >= (3, 8) or not self._loop_count:
            if isinstance(node, ast.Name):
                self.assigns[node.id].append(node.lineno)
                return

        # get item, etc.
        self.generic_visit(node)

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

        if sys.version_info >= (3, 8):
            if self._has_refs_or_assigns_within_try_or_loop(var_name):
                return

        self.error_from_node(UnnecessaryAssign, node)

    def _has_refs_or_assigns_within_try_or_loop(self, var_name: str) -> bool:
        for item in [*self.refs[var_name], *self.assigns[var_name]]:
            for try_start, try_end in self.tries.items():
                if try_start < item <= try_end:
                    return True

            for loop_start, loop_end in self.loops.items():
                if loop_start < item <= loop_end:
                    return True

        return False

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
