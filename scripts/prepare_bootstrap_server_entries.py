#!/usr/bin/env python3
"""
Convert server entries to hex format for Psiphon Android builds.

Psiphon tunnel-core expects each embedded server entry as a hex-encoded string
(see psiphon/common/protocol/serverEntry.go decodeServerEntry).

Input: one entry per line — either already hex, or legacy plaintext:
  0 0 0 0 {"ipAddress":"...","sshPort":"22",...}

Output: server_entries.txt with one hex line per entry (for CI / PSIPHON_BOOTSTRAP_SERVER_ENTRIES).

To create the GitHub secret (run from repo root):
  python3 scripts/prepare_bootstrap_server_entries.py /path/to/server_entries_extracted.txt
  gzip -c server_entries.txt | base64 -w0 > bootstrap.b64.txt
  # Paste bootstrap.b64.txt into secret PSIPHON_BOOTSTRAP_SERVER_ENTRIES
"""

from __future__ import annotations

import gzip
import base64
import sys
from pathlib import Path


def is_hex_line(line: str) -> bool:
    s = line.strip()
    if len(s) < 40 or len(s) % 2 != 0:
        return False
    try:
        bytes.fromhex(s)
        return True
    except ValueError:
        return False


def to_hex_entry(line: str) -> str:
    line = line.strip()
    if not line:
        return ""
    if is_hex_line(line):
        return line
    return line.encode("utf-8").hex()


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        return 1

    src = Path(sys.argv[1])
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("server_entries.txt")

    count = 0
    with src.open(encoding="utf-8", errors="replace") as fin, out.open("w", encoding="utf-8") as fout:
        for raw in fin:
            hex_line = to_hex_entry(raw)
            if hex_line:
                fout.write(hex_line + "\n")
                count += 1

    print(f"Wrote {count} hex-encoded entries to {out}")

    if "--gzip-b64" in sys.argv:
        data = gzip.compress(out.read_bytes())
        b64 = base64.standard_b64encode(data).decode("ascii")
        secret_path = out.with_suffix(".b64.txt")
        secret_path.write_text(b64, encoding="utf-8")
        print(f"GitHub secret payload ({len(b64)} chars) -> {secret_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
