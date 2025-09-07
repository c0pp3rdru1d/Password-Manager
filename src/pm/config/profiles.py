from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, Optional, Set
import math
import string


# Character Classes

LOWER = set(string.ascii_lowercase)
UPPER = set(string.ascii_uppercase)
DIGITS = set(string.digits)

# Symbols chosen to be widely available in common fonts/keyboards
SYMBOLS = set("!@#$%^&*()-_=+{}[];:,./?")

# Characters that are commonly confused (can be excluded)
AMBIGIOUS = set("0Oo1lI|`'\"~")

# Safe default "base" character classes you can compose
CHARSETS: Dict[str, Set[str]] = {
    "lower": LOWER,
    "upper": UPPER,
    "digits": DIGITS,
    "symbols": SYMBOLS,
}

# Profile Model

@dataclass(frozen=True)
class PasswordProfile:
    """
    A reusable password policy/profile.

    Fields:
        name: Human-friendly profile name (also key in registry).
        length: Total password length to generate.
        allow_lower/upper/digits/symbols: Which classes are allowed to appear.
        min_lower/min_upper/min_digits/min_symbols: Per-class minimums (0+).
        exclude_chars: Specific characters to never include.
        custom_allow: Additional characters to *allow* (merged into the effective charset).
                    Useful if you need specific symbols not in the defaults!

    """

    name: str
    length: int

    allow_lower: bool = True
    allow_upper: bool = True
    allow_digits: bool = True
    allow_symbols: bool = True

    
    min_lower: bool = True
    min_upper: bool = True
    min_digits: bool = True
    allow_symbols: bool = False

    min_lower: int = 0
    min_upper: int = 0
    min_digits: int = 0
    min_symbols: int = 0

    
