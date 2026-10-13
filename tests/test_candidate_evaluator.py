from src.c_to_tac import CToTACCompiler
from src.candidate_evaluator import CandidateEvaluator
from src.optimizer_pipeline import OptimizerPipeline


def test_candidate_evaluation():
    source = """int compute(int x) {
    int a;

    a = x + 0;

    return a;
}"""

    compiler = CToTACCompiler()
    original_tac = compiler.compile(source)

    candidates = OptimizerPipeline().generate_candidates(source)

    test_inputs = [
        {"x": 5},
        {"x": -3},
        {"x": 0},
    ]

    expected_outputs = [5, -3, 0]

    evaluated = CandidateEvaluator().evaluate(
        candidates=candidates,
        test_inputs=test_inputs,
        expected_outputs=expected_outputs,
        original_tac=original_tac,
    )

    m1_candidates = [
        candidate
        for candidate in evaluated
        if candidate["operator"] == "M1"
    ]

    assert len(m1_candidates) == 1
    assert m1_candidates[0]["valid"] is True