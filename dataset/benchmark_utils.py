import random

from dataset.program_executor import execute_program
from dataset.test_inputs import generate_test_inputs


def generate_expected_outputs(
    source_code: str,
    parameters: list[str],
    rng: random.Random,
    count: int = 8,
) -> tuple[list[dict[str, int]], list[int]]:
    """Generate test inputs and compute expected outputs."""

    test_inputs = generate_test_inputs(
        parameters=parameters,
        rng=rng,
        count=count,
    )

    expected_outputs = [
        execute_program(
            source_code=source_code,
            test_input=test_input,
        )
        for test_input in test_inputs
    ]

    return test_inputs, expected_outputs