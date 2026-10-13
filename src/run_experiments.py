import json
from pathlib import Path

from src.beam_optimizer import BeamOptimizer
from src.greedy_optimizer import GreedyOptimizer
from src.tac import TACInstruction


INPUT_FILE = Path(
    "dataset/generated/prototype_dataset_with_tac.json"
)

OUTPUT_FILE = Path(
    "dataset/generated/experiment_results.json"
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


def percentage_reduction(original, final):
    if original == 0:
        return 0.0

    return (
        (original - final)
        / original
        * 100
    )


def run_experiments():
    with INPUT_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:
        dataset = json.load(file)

    results = []

    for index, benchmark in enumerate(dataset, start=1):

        tac = parse_tac(benchmark["tac"])

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

        original_cost = greedy["original_cost"]

        result = {
            "id": benchmark["id"],
            "category": benchmark["category"],
            "difficulty": benchmark["difficulty"],

            "original_cost": original_cost,

            "greedy_final_cost": greedy["final_cost"],
            "greedy_reduction_percent": percentage_reduction(
                original_cost,
                greedy["final_cost"],
            ),
            "greedy_iterations": greedy["iterations"],
            "greedy_history": greedy["history"],

            "beam_final_cost": beam["final_cost"],
            "beam_reduction_percent": percentage_reduction(
                original_cost,
                beam["final_cost"],
            ),
            "beam_iterations": beam["iterations"],
            "beam_history": beam["history"],
            "beam_explored_candidates": beam[
                "explored_candidates"
            ],
            "beam_width": beam["beam_width"],
        }

        results.append(result)

        print(
            f"[{index}/{len(dataset)}] "
            f"{benchmark['id']} | "
            f"Greedy: "
            f"{greedy['final_cost']:.4f} | "
            f"Beam: "
            f"{beam['final_cost']:.4f}"
        )

    with OUTPUT_FILE.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            results,
            file,
            indent=2,
        )

    print()
    print("=" * 60)
    print("EXPERIMENTS COMPLETE")
    print("=" * 60)
    print(f"Programs evaluated: {len(results)}")
    print(f"Results saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    run_experiments()