import random

from dataset.benchmark_utils import generate_expected_outputs
from dataset.generator import CProgramGenerator
from dataset.schema import BenchmarkProgram


DATASET_VERSION = "1.0"
GENERATOR_VERSION = "1.0"


CATEGORY_OPERATORS = {
    "zero_add": ["M1"],
    "one_mul": ["M2"],
    "constant_expr": ["M3"],
    "strength_reduce": ["M4"],
    "dead_assignment": ["M5"],
    "common_subexpression": ["M6"],
    "constant_propagation": ["M7"],
    "independent_ops": ["M8"],
    "mixed": ["M1", "M3", "M4"],
}


def build_benchmark(
    program_id: str,
    category: str,
    seed: int,
    difficulty: str = "small",
) -> BenchmarkProgram:
    """Build one complete benchmark record."""

    generator = CProgramGenerator(seed=seed)

    source_code = generator.generate_program(
        category,
        size=difficulty,
    )

    parameters = _extract_parameters(source_code)
    variables = _extract_variables(source_code)

    rng = random.Random(seed + 1000)

    test_inputs, expected_outputs = generate_expected_outputs(
        source_code=source_code,
        parameters=parameters,
        rng=rng,
        count=8,
    )

    opportunities = [
        {
            "operator": operator,
            "reason": f"Generated {category} opportunity.",
        }
        for operator in CATEGORY_OPERATORS[category]
    ]

    from dataset.schema import OptimizationOpportunity

    optimization_opportunities = [
        OptimizationOpportunity(
            operator=item["operator"],
            reason=item["reason"],
        )
        for item in opportunities
    ]

    return BenchmarkProgram(
        id=program_id,
        dataset_version=DATASET_VERSION,
        generator_version=GENERATOR_VERSION,
        seed=seed,
        category=category,
        difficulty=difficulty,
        source_code=source_code,
        parameters=parameters,
        variables=variables,
        test_inputs=test_inputs,
        expected_outputs=expected_outputs,
        optimization_opportunities=optimization_opportunities,
    )


def _extract_parameters(source_code: str) -> list[str]:
    """Extract parameter names from the compute function."""

    header = source_code.split("{", 1)[0]

    parameter_text = header.split("(", 1)[1].split(")", 1)[0].strip()

    if not parameter_text:
        return []

    parameters = []

    for parameter in parameter_text.split(","):
        parts = parameter.strip().split()
        parameters.append(parts[-1])

    return parameters


def _extract_variables(source_code: str) -> list[str]:
    """Extract local integer variable declarations."""

    variables = []

    for line in source_code.splitlines():
        line = line.strip()

        if line.startswith("int ") and line.endswith(";"):
            declaration = line[4:-1].strip()

            if "=" not in declaration:
                variables.append(declaration)

    return variables