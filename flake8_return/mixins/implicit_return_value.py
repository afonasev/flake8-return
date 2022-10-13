from flake8_plugin_utils import Visitor

from ..errors import ImplicitReturnValue


class ImplicitReturnValueMixin(Visitor):
    def _check_implicit_return_value(self) -> None:
        for node in self.returns:
            if not node.value:
                self.error_from_node(ImplicitReturnValue, node)
