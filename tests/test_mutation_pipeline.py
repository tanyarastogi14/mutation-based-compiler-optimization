from src.optimizer_pipeline import OptimizerPipeline


def test_all_mutations_generate_candidates():
    source = """int compute(int x, int y) {
    int dead;
    int constant;
    int a;
    int b;
    int c;
    int d;
    int e;
    int f;

    dead = x + 5;
    constant = 7;

    a = x + 0;
    b = y * 1;
    c = x + (4 + 3);
    d = y * 2;
    e = x + y;
    f = x + y;

    return c;
}"""

    candidates = OptimizerPipeline().generate_candidates(source)

    assert len(candidates["M1"]) >= 1
    assert len(candidates["M2"]) >= 1
    assert len(candidates["M3"]) >= 1
    assert len(candidates["M4"]) >= 1
    assert len(candidates["M5"]) >= 1
    assert len(candidates["M6"]) >= 1
    assert len(candidates["M8"]) >= 1