import ast


def evaluate_expression(
    expression: str,
    variables: dict[str, int],
) -> int:
    """Safely evaluate a restricted arithmetic expression."""

    tree = ast.parse(expression, mode="eval")

    return _evaluate_node(tree.body, variables)


def _evaluate_node(
    node: ast.AST,
    variables: dict[str, int],
) -> int:
    if isinstance(node, ast.Constant):
        if isinstance(node.value, int):
            return node.value

        raise ValueError("Only integer constants are supported.")

    if isinstance(node, ast.Name):
        if node.id not in variables:
            raise ValueError(f"Unknown variable: {node.id}")

        return variables[node.id]

    if isinstance(node, ast.BinOp):
        left = _evaluate_node(node.left, variables)
        right = _evaluate_node(node.right, variables)

        if isinstance(node.op, ast.Add):
            return left + right

        if isinstance(node.op, ast.Sub):
            return left - right

        if isinstance(node.op, ast.Mult):
            return left * right

        if isinstance(node.op, ast.Div):
            if right == 0:
                raise ValueError("Division by zero.")

            return int(left / right)

    raise ValueError(
        f"Unsupported expression node: {type(node).__name__}"
    )