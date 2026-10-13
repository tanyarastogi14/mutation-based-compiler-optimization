import json
from pathlib import Path

from src.c_to_tac import CToTACCompiler


INPUT_FILE = Path("dataset/generated/prototype_dataset.json")
OUTPUT_FILE = Path("dataset/generated/prototype_dataset_with_tac.json")


def compile_dataset():
    with INPUT_FILE.open("r", encoding="utf-8") as file:
        dataset = json.load(file)

    compiler = CToTACCompiler()

    for benchmark in dataset:
        instructions = compiler.compile(
            benchmark["source_code"]
        )

        benchmark["tac"] = [
            str(instruction)
            for instruction in instructions
        ]

    with OUTPUT_FILE.open("w", encoding="utf-8") as file:
        json.dump(
            dataset,
            file,
            indent=2,
        )

    print("=" * 50)
    print("TAC GENERATION COMPLETE")
    print("=" * 50)
    print(f"Programs compiled: {len(dataset)}")
    print(f"Output file: {OUTPUT_FILE}")


if __name__ == "__main__":
    compile_dataset()