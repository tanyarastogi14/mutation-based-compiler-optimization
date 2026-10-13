import json
from pathlib import Path

from src.beam_optimizer import BeamOptimizer
from src.greedy_optimizer import GreedyOptimizer
from src.tac import TACInstruction
from src.tac_executor import execute_tac


DATASET_FILE = Path(
    "dataset/generated/prototype_dataset_with_tac.json"
)


def parse_tac(tac_lines):
    instructions = []

    for line in tac_lines:
        line = line.strip()

        if line.startswith("return "):
            instructions.append(
                TACInstruction(
                    result=None,
                    arg1=line.split(" ", 1)[1],
                    operator="return",
                    arg2=None,
                )
            )
            continue

        result, expression = line.split(" = ", 1)
        parts = expression.split()

        if len(parts) == 1:
            instructions.append(
                TACInstruction(
                    result=result,
                    arg1=parts[0],
                    operator=None,
                    arg2=None,
                )
            )
        else:
            instructions.append(
                TACInstruction(
                    result=result,
                    arg1=parts[0],
                    operator=parts[1],
                    arg2=parts[2],
                )
            )

    return instructions


def validate_outputs(
    tac,
    test_inputs,
    expected_outputs,
):
    actual_outputs = []

    for test_input in test_inputs:
        actual_outputs.append(
            execute_tac(
                tac,
                test_input,
            )
        )

    return actual_outputs == expected_outputs


def print_tac(title, tac):
    print()
    print(title)
    print("-" * len(title))

    for index, instruction in enumerate(tac, start=1):
        print(f"{index:02d}. {instruction}")


def main():

    with DATASET_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:
        dataset = json.load(file)

    # Pick the last mixed benchmark so we get
    # a larger example from the final dataset.
    benchmark = next(
        item
        for item in reversed(dataset)
        if item["category"] == "mixed"
    )

    tac = parse_tac(benchmark["tac"])

    print("=" * 70)
    print("WORKED OPTIMIZATION EXAMPLE")
    print("=" * 70)

    print(f"Program: {benchmark['id']}")
    print(f"Category: {benchmark['category']}")
    print(f"Difficulty: {benchmark['difficulty']}")

    print()
    print("ORIGINAL C PROGRAM")
    print("------------------")
    print(benchmark["source_code"])

    print_tac(
        "ORIGINAL TAC",
        tac,
    )

    greedy = GreedyOptimizer().optimize(
        original_tac=tac,
        test_inputs=benchmark["test_inputs"],
        expected_outputs=benchmark["expected_outputs"],
    )

    beam = BeamOptimizer(
        beam_width=3
    ).optimize(
        original_tac=tac,
        test_inputs=benchmark["test_inputs"],
        expected_outputs=benchmark["expected_outputs"],
    )

    print()
    print("=" * 70)
    print("GREEDY SEARCH")
    print("=" * 70)

    print(
        f"Original cost: {greedy['original_cost']:.4f}"
    )

    print(
        f"Final cost:    {greedy['final_cost']:.4f}"
    )

    print(
        f"Reduction:     "
        f"{(
            (greedy['original_cost']
             - greedy['final_cost'])
            / greedy['original_cost']
            * 100
        ):.2f}%"
    )

    print(
        f"Mutation path: "
        f"{' -> '.join(
            x['operator']
            for x in greedy['history']
            if x['operator']
        ) or 'No mutation'}"
    )

    print_tac(
        "GREEDY OPTIMIZED TAC",
        greedy["optimized_tac"],
    )

    print()
    print("=" * 70)
    print("BEAM SEARCH")
    print("=" * 70)

    print(
        f"Original cost: {beam['original_cost']:.4f}"
    )

    print(
        f"Final cost:    {beam['final_cost']:.4f}"
    )

    print(
        f"Reduction:     "
        f"{(
            (beam['original_cost']
             - beam['final_cost'])
            / beam['original_cost']
            * 100
        ):.2f}%"
    )

    print(
        f"Beam width:    {beam['beam_width']}"
    )

    print(
        f"Candidates explored: "
        f"{beam['explored_candidates']}"
    )

    print(
        f"Mutation path: "
        f"{' -> '.join(beam['history']) or 'No mutation'}"
    )

    print_tac(
        "BEAM OPTIMIZED TAC",
        beam["optimized_tac"],
    )

    print()
    print("=" * 70)
    print("CORRECTNESS VALIDATION")
    print("=" * 70)

    greedy_correct = validate_outputs(
        greedy["optimized_tac"],
        benchmark["test_inputs"],
        benchmark["expected_outputs"],
    )

    beam_correct = validate_outputs(
        beam["optimized_tac"],
        benchmark["test_inputs"],
        benchmark["expected_outputs"],
    )

    print(
        f"Greedy output preservation: "
        f"{'PASS' if greedy_correct else 'FAIL'}"
    )

    print(
        f"Beam output preservation:   "
        f"{'PASS' if beam_correct else 'FAIL'}"
    )

    print()
    print("Expected outputs:")
    print(benchmark["expected_outputs"])

    print()
    print("Greedy optimized outputs:")
    print([
        execute_tac(
            greedy["optimized_tac"],
            test_input,
        )
        for test_input in benchmark["test_inputs"]
    ])

    print()
    print("Beam optimized outputs:")
    print([
        execute_tac(
            beam["optimized_tac"],
            test_input,
        )
        for test_input in benchmark["test_inputs"]
    ])


if __name__ == "__main__":
    main()