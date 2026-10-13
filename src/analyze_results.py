import json
from pathlib import Path
from collections import defaultdict


RESULTS_FILE = Path(
    "dataset/generated/experiment_results.json"
)


def average(values):
    return sum(values) / len(values) if values else 0.0


def analyze():
    with RESULTS_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:
        results = json.load(file)

    greedy_reductions = [
        r["greedy_reduction_percent"]
        for r in results
    ]

    beam_reductions = [
        r["beam_reduction_percent"]
        for r in results
    ]

    beam_better = 0
    greedy_better = 0
    ties = 0

    for result in results:
        greedy = result["greedy_final_cost"]
        beam = result["beam_final_cost"]

        if beam < greedy:
            beam_better += 1
        elif greedy < beam:
            greedy_better += 1
        else:
            ties += 1

    print("=" * 60)
    print("OVERALL RESULTS")
    print("=" * 60)

    print(
        f"Programs: {len(results)}"
    )

    print(
        f"Average Greedy reduction: "
        f"{average(greedy_reductions):.2f}%"
    )

    print(
        f"Average Beam reduction: "
        f"{average(beam_reductions):.2f}%"
    )

    print(
        f"Beam better: {beam_better}"
    )

    print(
        f"Greedy better: {greedy_better}"
    )

    print(
        f"Ties: {ties}"
    )

    print()
    print("=" * 60)
    print("BY CATEGORY")
    print("=" * 60)

    categories = defaultdict(list)

    for result in results:
        categories[
            result["category"]
        ].append(result)

    for category, items in categories.items():

        greedy = average([
            x["greedy_reduction_percent"]
            for x in items
        ])

        beam = average([
            x["beam_reduction_percent"]
            for x in items
        ])

        beam_wins = sum(
            x["beam_final_cost"]
            < x["greedy_final_cost"]
            for x in items
        )

        print(
            f"{category:25s} | "
            f"Greedy: {greedy:6.2f}% | "
            f"Beam: {beam:6.2f}% | "
            f"Beam wins: {beam_wins}/{len(items)}"
        )

    print()
    print("=" * 60)
    print("BY DIFFICULTY")
    print("=" * 60)

    difficulties = defaultdict(list)

    for result in results:
        difficulties[
            result["difficulty"]
        ].append(result)

    for difficulty, items in difficulties.items():

        greedy = average([
            x["greedy_reduction_percent"]
            for x in items
        ])

        beam = average([
            x["beam_reduction_percent"]
            for x in items
        ])

        explored = average([
            x["beam_explored_candidates"]
            for x in items
        ])

        print(
            f"{difficulty:10s} | "
            f"Greedy: {greedy:6.2f}% | "
            f"Beam: {beam:6.2f}% | "
            f"Avg Beam explored: {explored:.1f}"
        )

    print()
    print("=" * 60)
    print("SEARCH EFFORT")
    print("=" * 60)

    print(
        f"Average Beam candidates explored: "
        f"{average([r['beam_explored_candidates'] for r in results]):.2f}"
    )

    print(
        f"Average Greedy iterations: "
        f"{average([r['greedy_iterations'] for r in results]):.2f}"
    )

    print(
        f"Average Beam iterations: "
        f"{average([r['beam_iterations'] for r in results]):.2f}"
    )


if __name__ == "__main__":
    analyze()