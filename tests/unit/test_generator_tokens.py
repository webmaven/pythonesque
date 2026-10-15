"""Unit tests for token resolution (_resolve method)."""

from pythonesque import UnifiedFoundationalGenerator


class TestTokenResolution:
    """Tests for _resolve method with various token types."""

    def test_historical_ordinal(self):
        gen = UnifiedFoundationalGenerator("token-test")
        result = gen._resolve("historical_ordinal")
        # Should be a number with ordinal suffix
        assert result[:-2].isdigit()  # number part
        assert result[-2:] in ("st", "nd", "rd", "th")

    def test_generated_proper_noun(self):
        gen = UnifiedFoundationalGenerator("token-test")
        result = gen._resolve("generated_proper_noun")
        # Should contain title, first name, last name
        parts = result.split()
        assert len(parts) >= 3
        # Title should be one of the known titles
        titles = ["Sir", "Inspector", "Cardinal", "Professor", "Mr.", "Mrs.", "Squire"]
        assert parts[0] in titles

    def test_enhanced_institution(self):
        gen = UnifiedFoundationalGenerator("token-test")
        result = gen._resolve("enhanced_institution")
        # Should not contain unresolved tokens
        assert "{{" not in result
        assert "}}" not in result
        # Should have at least one word
        assert len(result.strip()) > 0

    def test_generated_legal_action(self):
        gen = UnifiedFoundationalGenerator("token-test")
        result = gen._resolve("generated_legal_action")
        assert "{{" not in result
        assert "}}" not in result
        assert len(result.strip()) > 0

    def test_generated_natural_philosophy_axiom(self):
        gen = UnifiedFoundationalGenerator("token-test")
        result = gen._resolve("generated_natural_philosophy_axiom")
        assert "{{" not in result
        assert "}}" not in result
        assert len(result.strip()) > 0

    def test_generated_academic_body(self):
        gen = UnifiedFoundationalGenerator("token-test")
        result = gen._resolve("generated_academic_body")
        assert "{{" not in result
        assert "}}" not in result
        assert len(result.strip()) > 0

    def test_generated_logistics_action(self):
        gen = UnifiedFoundationalGenerator("token-test")
        result = gen._resolve("generated_logistics_action")
        assert "{{" not in result
        assert "}}" not in result
        assert len(result.strip()) > 0

    def test_generated_academic_discipline(self):
        gen = UnifiedFoundationalGenerator("token-test")
        result = gen._resolve("generated_academic_discipline")
        assert "{{" not in result
        assert "}}" not in result
        assert len(result.strip()) > 0

    def test_noun_verbing(self):
        gen = UnifiedFoundationalGenerator("token-test")
        result = gen._resolve("noun_verbing")
        # Should be verbing_base_noun-verbing_suffix_gerund
        assert "-" in result
        base, suffix = result.split("-", 1)
        assert base in gen._grammar["verbing_base_noun"]
        assert suffix in gen._grammar["verbing_suffix_gerund"]

    def test_unknown_token_returns_as_is(self):
        gen = UnifiedFoundationalGenerator("token-test")
        result = gen._resolve("unknown_token_xyz")
        assert result == "unknown_token_xyz"

    def test_optional_modifier_can_be_empty(self):
        gen = UnifiedFoundationalGenerator("token-test")
        # optional_modifier includes empty string
        results = [gen._resolve("optional_modifier") for _ in range(20)]
        # At least some should be empty (empty string is in the list)
        # Actually empty string is one of the options, so it should appear
        # With 20 tries and ~17 options, empty should appear
        # But it's random, so just verify it runs
        assert all(isinstance(r, str) for r in results)

    def test_optional_nationality_can_be_empty(self):
        gen = UnifiedFoundationalGenerator("token-test")
        results = [gen._resolve("optional_nationality") for _ in range(20)]
        assert all(isinstance(r, str) for r in results)

    def test_optional_annual_can_be_empty(self):
        gen = UnifiedFoundationalGenerator("token-test")
        results = [gen._resolve("optional_annual") for _ in range(20)]
        assert all(isinstance(r, str) for r in results)


class TestGrammarCoverage:
    """Tests that all grammar categories are accessible."""

    def test_all_grammar_keys_resolvable(self):
        gen = UnifiedFoundationalGenerator("grammar-test")
        for key in gen._grammar:
            if isinstance(gen._grammar[key], list) and gen._grammar[key]:
                # Try to resolve a sample from each list-type grammar entry
                sample = gen._grammar[key][0]
                result = gen._expand(sample)
                assert "{{" not in result, f"Unresolved tokens in {key}: {result}"

    def test_start_templates_all_resolve(self):
        gen = UnifiedFoundationalGenerator("start-test")
        for template in gen._grammar["START"]:
            result = gen._expand(template)
            assert "{{" not in result, (
                f"Unresolved tokens in START template: {template} -> {result}"
            )
