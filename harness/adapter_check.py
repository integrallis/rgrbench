"""Static no-cheating constraints for adapter modules.

An adapter maps the candidate's API onto the oracle's expected names. Anything that could
carry domain behavior is rejected: control flow, operators, comprehensions, lambdas with
bodies beyond a call, and oversized modules. Delegation is structural, so the whitelist is
structural.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass, field

MAX_ADAPTER_LINES = 120

FORBIDDEN_NODES = (
    ast.If, ast.For, ast.While, ast.Try, ast.With,
    ast.BinOp, ast.BoolOp, ast.UnaryOp, ast.Compare, ast.IfExp,
    ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp,
    ast.Match, ast.Raise, ast.Assert, ast.Global, ast.Nonlocal,
    ast.AugAssign, ast.NamedExpr, ast.Subscript, ast.Slice,
)


@dataclass
class AdapterVerdict:
    ok: bool
    violations: list[str] = field(default_factory=list)


def check_adapter_source(source: str, filename: str = "<adapter>") -> AdapterVerdict:
    violations: list[str] = []
    if len(source.splitlines()) > MAX_ADAPTER_LINES:
        violations.append(f"{filename}: exceeds {MAX_ADAPTER_LINES} lines")
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        return AdapterVerdict(False, [f"{filename}: syntax error: {e}"])

    for node in ast.walk(tree):
        if isinstance(node, FORBIDDEN_NODES):
            violations.append(
                f"{filename}:{getattr(node, 'lineno', '?')}: "
                f"forbidden construct {type(node).__name__}"
            )
        if isinstance(node, ast.Constant) and not isinstance(
            node.value, (str, type(None), bool)
        ):
            # numeric or bytes constants smuggle domain values into the mapping
            violations.append(
                f"{filename}:{node.lineno}: non-trivial constant {node.value!r}"
            )
        if isinstance(node, ast.Lambda) and not isinstance(node.body, ast.Call):
            violations.append(
                f"{filename}:{node.lineno}: lambda body must be a single call"
            )
    return AdapterVerdict(not violations, violations)
