#!/usr/bin/env python3
"""Canonical JSON serializer for Regression Unit VI topic 6."""
from pathlib import Path
import sys
from tools.serialize_regression_lesson import serialize

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "seed" / "lesson_regression_t6.json"
OUTPUT = SOURCE
TOPIC = "regression-t6"

if __name__ == "__main__":
    # Optional --output PATH; otherwise serialize in place.
    output = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else OUTPUT
    serialize(SOURCE, output, TOPIC)
