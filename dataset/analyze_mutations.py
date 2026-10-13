import json
from pathlib import Path

from src.mutations import MutationEngine
from src.tac import TACInstruction


INPUT_FILE = Path(
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


def analyze_dataset():
    with INPUT_FILE.open("r", encoding="utf-8") as file:
        dataset = json.load(file)

    mutation_engine = MutationEngine()

    totals = {
        "M1": 0,
        "M2": 0,
        "M3": 0,
        "M4": 0,
        "M5": 0,
        "M6": 0,
        "M7": 0,
        "M8": 0,
    }

    for benchmark in dataset:
        instructions = parse_tac(benchmark["tac"])

        candidates = mutation_engine.apply_all(
            instructions
        )

        print()
        print(
            f"{benchmark['id']} "
            f"[{benchmark['category']}]"
        )

        for operator, operator_candidates in candidates.items():
            count = len(operator_candidates)
            totals[operator] += count

            if count > 0:
                print(f"  {operator}: {count}")

    print()
    print("=" * 40)
    print("TOTAL MUTATION CANDIDATES")
    print("=" * 40)

    for operator, count in totals.items():
        print(f"{operator}: {count}")


if __name__ == "__main__":
    analyze_dataset()