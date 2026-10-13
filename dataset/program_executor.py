import re

from dataset.reference_executor import evaluate_expression


def execute_program(
    source_code: str,
    test_input: dict[str, int],
) -> int:
    """Execute a restricted straight-line C program."""

    variables = dict(test_input)

    statements = re.findall(
        r"(\w+)\s*=\s*(.*?);",
        source_code,
    )

    for variable, expression in statements:
        variables[variable] = evaluate_expression(
            expression,
            variables,
        )

    return_matches = re.findall(
        r"return\s+(\w+)\s*;",
        source_code,
    )

    if len(return_matches) != 1:
        raise ValueError(
            "Program must contain exactly one return statement."
        )

    return_variable = return_matches[0]

    if return_variable not in variables:
        raise ValueError(
            f"Unknown return variable: {return_variable}"
        )

    return variables[return_variable]