"""
config package: central place for password policy profiles.

Typical usage:
    from config import get_profile, list_profiles, register_profile, PasswordProfile

    prof = get_profile("strong")
    charset = prof.effective_charset()
    print(prof.estimate_entropy_bits())
"""

from .profiles import (
    PasswordProfile,
    get_profile,
    list_profiles,
    register_profile,
)
__all__ = [
    "PasswordProfile",
    "get_profile",
    "list_profiles",
    "register_profile",
]
