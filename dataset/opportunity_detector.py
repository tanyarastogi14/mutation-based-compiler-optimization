import re


def detect_opportunities(source_code: str) -> set[str]:
    """Detect optimization opportunities present in source code."""

    opportunities = set()

    # M1: x + 0 or 0 + x
    if re.search(r"\b\w+\s*\+\s*0\b", source_code):
        opportunities.add("M1")

    if re.search(r"\b0\s*\+\s*\w+\b", source_code):
        opportunities.add("M1")

    # M2: x * 1 or 1 * x
    if re.search(r"\b\w+\s*\*\s*1\b", source_code):
        opportunities.add("M2")

    if re.search(r"\b1\s*\*\s*\w+\b", source_code):
        opportunities.add("M2")

    # M3: constant arithmetic expression
    if re.search(
        r"\(\s*-?\d+\s*[\+\-\*\/]\s*-?\d+\s*\)",
        source_code,
    ):
        opportunities.add("M3")

    # M4: multiplication by 2
    if re.search(r"\b\w+\s*\*\s*2\b", source_code):
        opportunities.add("M4")

    # M7: assignment of a constant followed by use
    if re.search(
        r"\b\w+\s*=\s*-?\d+\s*;\s*"
        r"\b\w+\s*=\s*\w+\s*[\+\-\*\/]",
        source_code,
        re.DOTALL,
    ):
        opportunities.add("M7")

    # M6: repeated arithmetic expression
    expressions = re.findall(
        r"\b\w+\s*[\+\-\*\/]\s*\w+\b",
        source_code,
    )

    if len(expressions) != len(set(expressions)):
        opportunities.add("M6")

    # M5 and M8 require data-flow analysis.
    # They will be detected later from TAC rather than regex.

    return opportunities