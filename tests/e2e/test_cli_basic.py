"""E2E tests for CLI basic generation."""

import subprocess
import sys


def run_cli(*args, input_text=None):
    """Run the CLI and return (returncode, stdout, stderr)."""
    cmd = [sys.executable, "-m", "pythonesque"] + list(args)
    result = subprocess.run(cmd, capture_output=True, text=True, input=input_text)
    return result.returncode, result.stdout, result.stderr


class TestCLIBasic:
    """Tests for basic CLI generation."""

    def test_default_generation(self):
        """Default generation should produce one title."""
        code, stdout, stderr = run_cli()
        assert code == 0
        assert len(stdout.strip()) > 0
        assert "{{" not in stdout
        assert "}}" not in stdout

    def test_custom_seed(self):
        """Custom seed should produce deterministic output."""
        code1, stdout1, _ = run_cli("-s", "test-seed")
        code2, stdout2, _ = run_cli("-s", "test-seed")

        assert code1 == 0
        assert code2 == 0
        assert stdout1 == stdout2

    def test_different_seeds_different_output(self):
        """Different seeds should produce different output."""
        code1, stdout1, _ = run_cli("-s", "seed-a")
        code2, stdout2, _ = run_cli("-s", "seed-b")

        assert code1 == 0
        assert code2 == 0
        assert stdout1 != stdout2

    def test_count_multiple(self):
        """-c N should produce N titles."""
        code, stdout, _ = run_cli("-c", "5")
        assert code == 0
        lines = stdout.strip().split("\n")
        assert len(lines) == 5

    def test_count_with_seed(self):
        """-c with -s should produce deterministic multiple titles."""
        code1, stdout1, _ = run_cli("-c", "3", "-s", "multi-seed")
        code2, stdout2, _ = run_cli("-c", "3", "-s", "multi-seed")

        assert code1 == 0
        assert code2 == 0
        assert stdout1 == stdout2

    def test_unique_flag(self):
        """-u should generate unique titles."""
        code, stdout, _ = run_cli("-c", "10", "-u", "-s", "unique-test")
        assert code == 0
        lines = stdout.strip().split("\n")
        assert len(lines) == 10
        assert len(set(lines)) == 10  # All unique

    def test_slugify_flag(self):
        """-g should output title (slug) pairs."""
        code, stdout, _ = run_cli("-g", "-s", "slug-test")
        assert code == 0
        # Output format: "title (slug)"
        assert "(" in stdout and ")" in stdout
        title_part, slug_part = stdout.strip().rsplit(" (", 1)
        slug = slug_part.rstrip(")")
        assert slug == slug.lower()
        assert all(c.isalnum() or c == "-" for c in slug)

    def test_slugify_with_count(self):
        """-g with -c should output multiple title (slug) pairs."""
        code, stdout, _ = run_cli("-c", "3", "-g", "-s", "slug-multi")
        assert code == 0
        lines = stdout.strip().split("\n")
        assert len(lines) == 3
        for line in lines:
            assert " (" in line and line.endswith(")")

    def test_complexity_exact(self):
        """-x N should filter by exact complexity."""
        code, stdout, _ = run_cli("-x", "1", "-s", "complexity-test")
        assert code == 0
        assert len(stdout.strip()) > 0

    def test_complexity_range(self):
        """-x min-max should filter by complexity range."""
        code, stdout, _ = run_cli("-x", "2-4", "-s", "complexity-range-test")
        assert code == 0
        assert len(stdout.strip()) > 0

    def test_no_leading_the(self):
        """-n should strip leading 'The '."""
        code, stdout, _ = run_cli("-n", "-c", "20", "-s", "no-the-test")
        assert code == 0
        lines = stdout.strip().split("\n")
        for line in lines:
            assert not line.startswith("The ")

    def test_no_leading_the_with_slugify(self):
        """-n should work with -g."""
        code, stdout, _ = run_cli("-n", "-g", "-s", "no-the-slug")
        assert code == 0
        assert " (" in stdout


class TestCLIVersion:
    """Tests for version flag."""

    def test_version_flag(self):
        """--version should print version and exit."""
        code, stdout, stderr = run_cli("--version")
        # version flag exits with 0 but prints to stdout
        assert code == 0
        assert "pythonesque" in stdout
        assert "0.1.1" in stdout

    def test_version_short_flag(self):
        """-V should not exist (only --version)."""
        # argparse doesn't define -V, so this should error
        code, stdout, stderr = run_cli("-V")
        assert code != 0  # Should error


class TestCLIHelp:
    """Tests for help output."""

    def test_help_flag(self):
        """-h should show help."""
        code, stdout, stderr = run_cli("-h")
        assert code == 0
        assert "usage:" in stdout.lower()
        assert "monty python" in stdout.lower()

    def test_help_long_flag(self):
        """--help should show help."""
        code, stdout, stderr = run_cli("--help")
        assert code == 0
        assert "usage:" in stdout.lower()
