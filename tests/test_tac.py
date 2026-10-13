from src.c_to_tac import CToTACCompiler


def test_c_to_tac():
    source = """int compute(int x) {
    int a;
    int b;

    a = x + 5;
    b = a * 2;

    return b;
}"""

    instructions = CToTACCompiler().compile(source)

    assert [str(instruction) for instruction in instructions] == [
        "t1 = x + 5",
        "a = t1",
        "t2 = a * 2",
        "b = t2",
        "return b",
    ]