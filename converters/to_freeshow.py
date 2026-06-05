#!/usr/bin/env python3
"""
to_freeshow.py
==============
Converts the Bro. William Branham sermon JSON library into a FreeShow
Bible module (.fsb format) — the json-bible standard used by FreeShow.

Output file:  bro-branham-sermons.fsb
Format spec:  https://github.com/ChurchApps/json-bible

Mapping:
  Sermon collection  →  Bible  (top-level name)
  Each sermon        →  Book   (numbered chronologically)
  Each sermon        →  1 Chapter (always chapter 1)
  Each paragraph     →  Verse

Book name format:  "47-0412 · Faith Is the Substance"
Reference display: handled natively by FreeShow's Scripture template
                   using the book name + verse number

Usage:
  python3 converters/to_freeshow.py
  python3 converters/to_freeshow.py --input output/ --output modules/freeshow/bro-branham-sermons.fsb
  python3 converters/to_freeshow.py --limit 10   (test with first 10 sermons)
"""

import os
import json
import argparse
from datetime import datetime

# ── Constants ────────────────────────────────────────────────────────────────

COLLECTION_NAME = "Bro. William Branham — Messages"
PUBLISHER       = "github.com/philipatosam/bro-william-branham-sermon-library"
WARN_THRESHOLD  = 3000   # characters — paragraphs over this go into warnings.txt

# ── Helpers ──────────────────────────────────────────────────────────────────

def load_sermons(input_dir: str, limit: int = None) -> list:
    """Load and sort all sermon JSON files from input_dir chronologically."""
    files = sorted(
        [f for f in os.listdir(input_dir) if f.endswith(".json")],
        key=lambda f: f.split(" ")[0]   # sort by the YY-MMDD[X] ID prefix
    )
    if limit:
        files = files[:limit]

    sermons = []
    errors  = []
    for fname in files:
        fpath = os.path.join(input_dir, fname)
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                sermons.append(json.load(f))
        except Exception as e:
            errors.append(f"  PARSE ERROR — {fname}: {e}")

    if errors:
        print(f"  ⚠️  {len(errors)} file(s) failed to parse:")
        for e in errors:
            print(e)

    return sermons


def build_book(sermon: dict, book_number: int) -> dict:
    """Convert a single sermon dict into a json-bible Book object."""
    sid   = sermon["id"]
    title = sermon["title"]

    verses = [
        {"number": p["number"], "text": p["text"]}
        for p in sermon["paragraphs"]
    ]

    return {
        "number": book_number,
        "name": f"{sid} \u00b7 {title}",   # e.g. "47-0412 · Faith Is the Substance"
        "chapters": [
            {
                "number": 1,
                "verses": verses
            }
        ]
    }


def collect_warnings(sermons: list, threshold: int) -> list:
    """
    Identify paragraphs whose text exceeds the character threshold.
    These will display as unusably long slides in FreeShow.
    Returns a list of (sid, title, para_number, length) tuples.
    """
    warnings = []
    for sermon in sermons:
        sid   = sermon["id"]
        title = sermon["title"]
        for p in sermon["paragraphs"]:
            length = len(p["text"])
            if length > threshold:
                warnings.append((sid, title, p["number"], length))
    return warnings


def build_fsb(sermons: list) -> dict:
    """Assemble the full json-bible structure from all sermons."""
    books = [build_book(sermon, i) for i, sermon in enumerate(sermons, start=1)]

    return {
        "name": COLLECTION_NAME,
        "metadata": {
            "publisher": PUBLISHER
        },
        "books": books
    }


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Convert Bro. Branham sermon JSONs → FreeShow .fsb module"
    )
    parser.add_argument(
        "--input",
        default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output"),
        help="Folder containing individual sermon JSON files (default: ../output)"
    )
    parser.add_argument(
        "--output",
        default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "modules", "freeshow", "bro-branham-sermons.fsb"),
        help="Output .fsb file path (default: ../modules/freeshow/bro-branham-sermons.fsb)"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Process only the first N sermons (useful for testing)"
    )
    parser.add_argument(
        "--warn-threshold",
        type=int,
        default=WARN_THRESHOLD,
        help=f"Character count above which a paragraph is flagged (default: {WARN_THRESHOLD})"
    )
    args = parser.parse_args()

    input_dir   = os.path.abspath(args.input)
    output_path = os.path.abspath(args.output)
    warn_path   = os.path.join(os.path.dirname(output_path), "warnings.txt")

    # ── Validate input ───────────────────────────────────────────────────────
    if not os.path.isdir(input_dir):
        print(f"❌  Input directory not found: {input_dir}")
        return

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # ── Load ─────────────────────────────────────────────────────────────────
    print(f"\n📂  Loading sermons from: {input_dir}")
    sermons = load_sermons(input_dir, limit=args.limit)
    print(f"    Loaded {len(sermons):,} sermons")

    # ── Warnings ─────────────────────────────────────────────────────────────
    print(f"\n🔍  Scanning for long paragraphs (>{args.warn_threshold:,} chars)...")
    warnings = collect_warnings(sermons, args.warn_threshold)

    if warnings:
        with open(warn_path, "w", encoding="utf-8") as wf:
            wf.write("Bro. Branham Sermon Library — FreeShow Converter Warnings\n")
            wf.write(f"Generated : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            wf.write(f"Threshold : >{args.warn_threshold:,} characters per paragraph\n")
            wf.write(f"Note      : These paragraphs are included in the .fsb file but may\n")
            wf.write(f"            display as unusably long slides in FreeShow. Consider\n")
            wf.write(f"            manual splitting in a future pass.\n")
            wf.write("=" * 75 + "\n\n")
            wf.write(f"  {'Sermon ID':<14}  {'Para':>5}  {'Length':>10}  Title\n")
            wf.write(f"  {'-'*14}  {'-'*5}  {'-'*10}  {'-'*45}\n")
            for sid, title, para_num, length in sorted(warnings, key=lambda x: -x[3]):
                wf.write(f"  {sid:<14}  ¶{para_num:>4}  {length:>9,}  {title}\n")
        print(f"    ⚠️  {len(warnings)} paragraph(s) flagged → {warn_path}")
    else:
        print(f"    ✅  No paragraphs exceed the threshold.")

    # ── Build ────────────────────────────────────────────────────────────────
    print(f"\n🔨  Building .fsb structure...")
    fsb = build_fsb(sermons)

    total_verses = sum(
        len(ch["verses"])
        for book in fsb["books"]
        for ch in book["chapters"]
    )
    print(f"    Books (sermons) : {len(fsb['books']):,}")
    print(f"    Total verses    : {total_verses:,}")

    # ── Write ────────────────────────────────────────────────────────────────
    print(f"\n💾  Writing: {output_path}")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(fsb, f, ensure_ascii=False, separators=(",", ":"))

    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"    File size       : {size_mb:.1f} MB")
    print(f"\n✅  Done!")
    print(f"    To import into FreeShow:")
    print(f"    Scriptures drawer → ＋ → Import Bible → select bro-branham-sermons.fsb\n")


if __name__ == "__main__":
    main()
