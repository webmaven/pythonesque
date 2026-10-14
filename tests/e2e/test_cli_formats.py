"""E2E tests for CLI output formats (JSON, CSV, TSV)."""

import csv
import io
import json
import subprocess
import sys


def run_cli(*args, input_text=None):
    """Run the CLI and return (returncode, stdout, stderr)."""
    cmd = [sys.executable, "-m", "pythonesque"] + list(args)
    result = subprocess.run(cmd, capture_output=True, text=True, input=input_text)
    return result.returncode, result.stdout, result.stderr


class TestCLIJSON:
    """Tests for JSON output format."""

    def test_json_single(self):
        """JSON output with single title."""
        code, stdout, _ = run_cli("-f", "json", "-s", "json-test")
        assert code == 0
        data = json.loads(stdout.strip())
        assert isinstance(data, list)
        assert len(data) == 1
        assert isinstance(data[0], str)
        assert len(data[0]) > 0

    def test_json_multiple(self):
        """JSON output with multiple titles."""
        code, stdout, _ = run_cli("-c", "3", "-f", "json", "-s", "json-multi")
        assert code == 0
        data = json.loads(stdout.strip())
        assert isinstance(data, list)
        assert len(data) == 3
        assert all(isinstance(item, str) for item in data)

    def test_json_with_slugify(self):
        """JSON output with slugify should produce array of [title, slug]."""
        code, stdout, _ = run_cli("-g", "-f", "json", "-s", "json-slug")
        assert code == 0
        data = json.loads(stdout.strip())
        assert isinstance(data, list)
        assert len(data) == 1
        item = data[0]
        assert isinstance(item, list)
        assert len(item) == 2
        assert isinstance(item[0], str)  # title
        assert isinstance(item[1], str)  # slug
        assert item[1] == item[1].lower()

    def test_json_multiple_with_slugify(self):
        """JSON output with multiple and slugify."""
        code, stdout, _ = run_cli("-c", "2", "-g", "-f", "json", "-s", "json-multi-slug")
        assert code == 0
        data = json.loads(stdout.strip())
        assert isinstance(data, list)
        assert len(data) == 2
        for item in data:
            assert isinstance(item, list)
            assert len(item) == 2
            assert isinstance(item[0], str)
            assert isinstance(item[1], str)


class TestCLICSV:
    """Tests for CSV output format."""

    def test_csv_single(self):
        """CSV output with single title."""
        code, stdout, _ = run_cli("-f", "csv", "-s", "csv-test")
        assert code == 0
        reader = csv.reader(io.StringIO(stdout.strip()))
        rows = list(reader)
        assert len(rows) == 1
        assert len(rows[0]) == 1
        assert len(rows[0][0]) > 0

    def test_csv_multiple(self):
        """CSV output with multiple titles."""
        code, stdout, _ = run_cli("-c", "3", "-f", "csv", "-s", "csv-multi")
        assert code == 0
        reader = csv.reader(io.StringIO(stdout.strip()))
        rows = list(reader)
        assert len(rows) == 3
        for row in rows:
            assert len(row) == 1
            assert len(row[0]) > 0

    def test_csv_with_slugify(self):
        """CSV output with slugify should have two columns."""
        code, stdout, _ = run_cli("-g", "-f", "csv", "-s", "csv-slug")
        assert code == 0
        reader = csv.reader(io.StringIO(stdout.strip()))
        rows = list(reader)
        assert len(rows) == 1
        assert len(rows[0]) == 2
        title, slug = rows[0]
        assert len(title) > 0
        assert len(slug) > 0
        assert slug == slug.lower()

    def test_csv_multiple_with_slugify(self):
        """CSV output with multiple and slugify."""
        code, stdout, _ = run_cli("-c", "2", "-g", "-f", "csv", "-s", "csv-multi-slug")
        assert code == 0
        reader = csv.reader(io.StringIO(stdout.strip()))
        rows = list(reader)
        assert len(rows) == 2
        for row in rows:
            assert len(row) == 2
            title, slug = row
            assert slug == slug.lower()


class TestCLITSV:
    """Tests for TSV output format."""

    def test_tsv_single(self):
        """TSV output with single title."""
        code, stdout, _ = run_cli("-f", "tsv", "-s", "tsv-test")
        assert code == 0
        lines = stdout.strip().split("\n")
        assert len(lines) == 1
        # No tabs for single title without slugify
        assert "\t" not in lines[0]
        assert len(lines[0]) > 0

    def test_tsv_multiple(self):
        """TSV output with multiple titles."""
        code, stdout, _ = run_cli("-c", "3", "-f", "tsv", "-s", "tsv-multi")
        assert code == 0
        lines = stdout.strip().split("\n")
        assert len(lines) == 3
        for line in lines:
            assert "\t" not in line
            assert len(line) > 0

    def test_tsv_with_slugify(self):
        """TSV output with slugify should have tab-separated title and slug."""
        code, stdout, _ = run_cli("-g", "-f", "tsv", "-s", "tsv-slug")
        assert code == 0
        lines = stdout.strip().split("\n")
        assert len(lines) == 1
        parts = lines[0].split("\t")
        assert len(parts) == 2
        title, slug = parts
        assert len(title) > 0
        assert len(slug) > 0
        assert slug == slug.lower()

    def test_tsv_multiple_with_slugify(self):
        """TSV output with multiple and slugify."""
        code, stdout, _ = run_cli("-c", "2", "-g", "-f", "tsv", "-s", "tsv-multi-slug")
        assert code == 0
        lines = stdout.strip().split("\n")
        assert len(lines) == 2
        for line in lines:
            parts = line.split("\t")
            assert len(parts) == 2
            title, slug = parts
            assert slug == slug.lower()


class TestCLIFormatCombinations:
    """Tests for format combinations with other flags."""

    def test_json_with_no_leading_the(self):
        """JSON with -n flag."""
        code, stdout, _ = run_cli("-f", "json", "-n", "-s", "json-no-the")
        assert code == 0
        data = json.loads(stdout.strip())
        assert isinstance(data, list)
        assert len(data) == 1
        assert isinstance(data[0], str)
        assert not data[0].startswith("The ")

    def test_csv_with_complexity(self):
        """CSV with complexity filter."""
        code, stdout, _ = run_cli("-f", "csv", "-x", "2", "-s", "csv-complex")
        assert code == 0
        reader = csv.reader(io.StringIO(stdout.strip()))
        rows = list(reader)
        assert len(rows) == 1
        assert len(rows[0][0]) > 0

    def test_tsv_with_unique(self):
        """TSV with unique flag."""
        code, stdout, _ = run_cli("-f", "tsv", "-c", "5", "-u", "-s", "tsv-unique")
        assert code == 0
        lines = stdout.strip().split("\n")
        assert len(lines) == 5
        assert len(set(lines)) == 5


class TestCLIDefaultFormat:
    """Tests for default (plain text) format."""

    def test_default_format_single(self):
        """Default format with single title."""
        code, stdout, _ = run_cli("-s", "default-test")
        assert code == 0
        assert len(stdout.strip()) > 0
        assert "\n" not in stdout.strip()

    def test_default_format_multiple(self):
        """Default format with multiple titles."""
        code, stdout, _ = run_cli("-c", "3", "-s", "default-multi")
        assert code == 0
        lines = stdout.strip().split("\n")
        assert len(lines) == 3

    def test_default_format_with_slugify(self):
        """Default format with slugify shows 'title (slug)'."""
        code, stdout, _ = run_cli("-g", "-s", "default-slug")
        assert code == 0
        assert " (" in stdout and stdout.strip().endswith(")")

    def test_default_format_multiple_with_slugify(self):
        """Default format with multiple and slugify."""
        code, stdout, _ = run_cli("-c", "2", "-g", "-s", "default-multi-slug")
        assert code == 0
        lines = stdout.strip().split("\n")
        assert len(lines) == 2
        for line in lines:
            assert " (" in line and line.endswith(")")
