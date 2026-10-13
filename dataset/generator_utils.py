import random


PARAMETER_NAMES = ["x", "y", "z", "w"]


VARIABLE_NAMES = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "value",
    "result",
    "temp",
    "temp1",
    "temp2",
    "temp3",
    "temp4",
    "temp5",
    "temp6",
    "temp7",
]

def choose_parameters(rng: random.Random, count: int) -> list[str]:
    """Choose distinct parameter names."""
    return rng.sample(PARAMETER_NAMES, count)


def choose_variable_names(
    rng: random.Random,
    count: int,
) -> list[str]:
    """Choose distinct local variable names."""
    return rng.sample(VARIABLE_NAMES, count)


def format_program(
    parameters: list[str],
    declarations: list[str],
    statements: list[str],
    return_variable: str,
) -> str:
    """Build a complete restricted-C program."""

    parameter_text = ", ".join(
        f"int {parameter}" for parameter in parameters
    )

    declaration_text = "\n".join(
        f"    int {variable};" for variable in declarations
    )

    statement_text = "\n".join(
        f"    {statement}" for statement in statements
    )

    return f"""int compute({parameter_text}) {{
{declaration_text}

{statement_text}

    return {return_variable};
}}"""