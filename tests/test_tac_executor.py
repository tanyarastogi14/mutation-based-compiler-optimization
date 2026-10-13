from src.c_to_tac import CToTACCompiler
from src.tac_executor import execute_tac


def test_tac_execution():
    source = """int compute(int x) {
    int a;
    int b;

    a = x + 5;
    b = a * 2;

    return b;
}"""

    instructions = CToTACCompiler().compile(source)

    assert execute_tac(instructions, {"x": 5}) == 20
    assert execute_tac(instructions, {"x": -3}) == 4