from src.c_to_tac import CToTACCompiler
from src.beam_optimizer import BeamOptimizer


def test_beam_optimizer_reduces_cost():

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

    result = BeamOptimizer(
        beam_width=3
    ).optimize(
        tac,
        inputs,
        expected,
    )

    assert result["final_cost"] < result["original_cost"]
    assert result["explored_candidates"] > 0