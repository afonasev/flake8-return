import ast
from typing import List

from flake8_plugin_utils import Visitor

from ..errors import (
    SuperfluousElseBreak,
    SuperfluousElseContinue,
    SuperfluousElseRaise,
    SuperfluousElseReturn,
)
from ..stack_keys import ELIFS, IFS


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
        if len(self._stack) > 0:
            return self._stack[-1][ELIFS]
        return []

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
