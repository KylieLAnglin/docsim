# proportion

# Steps:
# - Tokenize
# - Mutate tokens
# - Compute similarity scores

import math
import random
from typing import Callable, Generator, List, Optional


def mutate(token: str) -> str:
    """Mutate a token by replacing it with a number."""
    num_to_return = random.choice(range(1_000_000))
    return str(num_to_return)


def mutate_tokens(
    mutate_proportion: float, tokens: List[str], mutate_fn: Optional[Callable] = mutate
) -> List[str]:
    """Mutate a given proportion of tokens in a list."""
    num_tokens = len(tokens)
    num_tokens_to_mutate = math.floor(mutate_proportion * num_tokens)
    token_indices_to_mutate = random.sample(range(num_tokens), num_tokens_to_mutate)
    mutated_tokens = []
    for i in range(num_tokens):
        if i in token_indices_to_mutate:
            mutated_token = mutate_fn(tokens[i])
        else:
            mutated_token = tokens[i]
        mutated_tokens.append(mutated_token)

    return mutated_tokens
