from src.cost import CostModel
from src.validator import CandidateValidator
from src.tac import TACInstruction


class CandidateEvaluator:
    """Validate and score mutation candidates."""

    def __init__(self):
        self.validator = CandidateValidator()
        self.cost_model = CostModel()

    def evaluate(
        self,
        candidates: dict[str, list[list[TACInstruction]]],
        test_inputs: list[dict[str, int]],
        expected_outputs: list[int],
        original_tac: list[TACInstruction],
    ) -> list[dict]:
        """Validate and score every generated candidate."""

        original_components = (
            self.cost_model.calculate_components(original_tac)
        )

        evaluated_candidates = []

        for operator, operator_candidates in candidates.items():
            for candidate in operator_candidates:
                valid = self.validator.validate(
                    candidate=candidate,
                    test_inputs=test_inputs,
                    expected_outputs=expected_outputs,
                )

                if not valid:
                    continue

                cost = self.cost_model.calculate(
                    instructions=candidate,
                    reference_components=original_components,
                )

                evaluated_candidates.append(
                    {
                        "operator": operator,
                        "instructions": candidate,
                        "cost": cost,
                        "valid": True,
                    }
                )

        return evaluated_candidates