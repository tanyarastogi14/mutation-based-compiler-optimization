import json
from pathlib import Path

from dataset.benchmark_builder import build_benchmark
from dataset.dataset_utils import source_fingerprint
from dataset.validate_benchmark import validate_benchmark


CATEGORIES = [
    "zero_add",
    "one_mul",
    "constant_expr",
    "strength_reduce",
    "dead_assignment",
    "common_subexpression",
    "constant_propagation",
    "independent_ops",
    "mixed",
]

PROGRAMS_PER_CATEGORY = 40

OUTPUT_DIR = Path("dataset/generated")
OUTPUT_FILE = OUTPUT_DIR / "prototype_dataset.json"


def generate_dataset() -> list[dict]:
    """Generate and validate the prototype benchmark dataset."""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    dataset = []
    fingerprints = set()

    program_number = 1

    for category in CATEGORIES:
        generated_for_category = 0
        seed = 1000

        while generated_for_category < PROGRAMS_PER_CATEGORY:
            benchmark_id = (
                f"P{program_number:03d}_{category}"
            )

            size_cycle = ["small", "medium", "large"]

            difficulty = size_cycle[
               generated_for_category % len(size_cycle)
            ]


            benchmark = build_benchmark(
                program_id=benchmark_id,
                category=category,
                seed=seed,
                difficulty=difficulty,
            )




            # Validate benchmark structure and semantics.
            errors = validate_benchmark(benchmark)

            if errors:
                print(
                    f"REJECTED {benchmark_id}:"
                )

                for error in errors:
                    print(f"  - {error}")

                seed += 1
                continue

            # Reject duplicate source programs.
            fingerprint = source_fingerprint(
                benchmark.source_code
            )

            if fingerprint in fingerprints:
                print(
                    f"REJECTED DUPLICATE: {benchmark_id}"
                )

                seed += 1
                continue

            fingerprints.add(fingerprint)

            dataset.append(benchmark.to_dict())

            print(
                f"ACCEPTED {benchmark_id} "
                f"({category})"
            )

            generated_for_category += 1
            program_number += 1
            seed += 1

    return dataset


def save_dataset(dataset: list[dict]) -> None:
    """Save dataset as formatted JSON."""

    with OUTPUT_FILE.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            dataset,
            file,
            indent=2,
        )


if __name__ == "__main__":
    dataset = generate_dataset()

    save_dataset(dataset)

    print()
    print("=" * 50)
    print("DATASET GENERATION COMPLETE")
    print("=" * 50)
    print(f"Programs generated: {len(dataset)}")
    print(f"Output file: {OUTPUT_FILE}")