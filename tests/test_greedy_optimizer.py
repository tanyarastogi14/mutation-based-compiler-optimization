from src.c_to_tac import CToTACCompiler
from src.greedy_optimizer import GreedyOptimizer


def test_greedy_optimizer_reduces_cost():

    source = """int compute(int x) {
    int a;
    int b;

    a = x + 0;
    b = a * 1;

    return b;
}"""

    compiler = CToTACCompiler()
    tac = compiler.compile(source)

    inputs = [
        {"x": 5},
        {"x": -3},
        {"x": 10},
    ]

    expected = [5, -3, 10]

    result = GreedyOptimizer().optimize(
        tac,
        inputs,
        expected,
    )

    assert result["final_cost"] < result["original_cost"]
    assert result["iterations"] >= 1