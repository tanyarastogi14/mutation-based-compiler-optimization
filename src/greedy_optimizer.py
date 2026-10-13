from src.mutations import MutationEngine
from src.validator import CandidateValidator
from src.cost import CostModel


class GreedyOptimizer:

    def __init__(self):
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
        current = original_tac

        original_components = (
            self.cost_model.calculate_components(
                original_tac
            )
        )

        current_cost = self.cost_model.calculate(
            current,
            reference_components=original_components,
        )

        history = [
            {
                "iteration": 0,
                "cost": current_cost,
                "operator": None,
            }
        ]

        for iteration in range(1, max_iterations + 1):

            mutation_candidates = (
                self.mutation_engine.apply_all(current)
            )

            best_candidate = None
            best_cost = current_cost
            best_operator = None

            for operator, candidates in mutation_candidates.items():

                for candidate in candidates:

                    valid = self.validator.validate(
                        candidate,
                        test_inputs,
                        expected_outputs,
                    )

                    if not valid:
                        continue

                    candidate_cost = (
                        self.cost_model.calculate(
                            candidate,
                            reference_components=original_components,
                        )
                    )

                    if candidate_cost < best_cost:
                        best_candidate = candidate
                        best_cost = candidate_cost
                        best_operator = operator

            if best_candidate is None:
                break

            current = best_candidate
            current_cost = best_cost

            history.append(
                {
                    "iteration": iteration,
                    "cost": current_cost,
                    "operator": best_operator,
                }
            )

        return {
            "optimized_tac": current,
            "original_cost": history[0]["cost"],
            "final_cost": current_cost,
            "iterations": len(history) - 1,
            "history": history,
        }