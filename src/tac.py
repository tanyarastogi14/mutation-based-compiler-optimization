from dataclasses import dataclass


@dataclass
class TACInstruction:
    """One three-address-code instruction."""

    result: str | None
    arg1: str | None
    operator: str | None
    arg2: str | None

    def __str__(self) -> str:
        if self.operator == "return":
            return f"return {self.arg1}"

        if self.operator is None:
            if self.result is None:
                return ""
            return f"{self.result} = {self.arg1}"

        return (
            f"{self.result} = "
            f"{self.arg1} {self.operator} {self.arg2}"
        )