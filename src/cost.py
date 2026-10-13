class CostModel:

    WEIGHTS = {
        "instructions": 0.4,
        "arithmetic": 0.3,
        "temporaries": 0.2,
        "execution_time": 0.1,
    }

    OPERATION_COST = {
        "+": 1.0,
        "-": 1.0,
        "*": 2.0,
        "/": 3.0,
    }

    def calculate_components(self, instructions):

        instruction_count = float(len(instructions))

        arithmetic_cost = sum(
            self.OPERATION_COST.get(
                instruction.operator,
                0.0,
            )
            for instruction in instructions
        )

        temporary_count = float(
            len({
                instruction.result
                for instruction in instructions
                if instruction.result
                and instruction.result.startswith("t")
            })
        )

        return {
            "instructions": instruction_count,
            "arithmetic": float(arithmetic_cost),
            "temporaries": temporary_count,
            "execution_time": 0.0,
        }

    def calculate(
        self,
        instructions,
        reference_components,
    ):

        components = self.calculate_components(
            instructions
        )

        normalized = {}

        for name, value in components.items():

            reference = reference_components[name]

            if reference <= 0:
                normalized[name] = 0.0
            else:
                normalized[name] = (
                    value / reference
                )

        return sum(
            self.WEIGHTS[name]
            * normalized[name]
            for name in self.WEIGHTS
        )