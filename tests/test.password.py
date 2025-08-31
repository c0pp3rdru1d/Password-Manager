import pytest
import string
from src.generators.password import PasswordGenerator


class TestPasswordGenerator:
    def setup_method(self):
        """Setup for each test method"""
        self.generator = PasswordGenerator()

    def test_password_length(self):
        """Test that generated password has correct length"""
        for length in [8, 12, 16, 20]:
            password = self.generator.generate(length=length)
            assert len(password) == length

    def test_password_contains_required_characters(self):
        """Test password contains required character types"""
        password = self.generator.generate(
            length=20,
            min_upper=2,
            min_lower=2,
            min_digits=2,
            min_symbols=2
        )

        upper_count = sum(1 for c in password if c in string.ascii_uppercase)
        lower_count = sum(1 for c in password if c in string.ascii_lowercase)
        digit_count = sum(1 for c in password if c in string.digits)
        symbol_count = sum(1 for c in password if c in string.punctuation)

        assert upper_count >= 2
        assert lower_count >= 2
        assert digit_count >= 2
        assert symbol_count >= 2

    def test_password_excludes_ambiguous(self):
        """Test that ambiguous characers are excluded when requested"""
        ambiguous = '0O1lI'
        password = self.generator.generate(
            length=100, # Long password to increase chance of catching errors
            exclude_ambiguous=True
        )

        for char in ambiguous:
            assert char not in password
    
    def test_password_uniqueness(self):
        """Test that multiple passwords are unique"""
        passwords = [self.generator.generate() for _ in range(100)]
        assert len(passwords) == len(set(passwords))

    def test_invalid_requirements_raises_error(self):
        """Test that impossible requirements raise appropriate error"""
        with pytest.raises(ValueError):
            # Length too small for requirements
            self.generator.generate(
                length=3,
                min_upper=2,
                min_lower=2,
                min_digits=2,
            )

    @pytest.mark.parametrize("length, expected", [
        (8, 8),
        (12, 12),
        (16, 16),
        (32, 32),
    ])

    def test_various_lengths(self, length, expected):
        """Parametrized test for various password lengths"""
        password = self.generator.generate(length=length)
        assert len(password) == expected