from __future__ import annotations

import argparse

from .converter import convert_html_file


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Convert HTML UI structure to QML")
    parser.add_argument("--input", required=True, help="Path to source HTML file")
    parser.add_argument("--output", required=True, help="Path to output QML file")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    warnings = convert_html_file(args.input, args.output)
    print(f"✅ QML generated: {args.output}")
    if warnings:
        print("\nWarnings:")
        for warning in warnings:
            print(f"- {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
