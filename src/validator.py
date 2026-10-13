from src.tac import TACInstruction
from src.tac_executor import execute_tac


class CandidateValidator:
    """Validate mutated TAC programs against reference outputs."""

    def validate(
        self,
        candidate: list[TACInstruction],
        test_inputs: list[dict[str, int]],
        expected_outputs: list[int],
    ) -> bool:
        """Return True only if every test case produces the expected output."""

        if len(test_inputs) != len(expected_outputs):
            return False

        for test_input, expected_output in zip(
            test_inputs,
            expected_outputs,
        ):
            try:
                actual_output = execute_tac(
                    candidate,
                    test_input,
                )
            except Exception:
                return False

            if actual_output != expected_output:
                return False

        return True