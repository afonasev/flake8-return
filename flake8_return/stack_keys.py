import ast
from typing import Optional


def is_none(node: Optional[ast.AST]) -> bool:
    return isinstance(node, ast.NameConstant) and node.value is None


def is_false(node: Optional[ast.AST]) -> bool:
    return isinstance(node, ast.NameConstant) and node.value is False


ASSIGNS = 'assigns'
REFS = 'refs'
RETURNS = 'returns'
TRIES = 'tries'
LOOPS = 'loops'
IFS = 'ifs'
ELIFS = 'elifs'
