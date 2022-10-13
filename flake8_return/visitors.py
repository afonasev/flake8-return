import ast
from collections import defaultdict
from typing import Any, List, Union

from .mixins.implicit_return import ImplicitReturnMixin
from .mixins.implicit_return_value import ImplicitReturnValueMixin
from .mixins.superfluous_return import SuperfluousReturnMixin
from .mixins.unnecessary_assign import UnnecessaryAssignMixin
from .mixins.unnecessary_return_none import UnnecessaryReturnNoneMixin
from .stack_keys import ASSIGNS, ELIFS, IFS, LOOPS, REFS, RETURNS, TRIES
from .utils import is_none

Function = Union[ast.AsyncFunctionDef, ast.FunctionDef]


class ReturnVisitor(
    SuperfluousReturnMixin,
    UnnecessaryAssignMixin,
    UnnecessaryReturnNoneMixin,
    ImplicitReturnMixin,
    ImplicitReturnValueMixin,
):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._stack: List[Any] = []

    @property
    def returns(self) -> List[ast.Return]:
        return self._stack[-1][RETURNS]

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._visit_with_stack(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._visit_with_stack(node)

    def _visit_with_stack(self, node: Function) -> None:
        self._stack.append(
            {
                ASSIGNS: defaultdict(list),
                REFS: defaultdict(list),
                TRIES: defaultdict(int),
                LOOPS: defaultdict(int),
                RETURNS: [],
                IFS: [],
                ELIFS: [],
            }
        )
        self.generic_visit(node)
        self._check_function(node)
        self._stack.pop()

    def visit_Return(self, node: ast.Return) -> None:
        self.returns.append(node)
        self.generic_visit(node)

    def _check_function(self, node: Function) -> None:
        if self._check_superfluous_elif() or self._check_superfluous_else():
            return
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
