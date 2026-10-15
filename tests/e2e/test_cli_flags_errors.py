"""E2E tests for CLI flags and error handling."""

import subprocess
import sys


def run_cli(*args):
    """Run the CLI and return (returncode, stdout, stderr)."""
    cmd = [sys.executable, "-m", "pythonesque"] + list(args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr


class TestCLIFlags:
    """Tests for CLI flag combinations."""

    def test_seed_and_count(self):
        """-s and -c together."""
        code, stdout, _ = run_cli("-s", "combo", "-c", "3")
        assert code == 0
        lines = stdout.strip().split("\n")
        assert len(lines) == 3

    def test_seed_and_unique(self):
        """-s and -u together."""
        code, stdout, _ = run_cli("-s", "combo", "-c", "5", "-u")
        assert code == 0
        lines = stdout.strip().split("\n")
        assert len(lines) == 5
        assert len(set(lines)) == 5

    def test_seed_and_slugify(self):
        """-s and -g together."""
        code, stdout, _ = run_cli("-s", "combo", "-g")
        assert code == 0
        assert " (" in stdout and stdout.strip().endswith(")")

    def test_seed_and_complexity(self):
        """-s and -x together."""
        code, stdout, _ = run_cli("-s", "combo", "-x", "2")
        assert code == 0
        assert len(stdout.strip()) > 0

    def test_seed_and_no_leading_the(self):
        """-s and -n together."""
        code, stdout, _ = run_cli("-s", "combo", "-n")
        assert code == 0
        assert not stdout.strip().startswith("The ")

    def test_all_flags_together(self):
        """All flags together should work."""
        code, stdout, _ = run_cli(
            "-s", "all-flags", "-c", "3", "-u", "-g", "-x", "1-3", "-n", "-f", "json"
        )
        assert code == 0
        import json

        data = json.loads(stdout.strip())
        assert isinstance(data, list)
        assert len(data) == 3
        for item in data:
            assert isinstance(item, list)
            assert len(item) == 2
            title, slug = item
            assert not title.startswith("The ")
            assert slug == slug.lower()

    def test_complexity_exact_with_count(self):
        """-x exact with -c."""
        code, stdout, _ = run_cli("-x", "2", "-c", "5", "-s", "complex-count")
        assert code == 0
        lines = stdout.strip().split("\n")
        assert len(lines) == 5

    def test_complexity_range_with_count(self):
        """-x range with -c."""
        code, stdout, _ = run_cli("-x", "2-4", "-c", "5", "-s", "complex-range-count")
        assert code == 0
        lines = stdout.strip().split("\n")
        assert len(lines) == 5


class TestCLIErrors:
    """Tests for CLI error handling."""

    def test_invalid_complexity_format(self):
        """Invalid complexity format should error."""
        code, stdout, stderr = run_cli("-x", "invalid")
        assert code != 0
        assert "Invalid complexity" in stderr

    def test_invalid_complexity_range_format(self):
        """Invalid complexity range format should error."""
        code, stdout, stderr = run_cli("-x", "2-3-4")
        assert code != 0
        assert "Invalid complexity" in stderr

    def test_complexity_min_greater_than_max(self):
        """Complexity min > max should error."""
        code, stdout, stderr = run_cli("-x", "5-2")
        assert code != 0
        assert "Invalid complexity range" in stderr

    def test_negative_count(self):
        """Negative count should error."""
        code, stdout, stderr = run_cli("-c", "-1")
        assert code != 0
        assert "count must be a positive integer" in stderr

    def test_zero_count(self):
        """Zero count should error."""
        code, stdout, stderr = run_cli("-c", "0")
        assert code != 0
        assert "count must be a positive integer" in stderr

    def test_invalid_format_choice(self):
        """Invalid format choice should error."""
        code, stdout, stderr = run_cli("-f", "xml")
        assert code != 0
        assert "invalid choice" in stderr.lower()

    def test_empty_seed(self):
        """Empty seed should work (uses default)."""
        code, stdout, _ = run_cli("-s", "")
        assert code == 0
        assert len(stdout.strip()) > 0

    def test_unicode_seed(self):
        """Unicode seed should work."""
        code, stdout, _ = run_cli("-s", "café 🍵")
        assert code == 0
        assert len(stdout.strip()) > 0


class TestCLIEdgeCases:
    """Tests for edge cases."""

    def test_large_count(self):
        """Large count should work."""
        code, stdout, _ = run_cli("-c", "100", "-s", "large")
        assert code == 0
        lines = stdout.strip().split("\n")
        assert len(lines) == 100

    def test_unique_with_large_count(self):
        """Unique with large count (may be limited by template variety)."""
        code, stdout, _ = run_cli("-c", "50", "-u", "-s", "large-unique")
        assert code == 0
        lines = stdout.strip().split("\n")
        # Should produce up to 50 unique titles
        assert len(lines) <= 50
        assert len(set(lines)) == len(lines)

    def test_slugify_unicode_output(self):
        """Slugify should handle unicode in generated titles."""
        code, stdout, _ = run_cli("-g", "-s", "unicode-slug")
        assert code == 0
        assert " (" in stdout
        title_part, slug_part = stdout.strip().rsplit(" (", 1)
        slug = slug_part.rstrip(")")
        # Slug should be ASCII-safe
        assert all(ord(c) < 128 for c in slug)

    def test_help_shows_examples(self):
        """Help should show examples."""
        code, stdout, _ = run_cli("-h")
        assert code == 0
        assert "Examples:" in stdout
        assert "pythonesque" in stdout

    def test_stderr_on_error(self):
        """Errors should go to stderr."""
        code, stdout, stderr = run_cli("-x", "bad")
        assert code != 0
        assert len(stderr) > 0
        assert len(stdout) == 0  # No output on error
