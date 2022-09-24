from flake8_plugin_utils import Visitor

from ..errors import UnnecessaryReturnNone
from ..utils import is_none


class UnnecessaryReturnNoneMixin(Visitor):
    def _check_unnecessary_return_none(self) -> None:
        for node in self.returns:
            if is_none(node.value):
                self.error_from_node(UnnecessaryReturnNone, node)
