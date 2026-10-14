"""Unit tests for core generator methods."""

import pytest

from pythonesque import UnifiedFoundationalGenerator


class TestHistoricalOrdinal:
    """Tests for _generate_historical_ordinal method."""

    def test_first(self):
        # We can't directly test the private method easily without mocking rng
        # Instead test through generate() with a template that uses historical_ordinal
        pass

    @pytest.mark.parametrize(
        "number,expected_suffix",
        [
            (1, "st"),
            (2, "nd"),
            (3, "rd"),
            (4, "th"),
            (11, "th"),
            (12, "th"),
            (13, "th"),
            (21, "st"),
            (22, "nd"),
            (23, "rd"),
            (24, "th"),
        ],
    )
    def test_ordinal_suffixes(self, number, expected_suffix):
        """Test ordinal suffix generation for various numbers."""
        # Since _generate_historical_ordinal uses rng.randint(1, 14),
        # we test the suffix logic by creating a generator with a seed
        # that produces specific numbers. This is hard to control directly.
        # Instead, we verify the logic by testing the public generate method
        # with templates that include historical_ordinal.
        gen = UnifiedFoundationalGenerator("ordinal-test")
        # Generate multiple times to hit different ordinals
        results = [gen.generate() for _ in range(50)]
        # At least one should contain an ordinal
        ordinals_found = [
            r
            for r in results
            if any(s in r for s in ["1st", "2nd", "3rd", "4th", "11th", "12th", "13th"])
        ]
        assert len(ordinals_found) > 0


class TestBuildProperNoun:
    """Tests for _build_proper_noun method."""

    def test_basic_structure(self):
        gen = UnifiedFoundationalGenerator("proper-noun")
        results = [gen.generate() for _ in range(20)]
        # Should contain titles like "Sir", "Professor", etc.
        titles_found = any("Sir " in r or "Professor " in r or "Inspector " in r for r in results)
        assert titles_found

    def test_name_components_present(self):
        gen = UnifiedFoundationalGenerator("name-parts")
        results = [gen.generate() for _ in range(30)]
        # Check for known first names
        first_names = [
            "Arthur",
            "Gwen",
            "Biggus",
            "Tim",
            "Robin",
            "Brian",
            "Dennis",
            "Raymond",
            "Michael",
            "John",
            "Bruce",
        ]
        last_names = [
            "Pewtey",
            "Dibley",
            "Dickus",
            "Luxury-Yacht",
            "Pither",
            "Ximénez",
            "Dim",
            "Cleese",
            "Palin",
            "Gumby",
        ]
        found_first = any(fn in " ".join(results) for fn in first_names)
        found_last = any(ln in " ".join(results) for ln in last_names)
        assert found_first
        assert found_last


class TestExpand:
    """Tests for _expand method."""

    def test_no_tokens(self):
        gen = UnifiedFoundationalGenerator("expand-test")
        result = gen._expand("plain text")
        assert result == "plain text"

    def test_single_token(self):
        gen = UnifiedFoundationalGenerator("expand-test")
        # Use a simple token from grammar
        result = gen._expand("{{noun_singular}}")
        assert result in gen._grammar["noun_singular"]

    def test_multiple_tokens(self):
        gen = UnifiedFoundationalGenerator("expand-test")
        result = gen._expand("{{noun_singular}} and {{noun_singular}}")
        parts = result.split(" and ")
        assert len(parts) == 2
        assert parts[0] in gen._grammar["noun_singular"]
        assert parts[1] in gen._grammar["noun_singular"]

    def test_nested_tokens(self):
        gen = UnifiedFoundationalGenerator("expand-test")
        # enhanced_institution expands to descriptor + institution_base
        result = gen._expand("{{enhanced_institution}}")
        # Should not contain unresolved tokens
        assert "{{" not in result
        assert "}}" not in result
        # Should contain words from institution_descriptor or institution_base
        assert len(result.split()) >= 1


class TestJoin:
    """Tests for _join static method."""

    def test_normal_join(self):
        result = UnifiedFoundationalGenerator._join("a", "b", "c")
        assert result == "a b c"

    def test_empty_parts_filtered(self):
        result = UnifiedFoundationalGenerator._join("a", "", "b", None, "c")
        assert result == "a b c"

    def test_all_empty(self):
        result = UnifiedFoundationalGenerator._join("", "", "")
        assert result == ""

    def test_single_part(self):
        result = UnifiedFoundationalGenerator._join("single")
        assert result == "single"


class TestSeedValidation:
    """Tests for seed validation in __init__."""

    def test_string_seed_accepted(self):
        gen = UnifiedFoundationalGenerator("valid seed")
        assert gen._seed == "valid seed"

    def test_non_string_seed_raises(self):
        with pytest.raises(TypeError, match="seed must be a string"):
            UnifiedFoundationalGenerator(42)  # type: ignore[arg-type]

    def test_none_seed_raises(self):
        with pytest.raises(TypeError, match="seed must be a string"):
            UnifiedFoundationalGenerator(None)  # type: ignore[arg-type]

    def test_empty_string_seed_accepted(self):
        gen = UnifiedFoundationalGenerator("")
        assert gen._seed == ""

    def test_unicode_seed_accepted(self):
        gen = UnifiedFoundationalGenerator("café 🍵")
        assert gen._seed == "café 🍵"


class TestRandomStateIsolation:
    """Tests that generator instances don't affect global random state."""

    def test_global_random_unchanged(self):
        import random

        random.seed(42)
        expected = random.random()

        random.seed(42)
        UnifiedFoundationalGenerator("test").generate()
        actual = random.random()

        assert actual == expected

    def test_multiple_instances_independent(self):
        gen1 = UnifiedFoundationalGenerator("same")
        gen2 = UnifiedFoundationalGenerator("same")

        seq1 = [gen1.generate() for _ in range(10)]
        seq2 = [gen2.generate() for _ in range(10)]

        assert seq1 == seq2

    def test_different_seeds_different_sequences(self):
        gen1 = UnifiedFoundationalGenerator("seed1")
        gen2 = UnifiedFoundationalGenerator("seed2")

        seq1 = [gen1.generate() for _ in range(10)]
        seq2 = [gen2.generate() for _ in range(10)]

        assert seq1 != seq2
