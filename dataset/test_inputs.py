import random


def generate_test_inputs(
    parameters: list[str],
    rng: random.Random,
    count: int = 8,
) -> list[dict[str, int]]:
    test_inputs = []
    seen = set()

    while len(test_inputs) < count:
        test_case = {
            parameter: rng.randint(-10, 10)
            for parameter in parameters
        }

        key = tuple(test_case[parameter] for parameter in parameters)

        if key not in seen:
            seen.add(key)
            test_inputs.append(test_case)

    return test_inputs