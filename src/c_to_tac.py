import re

from src.tac import TACInstruction
from src.tac_generator import TACGenerator


class CToTACCompiler:
    """Compile our restricted C programs into TAC."""

    def compile(self, source_code: str) -> list[TACInstruction]:
        generator = TACGenerator()

        lines = [
            line.strip()
            for line in source_code.splitlines()
            if line.strip()
        ]

        for line in lines:
            # Ignore function header, declarations, and closing brace.
            if line.startswith("int compute"):
                continue

            if line.startswith("int "):
                continue

            if line == "}":
                continue

            # Handle return statement.
            return_match = re.fullmatch(
                r"return\s+(\w+)\s*;",
                line,
            )

            if return_match:
                generator.generate_return(
                    return_match.group(1)
                )
                continue

            # Handle assignment.
            assignment_match = re.fullmatch(
                r"(\w+)\s*=\s*(.+);",
                line,
            )

            if assignment_match:
                variable = assignment_match.group(1)
                expression = assignment_match.group(2)

                generator.generate_assignment(
                    variable,
                    expression,
                )
                continue

            raise ValueError(
                f"Unsupported C statement: {line}"
            )

        return generator.instructions