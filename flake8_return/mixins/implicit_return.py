import ast

from flake8_plugin_utils import Visitor

from ..errors import ImplicitReturn
from ..utils import is_false


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

        if isinstance(last_node, ast.Match):
            # We need at least one catch-all case, otherwise we'll consider
            # the match to be non-exhaustive and therefore fail the linter
            if not any(
                isinstance(case.pattern, ast.MatchAs)
                and not case.pattern.pattern
                for case in last_node.cases
            ):
                self.error_from_node(ImplicitReturn, last_node)

            # Every entry of the match statement must have an explicit return
            for case in last_node.cases:
                self._check_implicit_return(case.body[-1])
            return

        if not isinstance(
            last_node, (ast.Return, ast.Raise, ast.While, ast.Try)
        ):
            self.error_from_node(ImplicitReturn, last_node)
