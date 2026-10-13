from src.c_to_tac import CToTACCompiler
from src.mutations import MutationEngine
from src.tac import TACInstruction


class OptimizerPipeline:
    """Compile C programs and generate mutation candidates."""

    def __init__(self):
        self.compiler = CToTACCompiler()
        self.mutation_engine = MutationEngine()

    def compile(
        self,
        source_code: str,
    ) -> list[TACInstruction]:
        """Compile C source into TAC."""

        return self.compiler.compile(source_code)

    def generate_candidates(
        self,
        source_code: str,
    ) -> dict[str, list[list[TACInstruction]]]:
        """Generate candidates for all mutation operators."""

        instructions = self.compile(source_code)

        return self.mutation_engine.apply_all(instructions)