from pm.config.profiles import Profile
from pm.generators.password import generate_password


def test_length_and_must_include():
    p = Profile(name="t", length=18, must_include=["upper","digits"], use_symbols=False)