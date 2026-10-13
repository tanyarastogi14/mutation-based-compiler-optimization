from dataset.schema import BenchmarkProgram, OptimizationOpportunity


def test_benchmark_program_schema():
    benchmark = BenchmarkProgram(
        id="TEST_001",
        dataset_version="1.0",
        generator_version="1.0",
        seed=42,
        category="zero_add",
        difficulty="small",
        source_code="""int compute(int x) {
    int a;
    a = x + 0;
    return a;
}""",
        parameters=["x"],
        variables=["a"],
        test_inputs=[
            {"x": 5},
            {"x": -3},
        ],
        expected_outputs=[5, -3],
        optimization_opportunities=[
            OptimizationOpportunity(
                operator="M1",
                reason="a = x + 0",
            )
        ],
    )

    data = benchmark.to_dict()

    assert data["id"] == "TEST_001"
    assert data["category"] == "zero_add"
    assert data["expected_outputs"] == [5, -3]
    assert data["optimization_opportunities"][0]["operator"] == "M1"

    # These must remain empty until later stages.
    assert data["tac"] is None
    assert data["baseline_cost"] is None
    assert data["reference_program"] is None
    assert data["reference_cost"] is None