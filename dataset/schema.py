from dataclasses import dataclass, field
from typing import Any


@dataclass
class OptimizationOpportunity:
    operator: str
    reason: str


@dataclass
class BenchmarkProgram:
    id: str
    dataset_version: str
    generator_version: str
    seed: int

    category: str
    difficulty: str

    source_code: str

    parameters: list[str]
    variables: list[str]

    test_inputs: list[dict[str, int]]
    expected_outputs: list[int]

    optimization_opportunities: list[OptimizationOpportunity] = field(
        default_factory=list
    )

    # Filled later by the compiler/optimization pipeline.
    tac: list[str] | None = None
    baseline_cost: float | None = None
    reference_program: str | None = None
    reference_cost: float | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "dataset_version": self.dataset_version,
            "generator_version": self.generator_version,
            "seed": self.seed,
            "category": self.category,
            "difficulty": self.difficulty,
            "source_code": self.source_code,
            "parameters": self.parameters,
            "variables": self.variables,
            "test_inputs": self.test_inputs,
            "expected_outputs": self.expected_outputs,
            "optimization_opportunities": [
                {
                    "operator": opportunity.operator,
                    "reason": opportunity.reason,
                }
                for opportunity in self.optimization_opportunities
            ],
            "tac": self.tac,
            "baseline_cost": self.baseline_cost,
            "reference_program": self.reference_program,
            "reference_cost": self.reference_cost,
        }