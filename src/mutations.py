from copy import deepcopy

from src.tac import TACInstruction


class MutationEngine:
    """Generate candidate TAC programs using mutation operators."""

    # ------------------------------------------------------------------
    # M1: Zero-Add Removal
    # ------------------------------------------------------------------

    def apply_m1_zero_add(
        self,
        instructions: list[TACInstruction],
    ) -> list[list[TACInstruction]]:
        """Replace x + 0 or 0 + x with a copy."""

        candidates = []

        for index, instruction in enumerate(instructions):
            if instruction.operator != "+":
                continue

            if instruction.arg2 == "0":
                candidate = deepcopy(instructions)

                candidate[index] = TACInstruction(
                    result=instruction.result,
                    arg1=instruction.arg1,
                    operator=None,
                    arg2=None,
                )

                candidates.append(candidate)

            elif instruction.arg1 == "0":
                candidate = deepcopy(instructions)

                candidate[index] = TACInstruction(
                    result=instruction.result,
                    arg1=instruction.arg2,
                    operator=None,
                    arg2=None,
                )

                candidates.append(candidate)

        return candidates

    # ------------------------------------------------------------------
    # M2: One-Multiplication Removal
    # ------------------------------------------------------------------

    def apply_m2_one_mul(
        self,
        instructions: list[TACInstruction],
    ) -> list[list[TACInstruction]]:
        """Replace x * 1 or 1 * x with a copy."""

        candidates = []

        for index, instruction in enumerate(instructions):
            if instruction.operator != "*":
                continue

            if instruction.arg2 == "1":
                candidate = deepcopy(instructions)

                candidate[index] = TACInstruction(
                    result=instruction.result,
                    arg1=instruction.arg1,
                    operator=None,
                    arg2=None,
                )

                candidates.append(candidate)

            elif instruction.arg1 == "1":
                candidate = deepcopy(instructions)

                candidate[index] = TACInstruction(
                    result=instruction.result,
                    arg1=instruction.arg2,
                    operator=None,
                    arg2=None,
                )

                candidates.append(candidate)

        return candidates

    # ------------------------------------------------------------------
    # M3: Constant Folding
    # ------------------------------------------------------------------

    def apply_m3_constant_folding(
        self,
        instructions: list[TACInstruction],
    ) -> list[list[TACInstruction]]:
        """Fold arithmetic operations whose operands are constants."""

        candidates = []

        for index, instruction in enumerate(instructions):
            if instruction.operator not in {"+", "-", "*", "/"}:
                continue

            if not self._is_integer(instruction.arg1):
                continue

            if not self._is_integer(instruction.arg2):
                continue

            left = int(instruction.arg1)
            right = int(instruction.arg2)

            if instruction.operator == "+":
                value = left + right

            elif instruction.operator == "-":
                value = left - right

            elif instruction.operator == "*":
                value = left * right

            else:
                if right == 0:
                    continue

                value = int(left / right)

            candidate = deepcopy(instructions)

            candidate[index] = TACInstruction(
                result=instruction.result,
                arg1=str(value),
                operator=None,
                arg2=None,
            )

            candidates.append(candidate)

        return candidates

    # ------------------------------------------------------------------
    # M4: Strength Reduction
    # ------------------------------------------------------------------

    def apply_m4_strength_reduction(
        self,
        instructions: list[TACInstruction],
    ) -> list[list[TACInstruction]]:
        """
        Replace multiplication by 2 with addition.

        x * 2 -> x + x
        2 * x -> x + x
        """

        candidates = []

        for index, instruction in enumerate(instructions):
            if instruction.operator != "*":
                continue

            if instruction.arg2 == "2":
                operand = instruction.arg1

            elif instruction.arg1 == "2":
                operand = instruction.arg2

            else:
                continue

            candidate = deepcopy(instructions)

            candidate[index] = TACInstruction(
                result=instruction.result,
                arg1=operand,
                operator="+",
                arg2=operand,
            )

            candidates.append(candidate)

        return candidates

    # ------------------------------------------------------------------
    # M5: Dead Assignment Removal
    # ------------------------------------------------------------------

    def apply_m5_dead_assignment(
        self,
        instructions: list[TACInstruction],
    ) -> list[list[TACInstruction]]:
        """
        Remove assignments whose result is never subsequently used.

        Example:
            t1 = x + 5
            a = t1
            b = y * 2
            return b

        removes both:
            t1 = x + 5
            a = t1
        """

        candidates = []

        # Count uses of every TAC variable.
        use_counts = self._count_uses(instructions)

        for index, instruction in enumerate(instructions):
            if instruction.result is None:
                continue

            if instruction.operator == "return":
                continue

            result = instruction.result

            # If the result is never used, the instruction is dead.
            if use_counts.get(result, 0) != 0:
                continue

            candidate = deepcopy(instructions)

            # If this instruction computes a temporary which is
            # immediately copied into a dead variable, remove both.
            remove_indices = {index}

            if (
                instruction.result.startswith("t")
                and index + 1 < len(instructions)
            ):
                next_instruction = instructions[index + 1]

                if (
                    next_instruction.operator is None
                    and next_instruction.arg1 == instruction.result
                    and next_instruction.result is not None
                    and use_counts.get(next_instruction.result, 0) == 0
                ):
                    remove_indices.add(index + 1)

            candidate = [
                instruction
                for position, instruction in enumerate(candidate)
                if position not in remove_indices
            ]

            candidates.append(candidate)

        return self._remove_duplicate_candidates(candidates)

    # ------------------------------------------------------------------
    # M6: Common Subexpression Elimination
    # ------------------------------------------------------------------

    def apply_m6_cse(
        self,
        instructions: list[TACInstruction],
    ) -> list[list[TACInstruction]]:
        """
        Reuse an earlier identical expression when its operands
        have not changed.

        Example:
            t1 = x + y
            a = t1
            t2 = x + y

        becomes:

            t1 = x + y
            a = t1
            t2 = t1
        """

        candidates = []

        expressions: dict[tuple[str, str, str], tuple[str, int]] = {}

        for index, instruction in enumerate(instructions):
            if instruction.operator not in {"+", "-", "*", "/"}:
                continue

            key = (
                instruction.arg1,
                instruction.operator,
                instruction.arg2,
            )

            # If this exact expression already exists and no operand
            # has been modified since, we can reuse its result.
            if key in expressions:
                previous_result, previous_index = expressions[key]

                if self._operands_unchanged(
                    instructions,
                    previous_index,
                    index,
                    key[0],
                    key[2],
                ):
                    candidate = deepcopy(instructions)

                    candidate[index] = TACInstruction(
                        result=instruction.result,
                        arg1=previous_result,
                        operator=None,
                        arg2=None,
                    )

                    candidates.append(candidate)

            # Record the latest occurrence.
            expressions[key] = (instruction.result, index)

            # Any assignment to an operand invalidates expressions
            # that depend on that operand.
            if instruction.result is not None:
                expressions = {
                    expression: data
                    for expression, data in expressions.items()
                    if instruction.result
                    not in {
                        expression[0],
                        expression[2],
                    }
                }

                # Re-add current expression if it survived.
                expressions[key] = (instruction.result, index)

        return self._remove_duplicate_candidates(candidates)

    # ------------------------------------------------------------------
    # M7: Constant Propagation
    # ------------------------------------------------------------------

    def apply_m7_constant_propagation(
        self,
        instructions: list[TACInstruction],
    ) -> list[list[TACInstruction]]:
        """
        Propagate known constant assignments.

        Example:
            a = 5
            t1 = a + x

        becomes:

            a = 5
            t1 = 5 + x
        """

        candidates = []

        constants: dict[str, str] = {}

        for index, instruction in enumerate(instructions):
            if instruction.operator is None:
                # Copy assignment.
                if (
                    instruction.result is not None
                    and self._is_integer(instruction.arg1)
                ):
                    constants[instruction.result] = instruction.arg1

                elif instruction.result is not None:
                    constants.pop(instruction.result, None)

                continue

            if instruction.operator == "return":
                continue

            new_arg1 = constants.get(
                instruction.arg1,
                instruction.arg1,
            )

            new_arg2 = constants.get(
                instruction.arg2,
                instruction.arg2,
            )

            if (
                new_arg1 == instruction.arg1
                and new_arg2 == instruction.arg2
            ):
                if instruction.result is not None:
                    constants.pop(instruction.result, None)

                continue

            candidate = deepcopy(instructions)

            candidate[index] = TACInstruction(
                result=instruction.result,
                arg1=new_arg1,
                operator=instruction.operator,
                arg2=new_arg2,
            )

            candidates.append(candidate)

            if instruction.result is not None:
                constants.pop(instruction.result, None)

        return self._remove_duplicate_candidates(candidates)

    # ------------------------------------------------------------------
    # M8: Independent Instruction Reordering
    # ------------------------------------------------------------------

    def apply_m8_instruction_reordering(
        self,
        instructions: list[TACInstruction],
    ) -> list[list[TACInstruction]]:
        """
        Swap adjacent independent instructions.

        Two instructions are considered independent if neither reads
        or writes the result of the other.
        """

        candidates = []

        for index in range(len(instructions) - 1):
            first = instructions[index]
            second = instructions[index + 1]

            if first.operator == "return":
                continue

            if second.operator == "return":
                continue

            if first.result is None or second.result is None:
                continue

            first_reads = self._operands(first)
            second_reads = self._operands(second)

            # Dependency checks:
            # first writes something second reads
            if first.result in second_reads:
                continue

            # second writes something first reads
            if second.result in first_reads:
                continue

            # Both write the same variable.
            if first.result == second.result:
                continue

            candidate = deepcopy(instructions)

            candidate[index], candidate[index + 1] = (
                candidate[index + 1],
                candidate[index],
            )

            candidates.append(candidate)

        return candidates

    # ------------------------------------------------------------------
    # Helper functions
    # ------------------------------------------------------------------

    @staticmethod
    def _is_integer(value: str | None) -> bool:
        if value is None:
            return False

        return value.lstrip("-").isdigit()

    @staticmethod
    def _operands(
        instruction: TACInstruction,
    ) -> set[str]:
        operands = set()

        for value in (instruction.arg1, instruction.arg2):
            if value is not None and not value.lstrip("-").isdigit():
                operands.add(value)

        return operands

    @staticmethod
    def _count_uses(
        instructions: list[TACInstruction],
    ) -> dict[str, int]:
        counts: dict[str, int] = {}

        for instruction in instructions:
            for operand in (
                instruction.arg1,
                instruction.arg2,
            ):
                if operand is None:
                    continue

                if operand.lstrip("-").isdigit():
                    continue

                counts[operand] = counts.get(operand, 0) + 1

        return counts

    @staticmethod
    def _operands_unchanged(
        instructions: list[TACInstruction],
        start: int,
        end: int,
        operand1: str,
        operand2: str,
    ) -> bool:
        for index in range(start + 1, end):
            instruction = instructions[index]

            if instruction.result in {operand1, operand2}:
                return False

        return True

    @staticmethod
    def _remove_duplicate_candidates(
        candidates: list[list[TACInstruction]],
    ) -> list[list[TACInstruction]]:
        unique = []
        seen = set()

        for candidate in candidates:
            key = tuple(str(instruction) for instruction in candidate)

            if key not in seen:
                seen.add(key)
                unique.append(candidate)

        return unique

    # ------------------------------------------------------------------
    # Apply all mutation operators
    # ------------------------------------------------------------------

    def apply_all(
        self,
        instructions: list[TACInstruction],
    ) -> dict[str, list[list[TACInstruction]]]:
        """Generate candidates for all eight mutation operators."""

        return {
            "M1": self.apply_m1_zero_add(instructions),
            "M2": self.apply_m2_one_mul(instructions),
            "M3": self.apply_m3_constant_folding(instructions),
            "M4": self.apply_m4_strength_reduction(instructions),
            "M5": self.apply_m5_dead_assignment(instructions),
            "M6": self.apply_m6_cse(instructions),
            "M7": self.apply_m7_constant_propagation(instructions),
            "M8": self.apply_m8_instruction_reordering(instructions),
        }