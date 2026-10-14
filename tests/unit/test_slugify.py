"""Unit tests for _slugify method."""

from pythonesque import UnifiedFoundationalGenerator


class TestSlugify:
    """Tests for _slugify method."""

    def test_basic_lowercase(self):
        gen = UnifiedFoundationalGenerator("slug-test")
        result = gen._slugify("Hello World")
        assert result == "hello-world"

    def test_already_lowercase(self):
        gen = UnifiedFoundationalGenerator("slug-test")
        result = gen._slugify("hello world")
        assert result == "hello-world"

    def test_numbers_preserved(self):
        gen = UnifiedFoundationalGenerator("slug-test")
        result = gen._slugify("Test 123")
        assert result == "test-123"

    def test_special_characters_replaced(self):
        gen = UnifiedFoundationalGenerator("slug-test")
        result = gen._slugify("Test!@#$%^&*()")
        # Non-alphanumeric replaced with hyphens; symbols get word replacements
        # @ -> at, $ -> usd, % -> pct, & -> and
        assert result == "test-at-usd-pct-and"

    def test_unicode_transliteration(self):
        gen = UnifiedFoundationalGenerator("slug-test")
        test_cases = [
            ("café", "cafe"),
            ("naïve", "naive"),
            ("résumé", "resume"),
            ("piñata", "pinata"),
            ("über", "uber"),
            # Cyrillic not in transliteration map, becomes empty after stripping
            ("Москва", ""),
        ]
        for input_text, expected in test_cases:
            result = gen._slugify(input_text)
            assert result == expected, f"Failed for {input_text}: got {result}, expected {expected}"

    def test_symbol_to_word_mapping(self):
        gen = UnifiedFoundationalGenerator("slug-test")
        test_cases = [
            ("A & B", "a-and-b"),
            ("$100", "usd-100"),
            ("50%", "50-pct"),
            ("user@example.com", "user-at-example-com"),
            ("C++", "c-plus-plus"),
        ]
        for input_text, expected in test_cases:
            result = gen._slugify(input_text)
            assert result == expected, f"Failed for {input_text}: got {result}, expected {expected}"

    def test_multiple_hyphens_normalized(self):
        gen = UnifiedFoundationalGenerator("slug-test")
        result = gen._slugify("Test---Multiple---Hyphens")
        assert result == "test-multiple-hyphens"

    def test_leading_trailing_hyphens_trimmed(self):
        gen = UnifiedFoundationalGenerator("slug-test")
        result = gen._slugify("-leading-and-trailing-")
        assert result == "leading-and-trailing"
        assert not result.startswith("-")
        assert not result.endswith("-")

    def test_length_limit(self):
        gen = UnifiedFoundationalGenerator("slug-test")
        long_text = "a" * 150
        result = gen._slugify(long_text)
        assert len(result) <= 100
        assert not result.endswith("-")

    def test_empty_string(self):
        gen = UnifiedFoundationalGenerator("slug-test")
        result = gen._slugify("")
        assert result == ""

    def test_only_special_chars(self):
        gen = UnifiedFoundationalGenerator("slug-test")
        result = gen._slugify("!@#$%")
        # Symbols get replaced with words, then become hyphen-separated
        assert result == "at-usd-pct"

    def test_spaces_to_hyphens(self):
        gen = UnifiedFoundationalGenerator("slug-test")
        result = gen._slugify("multiple   spaces")
        assert result == "multiple-spaces"

    def test_mixed_case_and_symbols(self):
        gen = UnifiedFoundationalGenerator("slug-test")
        result = gen._slugify("The Ministry of Silly Walks!")
        assert result == "the-ministry-of-silly-walks"

    def test_slugify_integration_with_generate(self):
        gen = UnifiedFoundationalGenerator("integration-test")
        title, slug = gen.generate(slugify=True)
        assert isinstance(title, str)
        assert isinstance(slug, str)
        assert len(title) > 0
        assert len(slug) > 0
        assert slug == slug.lower()
        assert slug.replace("-", "").isalnum() or slug == ""
        # Slug should be derived from title
        assert gen._slugify(title) == slug
