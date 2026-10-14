#!/usr/bin/env python3
"""
Command Line Interface for the pythonesque generator.
"""

import sys
import argparse
import json
import csv
from typing import List, Union, Tuple, Optional

from .generator import UnifiedFoundationalGenerator


def parse_complexity(complexity_str: Optional[str]) -> Optional[Union[int, Tuple[int, int]]]:
    """
    Parse complexity string into int or tuple.
    
    Args:
        complexity_str: String like "3" or "2-4" or None
        
    Returns:
        None, int, or tuple of (min, max)
    """
    if complexity_str is None:
        return None
    
    if '-' in complexity_str:
        try:
            parts = complexity_str.split('-')
            if len(parts) != 2:
                raise ValueError
            min_val, max_val = int(parts[0]), int(parts[1])
            if min_val > max_val:
                raise ValueError("Minimum complexity cannot be greater than maximum")
            return (min_val, max_val)
        except ValueError:
            raise ValueError(f"Invalid complexity range: '{complexity_str}'. Use format 'min-max' with integers")
    else:
        try:
            return int(complexity_str)
        except ValueError:
            raise ValueError(f"Invalid complexity value: '{complexity_str}'. Use integer or 'min-max' format")


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
  pythonesque -c 3 -j                  # JSON output
  pythonesque -c 2 --csv               # CSV output
        """
    )
    
    parser.add_argument(
        '--seed',
        '-s',
        default="The Larch",
        help='Seed for deterministic generation (default: "The Larch")'
    )
    
    parser.add_argument(
        '--count',
        '-c',
        type=int,
        default=1,
        help='Number of titles to generate (default: 1)'
    )
    
    parser.add_argument(
        '--unique',
        '-u',
        action='store_true',
        help='Generate unique titles (boolean flag)'
    )
    
    parser.add_argument(
        '--slugify',
        '-g',
        action='store_true',
        help='Slugify output (returns title,slug tuples)'
    )
    
    parser.add_argument(
        '--complexity',
        '-x',
        type=str,
        help='Title complexity: integer for exact length, or "min-max" for range'
    )
    
    parser.add_argument(
        '--no-leading-the',
        '-n',
        action='store_true',
        help='Strip leading "The " from titles'
    )
    
    parser.add_argument(
        '--json',
        '-j',
        action='store_true',
        help='Output as JSON array'
    )
    
    parser.add_argument(
        '--csv',
        action='store_true',
        help='Output as CSV (headerless, single column)'
    )
    
    parser.add_argument(
        '--tsv',
        action='store_true',
        help='Output as TSV (tab-separated, headerless)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='pythonesque 0.1.1'
    )
    
    try:
        args = parser.parse_args()
        
        # Validate mutually exclusive options
        format_flags = [args.json, args.csv, args.tsv]
        if sum(format_flags) > 1:
            parser.error("Only one output format can be specified: --json, --csv, or --tsv")
        
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
                slugify=args.slugify,
                complexity=complexity,
                allow_leading_the=not args.no_leading_the
            )
        else:
            results = generator.generate_multiple(
                count=args.count,
                slugify=args.slugify,
                complexity=complexity,
                allow_leading_the=not args.no_leading_the
            )
        
        # Output results
        if args.json:
            print(json.dumps(results))
        elif args.csv:
            writer = csv.writer(sys.stdout)
            for result in results:
                if isinstance(result, tuple) and args.slugify:
                    writer.writerow([result[0], result[1]])  # title, slug
                else:
                    writer.writerow([result])  # just title
        elif args.tsv:
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