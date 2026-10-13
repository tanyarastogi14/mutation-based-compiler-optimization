import random

from dataset.generator_utils import (
    choose_parameters,
    choose_variable_names,
    format_program,
)


class CProgramGenerator:
    def __init__(self, seed: int = 42):
        self.random = random.Random(seed)
        self.seed = seed

    def _base_program(self, size: str = "small"):
        if size == "small":
            extra = 0
        elif size == "medium":
            extra = 3
        elif size == "large":
            extra = 7
        else:
            raise ValueError(f"Unknown size: {size}")

        parameters = choose_parameters(
            self.random,
            2,
        )

        variable_count = 5 + extra

        variables = choose_variable_names(
            self.random,
            variable_count,
        )

        x, y = parameters

        a, b, c, d, result = variables[:5]

        statements = [
            f"{a} = {x} + 0;",
            f"{b} = {y} * 1;",
            f"{c} = {a} + ({self.random.randint(2, 9)} + "
            f"{self.random.randint(2, 9)});",
            f"{d} = {b} * 2;",
        ]

        current = d

        for index in range(extra):
            variable = variables[5 + index]

            if index % 3 == 0:
                statements.append(
                    f"{variable} = {current} + {x};"
                )
            elif index % 3 == 1:
                statements.append(
                    f"{variable} = {current} * 2;"
                )
            else:
                statements.append(
                    f"{variable} = {current} + "
                    f"({self.random.randint(2, 9)} + "
                    f"{self.random.randint(2, 9)});"
                )

            current = variable

        statements.append(
            f"{result} = {c} + {current};"
        )

        return format_program(
            parameters=parameters,
            declarations=variables,
            statements=statements,
            return_variable=result,
        )

    def generate_zero_add_program(self, size="small"):
        parameters = choose_parameters(self.random, 2)
        variables = choose_variable_names(
            self.random,
            5 if size == "small" else 8 if size == "medium" else 12,
        )

        x, y = parameters
        a = variables[0]
        b = variables[1]
        result = variables[2]

        statements = [
            f"{a} = {x} + 0;",
            f"{b} = {a} + {y};",
        ]

        if size != "small":
            for variable in variables[3:-1]:
                statements.append(
                    f"{variable} = {b} + {x};"
                )
                b = variable

        statements.append(
            f"{result} = {b} + 1;"
        )

        return format_program(
            parameters,
            variables,
            statements,
            result,
        )

    def generate_one_mul_program(self, size="small"):
        parameters = choose_parameters(self.random, 2)
        variables = choose_variable_names(
            self.random,
            5 if size == "small" else 8 if size == "medium" else 12,
        )

        x, y = parameters
        a = variables[0]
        b = variables[1]
        result = variables[2]

        statements = [
            f"{a} = {x} * 1;",
            f"{b} = {a} + {y};",
        ]

        if size != "small":
            for variable in variables[3:-1]:
                statements.append(
                    f"{variable} = {b} + {y};"
                )
                b = variable

        statements.append(
            f"{result} = {b} * 1;"
        )

        return format_program(
            parameters,
            variables,
            statements,
            result,
        )

    def generate_constant_expr_program(self, size="small"):
        parameters = choose_parameters(self.random, 2)
        variables = choose_variable_names(
            self.random,
            5 if size == "small" else 8 if size == "medium" else 12,
        )

        x, y = parameters
        a = variables[0]
        b = variables[1]
        result = variables[2]

        left = self.random.randint(2, 9)
        right = self.random.randint(2, 9)

        statements = [
            f"{a} = {x} + ({left} + {right});",
            f"{b} = {a} + {y};",
        ]

        if size != "small":
            for variable in variables[3:-1]:
                left = self.random.randint(2, 9)
                right = self.random.randint(2, 9)

                statements.append(
                    f"{variable} = {b} + "
                    f"({left} + {right});"
                )
                b = variable

        statements.append(
            f"{result} = {b} + 1;"
        )

        return format_program(
            parameters,
            variables,
            statements,
            result,
        )

    def generate_strength_reduce_program(self, size="small"):
        parameters = choose_parameters(self.random, 2)
        variables = choose_variable_names(
            self.random,
            5 if size == "small" else 8 if size == "medium" else 12,
        )

        x, y = parameters
        a = variables[0]
        b = variables[1]
        result = variables[2]

        statements = [
            f"{a} = {x} * 2;",
            f"{b} = {a} + {y};",
        ]

        if size != "small":
            for variable in variables[3:-1]:
                statements.append(
                    f"{variable} = {b} * 2;"
                )
                b = variable

        statements.append(
            f"{result} = {b} + 1;"
        )

        return format_program(
            parameters,
            variables,
            statements,
            result,
        )

    def generate_dead_assignment_program(self, size="small"):
        parameters = choose_parameters(self.random, 2)
        variables = choose_variable_names(
            self.random,
            6 if size == "small" else 9 if size == "medium" else 13,
        )

        x, y = parameters
        result = variables[-1]

        statements = []

        for variable in variables[:-1]:
            if len(statements) % 2 == 0:
                statements.append(
                    f"{variable} = {x} + 5;"
                )
            else:
                statements.append(
                    f"{variable} = {y} * 2;"
                )

        statements.append(
            f"{result} = {x} + {y};"
        )

        return format_program(
            parameters,
            variables,
            statements,
            result,
        )

    def generate_cse_program(self, size="small"):
        parameters = choose_parameters(self.random, 2)
        variables = choose_variable_names(
            self.random,
            6 if size == "small" else 9 if size == "medium" else 13,
        )

        x, y = parameters
        a = variables[0]
        b = variables[1]
        result = variables[2]

        statements = [
            f"{a} = {x} + {y};",
            f"{b} = {x} + {y};",
        ]

        current = b

        if size != "small":
            for variable in variables[3:-1]:
                statements.append(
                    f"{variable} = {current} + {x};"
                )
                current = variable

        statements.append(
            f"{result} = {a} + {current};"
        )

        return format_program(
            parameters,
            variables,
            statements,
            result,
        )

    def generate_constant_propagation_program(self, size="small"):
        parameters = choose_parameters(self.random, 2)
        variables = choose_variable_names(
            self.random,
            6 if size == "small" else 9 if size == "medium" else 13,
        )

        x, y = parameters
        constant_variable = variables[0]
        current = variables[1]
        result = variables[-1]

        constant_value = self.random.randint(2, 20)

        statements = [
            f"{constant_variable} = {constant_value};",
            f"{current} = {constant_variable} + {x};",
        ]

        if size != "small":
            for variable in variables[2:-1]:
                statements.append(
                    f"{variable} = {current} + {y};"
                )
                current = variable

        statements.append(
            f"{result} = {current} + {constant_variable};"
        )

        return format_program(
            parameters,
            variables,
            statements,
            result,
        )

    def generate_independent_ops_program(self, size="small"):
        parameters = choose_parameters(self.random, 2)
        variables = choose_variable_names(
            self.random,
            6 if size == "small" else 9 if size == "medium" else 13,
        )

        x, y = parameters

        a = variables[0]
        b = variables[1]
        c = variables[2]
        result = variables[-1]

        statements = [
            f"{a} = {x} + 5;",
            f"{b} = {y} * 2;",
            f"{c} = {x} + 3;",
        ]

        if size != "small":
            for variable in variables[3:-1]:
                statements.append(
                    f"{variable} = {x} + {y};"
                )

        statements.append(
            f"{result} = {a} + {b};"
        )

        return format_program(
            parameters,
            variables,
            statements,
            result,
        )

    def generate_mixed_program(self, size="small"):
        return self._base_program(size)

    def generate_program(
        self,
        category: str,
        size: str = "small",
    ) -> str:

        generators = {
            "zero_add": self.generate_zero_add_program,
            "one_mul": self.generate_one_mul_program,
            "constant_expr": self.generate_constant_expr_program,
            "strength_reduce": self.generate_strength_reduce_program,
            "dead_assignment": self.generate_dead_assignment_program,
            "common_subexpression": self.generate_cse_program,
            "constant_propagation": self.generate_constant_propagation_program,
            "independent_ops": self.generate_independent_ops_program,
            "mixed": self.generate_mixed_program,
        }

        if category not in generators:
            raise ValueError(
                f"Unknown category: {category}"
            )

        return generators[category](size)