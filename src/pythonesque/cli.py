#!/usr/bin/env python3
"""
Command Line Interface for the pythonesque generator.
"""

import argparse
import csv
import importlib.metadata
import json
import sys

from .generator import UnifiedFoundationalGenerator


def parse_complexity(complexity_str: str | None) -> int | tuple[int, int] | None:
    """
    Parse complexity string into int or tuple.

    Args:
        complexity_str: String like "3" or "2-4" or None

    Returns:
        None, int, or tuple of (min, max)
    """
    if complexity_str is None:
        return None

    if "-" in complexity_str:
        try:
            parts = complexity_str.split("-")
            if len(parts) != 2:
                raise ValueError
            min_val, max_val = int(parts[0]), int(parts[1])
            if min_val > max_val:
                raise ValueError("Minimum complexity cannot be greater than maximum")
            return (min_val, max_val)
        except ValueError:
            raise ValueError(
                f"Invalid complexity range: '{complexity_str}'. Use format 'min-max' with integers"
            )
    else:
        try:
            return int(complexity_str)
        except ValueError:
            raise ValueError(
                f"Invalid complexity value: '{complexity_str}'. Use integer or 'min-max' format"
            )


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate absurdist institutional titles in the spirit of Monty Python.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  pythonesque                          # Generate one title
  pythonesque -s "test"                # Custom seed
  pythonesque -c 5                     # Five titles
  pythonesque -u                       # Unique titles (boolean flag)
  pythonesque -g                       # Title and slug pairs
  pythonesque -x 3                     # Exactly 3 elements
  pythonesque -x 2-4                   # 2-4 elements range
  pythonesque -n                       # Strip leading "The"
  pythonesque -c 3 -f json             # JSON output
  pythonesque -c 2 -f csv              # CSV output
        """,
    )

    parser.add_argument(
        "--seed",
        "-s",
        default="The Larch",
        help='Seed for deterministic generation (default: "The Larch")',
    )

    parser.add_argument(
        "--count", "-c", type=int, default=1, help="Number of titles to generate (default: 1)"
    )

    parser.add_argument(
        "--unique", "-u", action="store_true", help="Generate unique titles (boolean flag)"
    )

    parser.add_argument(
        "--slugify", "-g", action="store_true", help="Slugify output (returns title,slug tuples)"
    )

    parser.add_argument(
        "--complexity",
        "-x",
        type=str,
        help='Title complexity: integer for exact length, or "min-max" for range',
    )

    parser.add_argument(
        "--no-leading-the", "-n", action="store_true", help='Strip leading "The " from titles'
    )

    parser.add_argument(
        "--format",
        "-f",
        choices=["json", "csv", "tsv"],
        help="Output format: json, csv, or tsv (default: plain text)",
    )

    version_str = importlib.metadata.version("pythonesque")
    parser.add_argument("--version", action="version", version=f"pythonesque {version_str}")

    try:
        args = parser.parse_args()

        # Validate count
        if args.count < 1:
            parser.error("--count must be a positive integer")

        # Parse complexity
        complexity = parse_complexity(args.complexity)

        # Create generator
        generator = UnifiedFoundationalGenerator(seed=args.seed)

        # Generate titles
        if args.unique:
            results = generator.generate_unique(
                count=args.count,
                slugify=args.slugify,
                complexity=complexity,
                allow_leading_the=not args.no_leading_the,
            )
        else:
            results = generator.generate_multiple(
                count=args.count,
                slugify=args.slugify,
                complexity=complexity,
                allow_leading_the=not args.no_leading_the,
            )

        # Output results
        if args.format == "json":
            print(json.dumps(results))
        elif args.format == "csv":
            writer = csv.writer(sys.stdout, lineterminator="\n")
            for result in results:
                if isinstance(result, tuple) and args.slugify:
                    writer.writerow([result[0], result[1]])  # title, slug
                else:
                    writer.writerow([result])  # just title
        elif args.format == "tsv":
            for result in results:
                if isinstance(result, tuple) and args.slugify:
                    print(f"{result[0]}\t{result[1]}")  # title{tab}slug
                else:
                    print(result)  # just title
        else:
            # Plain text output (default)
            for result in results:
                if isinstance(result, tuple) and args.slugify:
                    print(f"{result[0]} ({result[1]})")  # title (slug)
                else:
                    print(result)  # just title

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
