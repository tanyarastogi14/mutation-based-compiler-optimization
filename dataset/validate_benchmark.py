from dataset.schema import BenchmarkProgram
from dataset.program_executor import execute_program

REQUIRED_CATEGORIES = {
    "zero_add",
    "one_mul",
    "constant_expr",
    "strength_reduce",
    "dead_assignment",
    "common_subexpression",
    "constant_propagation",
    "independent_ops",
    "mixed",
}


def validate_benchmark(benchmark: BenchmarkProgram) -> list[str]:
    """Return a list of validation errors."""

    errors = []

    if not benchmark.id:
        errors.append("Missing benchmark ID.")

    if benchmark.category not in REQUIRED_CATEGORIES:
        errors.append(
            f"Unknown category: {benchmark.category}"
        )

    if not benchmark.source_code.strip():
        errors.append("Source code is empty.")

    if not benchmark.parameters:
        errors.append("No parameters found.")

    if len(benchmark.test_inputs) != len(
        benchmark.expected_outputs
    ):
        errors.append(
            "Number of test inputs does not match "
            "number of expected outputs."
        )

    if len(benchmark.test_inputs) == 0:
        errors.append("No test inputs found.")

    for index, test_input in enumerate(benchmark.test_inputs):
        missing_parameters = [
            parameter
            for parameter in benchmark.parameters
            if parameter not in test_input
        ]

        if missing_parameters:
            errors.append(
                f"Test input {index} is missing parameters: "
                f"{missing_parameters}"
            )

    if not benchmark.optimization_opportunities:
        errors.append(
            "No optimization opportunities recorded."
        )

    for index, test_input in enumerate(benchmark.test_inputs):
        try:
            actual_output = execute_program(
                source_code=benchmark.source_code,
                test_input=test_input,
            )

            expected_output = benchmark.expected_outputs[index]

            if actual_output != expected_output:
                errors.append(
                    f"Test case {index} has incorrect expected output: "
                    f"stored={expected_output}, "
                    f"actual={actual_output}"
                )

        except Exception as error:
            errors.append(
                f"Test case {index} could not be executed: {error}"
            )

    return errors