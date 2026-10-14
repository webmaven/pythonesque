"""Unit tests for _fix_indefinite_articles method."""

from pythonesque import UnifiedFoundationalGenerator


class TestFixIndefiniteArticles:
    """Tests for _fix_indefinite_articles method."""

    def test_a_before_consonant(self):
        gen = UnifiedFoundationalGenerator("article-test")
        result = gen._fix_indefinite_articles("A cat")
        assert result == "A cat"

    def test_an_before_vowel(self):
        gen = UnifiedFoundationalGenerator("article-test")
        result = gen._fix_indefinite_articles("A apple")
        assert result == "An apple"

    def test_an_before_honest(self):
        gen = UnifiedFoundationalGenerator("article-test")
        result = gen._fix_indefinite_articles("A honest person")
        assert result == "An honest person"

    def test_an_before_honor(self):
        gen = UnifiedFoundationalGenerator("article-test")
        result = gen._fix_indefinite_articles("A honor")
        assert result == "An honor"

    def test_an_before_hour(self):
        gen = UnifiedFoundationalGenerator("article-test")
        result = gen._fix_indefinite_articles("A hour")
        assert result == "An hour"

    def test_an_before_heir(self):
        gen = UnifiedFoundationalGenerator("article-test")
        result = gen._fix_indefinite_articles("A heir")
        assert result == "An heir"

    def test_lowercase_a_before_vowel(self):
        gen = UnifiedFoundationalGenerator("article-test")
        result = gen._fix_indefinite_articles("a apple")
        assert result == "an apple"

    def test_lowercase_an_before_consonant(self):
        gen = UnifiedFoundationalGenerator("article-test")
        result = gen._fix_indefinite_articles("an cat")
        assert result == "a cat"

    def test_multiple_articles_in_text(self):
        gen = UnifiedFoundationalGenerator("article-test")
        result = gen._fix_indefinite_articles("A cat and a apple")
        assert result == "A cat and an apple"

    def test_no_article_no_change(self):
        gen = UnifiedFoundationalGenerator("article-test")
        result = gen._fix_indefinite_articles("The cat")
        assert result == "The cat"

    def test_word_boundary_respected(self):
        gen = UnifiedFoundationalGenerator("article-test")
        # "A" as part of another word should not be changed
        result = gen._fix_indefinite_articles("A about")
        # "about" starts with vowel, so "A about" -> "An about"
        assert result == "An about"

    def test_case_preservation(self):
        gen = UnifiedFoundationalGenerator("article-test")
        # "A" at start of sentence
        result = gen._fix_indefinite_articles("A apple")
        assert result == "An apple"
        # "a" in middle
        result = gen._fix_indefinite_articles("Give a apple")
        assert result == "Give an apple"

    def test_hyphenated_words(self):
        gen = UnifiedFoundationalGenerator("article-test")
        # Hyphenated words after article
        result = gen._fix_indefinite_articles("A well-known fact")
        assert result == "A well-known fact"  # "well-known" starts with consonant

        result = gen._fix_indefinite_articles("A apple-pie")
        assert result == "An apple-pie"  # "apple-pie" starts with vowel

    def test_integration_with_generate(self):
        gen = UnifiedFoundationalGenerator("article-integration")
        # Generate many titles and check that articles are fixed
        results = [gen.generate() for _ in range(100)]
        for title in results:
            # Should not have "A " followed by vowel word
            # (This is a basic check - the method is applied internally)
            assert "A apple" not in title
            assert "A honest" not in title
            assert "A hour" not in title
            assert "A heir" not in title
