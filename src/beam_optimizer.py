from src.mutations import MutationEngine
from src.validator import CandidateValidator
from src.cost import CostModel


class BeamOptimizer:

    def __init__(self, beam_width=3):
        self.beam_width = beam_width
        self.mutation_engine = MutationEngine()
        self.validator = CandidateValidator()
        self.cost_model = CostModel()

    def optimize(
        self,
        original_tac,
        test_inputs,
        expected_outputs,
        max_iterations=20,
    ):
        original_components = (
            self.cost_model.calculate_components(original_tac)
        )

        original_cost = self.cost_model.calculate(
            original_tac,
            reference_components=original_components,
        )

        beam = [
            {
                "instructions": original_tac,
                "cost": original_cost,
                "history": [],
            }
        ]

        best_program = original_tac
        best_cost = original_cost
        best_history = []

        explored = 0
        visited = {
            tuple(str(i) for i in original_tac)
        }

        for iteration in range(1, max_iterations + 1):

            expanded = []

            for state in beam:

                candidates = self.mutation_engine.apply_all(
                    state["instructions"]
                )

                for operator, operator_candidates in candidates.items():

                    for candidate in operator_candidates:

                        key = tuple(
                            str(i) for i in candidate
                        )

                        if key in visited:
                            continue

                        visited.add(key)
                        explored += 1

                        if not self.validator.validate(
                            candidate,
                            test_inputs,
                            expected_outputs,
                        ):
                            continue

                        candidate_cost = self.cost_model.calculate(
                            candidate,
                            reference_components=original_components,
                        )

                        expanded.append({
                            "instructions": candidate,
                            "cost": candidate_cost,
                            "history": state["history"] + [operator],
                        })

            if not expanded:
                break

            expanded.sort(
                key=lambda state: state["cost"]
            )

            beam = expanded[:self.beam_width]

            # Update global best independently of beam continuation.
            if beam[0]["cost"] < best_cost:
                best_program = beam[0]["instructions"]
                best_cost = beam[0]["cost"]
                best_history = beam[0]["history"]

        return {
            "optimized_tac": best_program,
            "original_cost": original_cost,
            "final_cost": best_cost,
            "iterations": len(best_history),
            "history": best_history,
            "explored_candidates": explored,
            "beam_width": self.beam_width,
        }