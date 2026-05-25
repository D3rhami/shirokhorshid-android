#!/usr/bin/env python3
"""Convert extracted server entries (text lines) to hex lines for EmbeddedValues / CI."""
import sys


def line_to_hex(line: str) -> str:
    return line.strip().encode("utf-8").hex()


def main() -> int:
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <input.txt> <output_hex.txt>", file=sys.stderr)
        return 1

    input_path, output_path = sys.argv[1], sys.argv[2]
    count = 0
    with open(input_path, encoding="utf-8") as inp, open(output_path, "w", encoding="utf-8") as out:
        for line in inp:
            line = line.strip()
            if not line:
                continue
            out.write(line_to_hex(line) + "\n")
            count += 1

    print(f"Wrote {count} hex entries to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
