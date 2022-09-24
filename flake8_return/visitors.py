import ast
from collections import defaultdict
from typing import Any, Dict, List, Union

from flake8_plugin_utils import Visitor

from .errors import (
    ImplicitReturn,
    ImplicitReturnValue,
    SuperfluousElseBreak,
    SuperfluousElseContinue,
    SuperfluousElseRaise,
    SuperfluousElseReturn,
    UnnecessaryReturnNone,
)
from .mixins.unnecessary_assign import UnnecessaryAssignMixin
from .stack_keys import ASSIGNS, ELIFS, IFS, LOOPS, REFS, RETURNS, TRIES
from .utils import is_false, is_none

NameToLines = Dict[str, List[int]]
BlockPosition = Dict[int, int]
Function = Union[ast.AsyncFunctionDef, ast.FunctionDef]
Loop = Union[ast.For, ast.AsyncFor, ast.While]


class UnnecessaryReturnNoneMixin(Visitor):
    def _check_unnecessary_return_none(self) -> None:
        for node in self.returns:
            if is_none(node.value):
                self.error_from_node(UnnecessaryReturnNone, node)


class ImplicitReturnValueMixin(Visitor):
    def _check_implicit_return_value(self) -> None:
        for node in self.returns:
            if not node.value:
                self.error_from_node(ImplicitReturnValue, node)


class ImplicitReturnMixin(Visitor):
    def _check_implicit_return(self, last_node: ast.AST) -> None:
        if isinstance(last_node, ast.If):
            if not last_node.body or not last_node.orelse:
                self.error_from_node(ImplicitReturn, last_node)
                return

            self._check_implicit_return(last_node.body[-1])
            self._check_implicit_return(last_node.orelse[-1])
            return

        if isinstance(last_node, (ast.For, ast.AsyncFor)) and last_node.orelse:
            self._check_implicit_return(last_node.orelse[-1])
            return

        if isinstance(last_node, (ast.With, ast.AsyncWith, ast.For)):
            self._check_implicit_return(last_node.body[-1])
            return

        if isinstance(last_node, ast.Assert) and is_false(last_node.test):
            return

        if not isinstance(
            last_node, (ast.Return, ast.Raise, ast.While, ast.Try)
        ):
            self.error_from_node(ImplicitReturn, last_node)


class SuperfluousReturnMixin(Visitor):
    superfluous_list = [
        (ast.Return, SuperfluousElseReturn),
        (ast.Break, SuperfluousElseBreak),
        (ast.Raise, SuperfluousElseRaise),
        (ast.Continue, SuperfluousElseContinue),
    ]

    @property
    def ifs(self) -> List[ast.If]:
        if len(self._stack) > 0:
            return self._stack[-1][IFS]
        return []

    @property
    def elifs(self) -> List[ast.If]:
        return self._stack[-1][ELIFS]

    def visit_If(self, node: ast.If) -> None:
        if len(node.orelse) == 1 and isinstance(node.orelse[0], ast.If):
            self.elifs.append(node)
        else:
            self.ifs.append(node)

        self.generic_visit(node)

    def _updated_error_message(self, message: str, check: str) -> str:
        message = message.replace("else", "[check]")
        message = message.replace("elif", "[check]")
        return message.replace("[check]", check)

    def _check_superfluous_else_node(self, node: ast.If, check: str) -> bool:
        for statement, error in self.superfluous_list:
            if any(isinstance(node, statement) for node in node.body):
                message = getattr(error, "message", "")
                message = self._updated_error_message(message, check)
                setattr(error, "message", message)  # noqa: B010
                self.error_from_node(error, node)
                return True

        return False

    def _check_superfluous_else(self) -> bool:
        for node in self.ifs:
            if not node.orelse:
                continue

            if self._check_superfluous_else_node(node, "else"):
                return True

        return False

    def _check_superfluous_elif(self) -> bool:
        for node in self.elifs:
            if self._check_superfluous_else_node(node, "elif"):
                return True

        return False


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
