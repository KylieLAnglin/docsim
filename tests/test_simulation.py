import math

from docsim.library import simulation


def test_mutate():
    test_string = "test"
    mutated_string = simulation.mutate(test_string)
    assert mutated_string != test_string
    assert mutated_string.isdigit()


def test_mutate_tokens():
    mutate_proportion = 0.4
    test_strings = [
        "this",
        "is",
        "a",
        "test",
        "of",
        "the",
        "public" "announcement",
        "system",
    ]
    mutated_strings = simulation.mutate_tokens(mutate_proportion, test_strings)
    expected_mutations = math.floor(mutate_proportion * len(test_strings))

    num_matches = sum(
        test != mutated for (test, mutated) in zip(test_strings, mutated_strings)
    )

    assert num_matches == expected_mutations