import json
from pathlib import Path
from collections import defaultdict

import matplotlib.pyplot as plt


RESULTS_FILE = Path("dataset/generated/experiment_results.json")
OUTPUT_DIR = Path("dataset/generated/plots")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------
# Load experiment results
# ---------------------------------------------------------

with open(RESULTS_FILE, "r") as f:
    results = json.load(f)


# ---------------------------------------------------------
# 1. Overall Greedy vs Beam
# ---------------------------------------------------------

avg_greedy = sum(
    r["greedy_reduction_percent"] for r in results
) / len(results)

avg_beam = sum(
    r["beam_reduction_percent"] for r in results
) / len(results)

plt.figure(figsize=(7, 5))

plt.bar(
    ["Greedy Search", "Beam Search"],
    [avg_greedy, avg_beam]
)

plt.ylabel("Average Cost Reduction (%)")
plt.title("Average Optimization Improvement")

plt.tight_layout()
plt.savefig(
    OUTPUT_DIR / "01_overall_reduction.png",
    dpi=300
)
plt.close()


# ---------------------------------------------------------
# 2. Reduction by Category
# ---------------------------------------------------------

category_data = defaultdict(
    lambda: {"greedy": [], "beam": []}
)

for r in results:
    category = r["category"]

    category_data[category]["greedy"].append(
        r["greedy_reduction_percent"]
    )

    category_data[category]["beam"].append(
        r["beam_reduction_percent"]
    )


categories = list(category_data.keys())

greedy_values = [
    sum(category_data[c]["greedy"])
    / len(category_data[c]["greedy"])
    for c in categories
]

beam_values = [
    sum(category_data[c]["beam"])
    / len(category_data[c]["beam"])
    for c in categories
]


x = range(len(categories))
width = 0.35

plt.figure(figsize=(12, 6))

plt.bar(
    [i - width / 2 for i in x],
    greedy_values,
    width,
    label="Greedy"
)

plt.bar(
    [i + width / 2 for i in x],
    beam_values,
    width,
    label="Beam"
)

plt.xticks(
    list(x),
    categories,
    rotation=35,
    ha="right"
)

plt.ylabel("Average Cost Reduction (%)")
plt.xlabel("Program Category")
plt.title("Optimization Improvement by Program Category")
plt.legend()

plt.tight_layout()
plt.savefig(
    OUTPUT_DIR / "02_reduction_by_category.png",
    dpi=300
)
plt.close()


# ---------------------------------------------------------
# 3. Reduction by Program Size
# ---------------------------------------------------------

size_order = ["small", "medium", "large"]

size_data = defaultdict(
    lambda: {"greedy": [], "beam": []}
)

for r in results:
    size = r["difficulty"]

    size_data[size]["greedy"].append(
        r["greedy_reduction_percent"]
    )

    size_data[size]["beam"].append(
        r["beam_reduction_percent"]
    )


greedy_size = [
    sum(size_data[s]["greedy"])
    / len(size_data[s]["greedy"])
    for s in size_order
]

beam_size = [
    sum(size_data[s]["beam"])
    / len(size_data[s]["beam"])
    for s in size_order
]


x = range(len(size_order))

plt.figure(figsize=(8, 5))

plt.plot(
    x,
    greedy_size,
    marker="o",
    label="Greedy"
)

plt.plot(
    x,
    beam_size,
    marker="o",
    label="Beam"
)

plt.xticks(
    x,
    ["Small", "Medium", "Large"]
)

plt.xlabel("Program Size")
plt.ylabel("Average Cost Reduction (%)")
plt.title("Optimization Improvement vs Program Size")
plt.legend()

plt.tight_layout()
plt.savefig(
    OUTPUT_DIR / "03_reduction_by_size.png",
    dpi=300
)
plt.close()


# ---------------------------------------------------------
# 4. Beam Search Effort vs Program Size
# ---------------------------------------------------------

effort_data = defaultdict(list)

for r in results:
    effort_data[r["difficulty"]].append(
        r["beam_explored_candidates"]
    )


avg_effort = [
    sum(effort_data[s])
    / len(effort_data[s])
    for s in size_order
]


plt.figure(figsize=(8, 5))

plt.plot(
    range(len(size_order)),
    avg_effort,
    marker="o"
)

plt.xticks(
    range(len(size_order)),
    ["Small", "Medium", "Large"]
)

plt.xlabel("Program Size")
plt.ylabel("Average Candidates Explored")
plt.title("Beam Search Effort vs Program Size")

plt.tight_layout()
plt.savefig(
    OUTPUT_DIR / "04_beam_search_effort.png",
    dpi=300
)
plt.close()


# ---------------------------------------------------------
# 5. Beam Wins / Ties / Greedy Wins
# ---------------------------------------------------------

beam_wins = 0
greedy_wins = 0
ties = 0

for r in results:

    greedy = r["greedy_reduction_percent"]
    beam = r["beam_reduction_percent"]

    if beam > greedy + 1e-9:
        beam_wins += 1

    elif greedy > beam + 1e-9:
        greedy_wins += 1

    else:
        ties += 1


labels = [
    "Beam Better",
    "Tie",
    "Greedy Better"
]

values = [
    beam_wins,
    ties,
    greedy_wins
]


plt.figure(figsize=(7, 5))

plt.bar(
    labels,
    values
)

plt.ylabel("Number of Programs")
plt.title("Greedy vs Beam Search Outcomes")

plt.tight_layout()
plt.savefig(
    OUTPUT_DIR / "05_search_outcomes.png",
    dpi=300
)
plt.close()


# ---------------------------------------------------------
# Print Summary
# ---------------------------------------------------------

print("\nGRAPH GENERATION COMPLETE")
print("=" * 50)

print(f"Programs analysed:        {len(results)}")
print(f"Average Greedy reduction: {avg_greedy:.2f}%")
print(f"Average Beam reduction:   {avg_beam:.2f}%")

print(f"Beam better:              {beam_wins}")
print(f"Ties:                     {ties}")
print(f"Greedy better:            {greedy_wins}")

print("\nPlots generated:")

for file in sorted(OUTPUT_DIR.glob("*.png")):
    print(f"✓ {file.name}")

print(f"\nSaved in: {OUTPUT_DIR}")