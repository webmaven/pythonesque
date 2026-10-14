"""Integration tests for determinism and complexity filtering."""

from pythonesque import UnifiedFoundationalGenerator


class TestDeterminism:
    """Tests for seed-based deterministic generation."""

    def test_same_seed_same_sequence(self):
        """Same seed should produce identical sequences."""
        gen1 = UnifiedFoundationalGenerator("deterministic-seed")
        gen2 = UnifiedFoundationalGenerator("deterministic-seed")

        seq1 = [gen1.generate() for _ in range(50)]
        seq2 = [gen2.generate() for _ in range(50)]

        assert seq1 == seq2

    def test_different_seeds_different_sequences(self):
        """Different seeds should produce different sequences."""
        gen1 = UnifiedFoundationalGenerator("seed-a")
        gen2 = UnifiedFoundationalGenerator("seed-b")

        seq1 = [gen1.generate() for _ in range(20)]
        seq2 = [gen2.generate() for _ in range(20)]

        assert seq1 != seq2

    def test_seed_reproducibility_across_instances(self):
        """Multiple instances with same seed stay in sync."""
        seeds = ["test", "another", "third-seed", "unicode-café", ""]

        for seed in seeds:
            gen1 = UnifiedFoundationalGenerator(seed)
            gen2 = UnifiedFoundationalGenerator(seed)

            for _ in range(10):
                assert gen1.generate() == gen2.generate()

    def test_generate_multiple_deterministic(self):
        """generate_multiple with same seed should be deterministic."""
        gen1 = UnifiedFoundationalGenerator("multi-seed")
        gen2 = UnifiedFoundationalGenerator("multi-seed")

        results1 = gen1.generate_multiple(count=10)
        results2 = gen2.generate_multiple(count=10)

        assert results1 == results2

    def test_generate_multiple_with_slugify_deterministic(self):
        """generate_multiple with slugify should be deterministic."""
        gen1 = UnifiedFoundationalGenerator("slug-multi-seed")
        gen2 = UnifiedFoundationalGenerator("slug-multi-seed")

        results1 = gen1.generate_multiple(count=10, slugify=True)
        results2 = gen2.generate_multiple(count=10, slugify=True)

        assert results1 == results2

    def test_generate_unique_deterministic(self):
        """generate_unique with same seed should be deterministic."""
        gen1 = UnifiedFoundationalGenerator("unique-seed")
        gen2 = UnifiedFoundationalGenerator("unique-seed")

        results1 = gen1.generate_unique(count=10)
        results2 = gen2.generate_unique(count=10)

        assert results1 == results2


class TestComplexityFiltering:
    """Tests for complexity parameter in generate()."""

    def test_complexity_exact_match(self):
        """Exact complexity match should filter templates."""
        gen = UnifiedFoundationalGenerator("complexity-test")

        # Generate with complexity=1 (simple templates)
        results = [gen.generate(complexity=1) for _ in range(20)]

        # All results should come from templates with exactly 1 token
        for result in results:
            assert "{{" not in result
            assert len(result) > 0

    def test_complexity_range_match(self):
        """Complexity range should filter templates."""
        gen = UnifiedFoundationalGenerator("complexity-range-test")

        # Generate with complexity=(2, 4)
        results = [gen.generate(complexity=(2, 4)) for _ in range(20)]

        for result in results:
            assert "{{" not in result
            assert len(result) > 0

    def test_complexity_none_uses_all(self):
        """complexity=None should use all templates."""
        gen = UnifiedFoundationalGenerator("complexity-none-test")

        results = [gen.generate(complexity=None) for _ in range(20)]

        for result in results:
            assert "{{" not in result
            assert len(result) > 0

    def test_complexity_invalid_fallback(self):
        """Invalid complexity should fallback to all templates."""
        gen = UnifiedFoundationalGenerator("complexity-invalid-test")

        # Invalid complexity (e.g., negative, or min > max)
        # The implementation falls back to all templates
        results = [gen.generate(complexity=(-1, -1)) for _ in range(10)]

        for result in results:
            assert "{{" not in result
            assert len(result) > 0

    def test_complexity_with_slugify(self):
        """Complexity filtering should work with slugify."""
        gen = UnifiedFoundationalGenerator("complexity-slug-test")

        title, slug = gen.generate(slugify=True, complexity=2)

        assert isinstance(title, str)
        assert isinstance(slug, str)
        assert "{{" not in title
        assert slug == gen._slugify(title)

    def test_complexity_with_multiple(self):
        """Complexity filtering should work with generate_multiple."""
        gen = UnifiedFoundationalGenerator("complexity-multi-test")

        results = gen.generate_multiple(count=10, complexity=(1, 3))

        assert len(results) == 10
        for result in results:
            assert "{{" not in result
            assert len(result) > 0

    def test_complexity_zero_or_negative(self):
        """Zero or negative complexity should fallback."""
        gen = UnifiedFoundationalGenerator("complexity-zero-test")

        results = [gen.generate(complexity=0) for _ in range(10)]

        for result in results:
            assert "{{" not in result
            assert len(result) > 0


class TestAllowLeadingThe:
    """Tests for allow_leading_the parameter."""

    def test_allow_leading_the_true(self):
        """allow_leading_the=True should keep 'The ' prefix."""
        gen = UnifiedFoundationalGenerator("leading-the-test")

        # Generate many and check some start with "The "
        results = [gen.generate(allow_leading_the=True) for _ in range(50)]
        the_count = sum(1 for r in results if r.startswith("The "))

        # Many templates start with "The ", so we should see some
        assert the_count > 0

    def test_allow_leading_the_false(self):
        """allow_leading_the=False should strip 'The ' prefix."""
        gen = UnifiedFoundationalGenerator("no-leading-the-test")

        results = [gen.generate(allow_leading_the=False) for _ in range(50)]

        # None should start with "The "
        for result in results:
            assert not result.startswith("The ")

    def test_allow_leading_the_with_slugify(self):
        """allow_leading_the should work with slugify."""
        gen = UnifiedFoundationalGenerator("the-slug-test")

        title1, slug1 = gen.generate(slugify=True, allow_leading_the=True)
        title2, slug2 = gen.generate(slugify=True, allow_leading_the=False)

        # Slugs should be different if titles differ
        if title1 != title2:
            assert slug1 != slug2
