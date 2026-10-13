from src.tac import TACInstruction


def execute_tac(
    instructions: list[TACInstruction],
    inputs: dict[str, int],
) -> int:
    """Execute TAC and return the program's output."""

    variables = dict(inputs)

    for instruction in instructions:
        if instruction.operator == "return":
            value = _get_value(instruction.arg1, variables)
            return value

        if instruction.operator is None:
            value = _get_value(instruction.arg1, variables)
            variables[instruction.result] = value
            continue

        left = _get_value(instruction.arg1, variables)
        right = _get_value(instruction.arg2, variables)

        if instruction.operator == "+":
            result = left + right

        elif instruction.operator == "-":
            result = left - right

        elif instruction.operator == "*":
            result = left * right

        elif instruction.operator == "/":
            if right == 0:
                raise ValueError("Division by zero.")

            result = int(left / right)

        else:
            raise ValueError(
                f"Unsupported operator: {instruction.operator}"
            )

        variables[instruction.result] = result

    raise ValueError("TAC contains no return instruction.")


def _get_value(
    value: str | None,
    variables: dict[str, int],
) -> int:
    if value is None:
        raise ValueError("Missing TAC operand.")

    if value.lstrip("-").isdigit():
        return int(value)

    if value not in variables:
        raise ValueError(
            f"Undefined TAC variable: {value}"
        )

    return variables[value]