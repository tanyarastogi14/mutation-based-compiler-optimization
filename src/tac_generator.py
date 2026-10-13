import ast

from src.tac import TACInstruction


class TACGenerator:
    """Generate TAC from expressions and assignments."""

    def __init__(self):
        self.instructions: list[TACInstruction] = []
        self.temp_counter = 0

    def new_temp(self) -> str:
        self.temp_counter += 1
        return f"t{self.temp_counter}"

    def generate_expression(self, expression: str) -> str:
        """Convert an arithmetic expression into TAC."""

        tree = ast.parse(expression, mode="eval")

        return self._generate_node(tree.body)

    def _generate_node(self, node: ast.AST) -> str:
        if isinstance(node, ast.Name):
            return node.id

        if isinstance(node, ast.Constant):
            if isinstance(node.value, int):
                return str(node.value)

            raise ValueError("Only integer constants are supported.")

        if isinstance(node, ast.BinOp):
            left = self._generate_node(node.left)
            right = self._generate_node(node.right)

            if isinstance(node.op, ast.Add):
                operator = "+"

            elif isinstance(node.op, ast.Sub):
                operator = "-"

            elif isinstance(node.op, ast.Mult):
                operator = "*"

            elif isinstance(node.op, ast.Div):
                operator = "/"

            else:
                raise ValueError(
                    f"Unsupported operator: {type(node.op).__name__}"
                )

            temp = self.new_temp()

            self.instructions.append(
                TACInstruction(
                    result=temp,
                    arg1=left,
                    operator=operator,
                    arg2=right,
                )
            )

            return temp

        raise ValueError(
            f"Unsupported expression node: {type(node).__name__}"
        )

    def generate_assignment(
        self,
        variable: str,
        expression: str,
    ) -> None:
        """Generate TAC for one assignment."""

        value = self.generate_expression(expression)

        self.instructions.append(
            TACInstruction(
                result=variable,
                arg1=value,
                operator=None,
                arg2=None,
            )
        )

    def generate_return(self, variable: str) -> None:
        """Generate TAC for a return statement."""

        self.instructions.append(
            TACInstruction(
                result=None,
                arg1=variable,
                operator="return",
                arg2=None,
            )
        )