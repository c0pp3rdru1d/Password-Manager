from __future__ import annotations
from typing import Optional, List, Tuple, Callable
import secrets
from pm.config.profiles import Profile


#----Internal helpers----

def _secure_shuffle(xs: List[str]) -> None:
    """Fisher-Yates shuffle using secrets.randbelow (CSPRNG)."""
    for i in range(len(xs) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        xs[i], xs[j] = xs[j], xs[i]

def _deterministic_choice_and_shuffle(seed: int) -> Tuple[Callable[[List[str]], str], Callable[[List[str]], None]]:
    """TEST-ONLY: deterministic RNG surfaces for unit tests. Not used in Prod!"""
    import random # local import to make test-only intent explicit
    rnd = random.Random(seed)
    return rnd.choice, rnd.shuffle

def _allowed_for_rule(profile: Profile, rule: str) -> str:
    from string import ascii_lowercase, ascii_uppercase, digits
    base = {
        "lower": ascii_lowercase,
        "upper": ascii_uppercase,
        "digits": digits,
        "symbols": "!@#$%^&*()-_=+[]{};:,.<>/?",
    }[rule]
    # apply exclusions consistent with Profile._alphabet()
    if profile.exclude_similar:
        for ch in "O0oIl1|`'\"":
            base = base.replace(ch, "")
    for ch in set(profile.exclude_chars):
        base = base.replace(ch, "")
    return base

#----Public API-----


def generate_password(profile: Profile, *, deterministic_seed: Optional[int] = None) -> str:
    """Generate a password using a Profile. 
    
    - Production path uses only 'secrets' (CSPRNG).
    - If 'deterministic_seed' is provided, a **test-only** deterministic RNG is used
      so unit tests can assert on stable outputs. Do not use this mode in production!
    """

    profile.validate()
    alphabet = profile._alphabet() # Uses the validation and exclusions we built

    if deterministic_seed is not None and not __debug__:
        raise RuntimeError("Deterministic mode must not be used in production!")
    elif deterministic_seed is not None:
        choice, shuffle = _deterministic_choice_and_shuffle(deterministic_seed)
    else:
        choice = secrets.choice
        shuffle = _secure_shuffle

    
    # Satisfy must-include rules first
    result: List[str] = []
    for rule in profile.must_include:
        allowed = _allowed_for_rule(profile, rule)
        if not allowed:
            raise ValueError(f"Rule '{rule}' leaves no characters after exclusions...")
        result.append(choice(list(allowed)))

    # Fill the remainder uniformly from the full alphabet
    while len(result) < profile.length:
        result.append(choice(list(alphabet)))

    shuffle(result)
    return "".join(result)
