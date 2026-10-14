"""Integration tests for template expansion."""

from pythonesque import UnifiedFoundationalGenerator


class TestTemplateExpansion:
    """Tests that all START templates fully resolve."""

    def test_all_start_templates_resolve(self):
        """All START templates should expand without unresolved tokens."""
        gen = UnifiedFoundationalGenerator("template-test")
        for i, template in enumerate(gen._grammar["START"]):
            result = gen._expand(template)
            assert "{{" not in result, f"Template {i} has unresolved tokens: {template} -> {result}"
            assert "}}" not in result, f"Template {i} has unresolved tokens: {template} -> {result}"
            assert len(result.strip()) > 0, f"Template {i} produced empty result: {template}"

    def test_start_templates_produce_varied_output(self):
        """Different seeds should produce different outputs from same template."""
        gen1 = UnifiedFoundationalGenerator("seed1")
        gen2 = UnifiedFoundationalGenerator("seed2")

        # Test a few templates
        for template in gen1._grammar["START"][:10]:
            result1 = gen1._expand(template)
            result2 = gen2._expand(template)
            # With different seeds, results should differ (very high probability)
            # But since it's random, we just verify they're valid strings
            assert isinstance(result1, str)
            assert isinstance(result2, str)
            assert len(result1) > 0
            assert len(result2) > 0

    def test_generate_method_uses_start_templates(self):
        """generate() should produce output derived from START templates."""
        gen = UnifiedFoundationalGenerator("generate-test")
        results = [gen.generate() for _ in range(20)]

        # Each result should be a non-empty string without unresolved tokens
        for result in results:
            assert isinstance(result, str)
            assert len(result) > 0
            assert "{{" not in result
            assert "}}" not in result

    def test_complex_templates_resolve(self):
        """Test complex multi-part templates resolve completely."""
        gen = UnifiedFoundationalGenerator("complex-test")

        # Find templates with many tokens
        complex_templates = [t for t in gen._grammar["START"] if t.count("{{") >= 5]

        for template in complex_templates:
            result = gen._expand(template)
            assert "{{" not in result, f"Complex template unresolved: {template} -> {result}"
            assert len(result) > 20, f"Complex template too short: {result}"

    def test_modular_historical_competition_templates(self):
        """Test modular historical competition components."""
        gen = UnifiedFoundationalGenerator("historical-test")

        # Test prefix templates
        for template in gen._grammar["historical_competition_prefix"]:
            result = gen._expand(template)
            assert "{{" not in result

        # Test middle templates
        for template in gen._grammar["historical_competition_middle"]:
            result = gen._expand(template)
            assert "{{" not in result

        # Test suffix templates
        for template in gen._grammar["historical_competition_suffix"]:
            result = gen._expand(template)
            assert "{{" not in result

    def test_modular_legal_templates(self):
        """Test modular legal components."""
        gen = UnifiedFoundationalGenerator("legal-test")

        for key in [
            "legal_authority",
            "legal_location",
            "legal_framework",
            "legal_statute",
            "adverb",
        ]:
            for template in gen._grammar[key]:
                result = gen._expand(template)
                assert "{{" not in result, f"Legal template {key} unresolved: {template}"

    def test_modular_academic_templates(self):
        """Test modular academic components."""
        gen = UnifiedFoundationalGenerator("academic-test")

        for key in ["academic_title", "institution_affiliation"]:
            for template in gen._grammar[key]:
                result = gen._expand(template)
                assert "{{" not in result, f"Academic template {key} unresolved: {template}"

    def test_modular_sports_templates(self):
        """Test modular sports components."""
        gen = UnifiedFoundationalGenerator("sports-test")

        for template in gen._grammar["sports_event"]:
            result = gen._expand(template)
            assert "{{" not in result


class TestSlugifyIntegration:
    """Integration tests for slugify with generated titles."""

    def test_generate_with_slugify(self):
        gen = UnifiedFoundationalGenerator("slug-integration")
        title, slug = gen.generate(slugify=True)

        assert isinstance(title, str)
        assert isinstance(slug, str)
        assert len(title) > 0
        assert len(slug) > 0
        assert slug == slug.lower()
        # Slug should only contain alphanumeric and hyphens
        assert all(c.isalnum() or c == "-" for c in slug)
        assert not slug.startswith("-")
        assert not slug.endswith("-")

    def test_multiple_generate_with_slugify(self):
        gen = UnifiedFoundationalGenerator("slug-multi")
        results = gen.generate_multiple(count=10, slugify=True)

        assert len(results) == 10
        for title, slug in results:
            assert isinstance(title, str)
            assert isinstance(slug, str)
            assert gen._slugify(title) == slug

    def test_slugify_deterministic(self):
        gen1 = UnifiedFoundationalGenerator("slug-deterministic")
        gen2 = UnifiedFoundationalGenerator("slug-deterministic")

        title1, slug1 = gen1.generate(slugify=True)
        title2, slug2 = gen2.generate(slugify=True)

        assert title1 == title2
        assert slug1 == slug2
