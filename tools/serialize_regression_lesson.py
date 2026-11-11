#!/usr/bin/env python3
"""Deterministic serializer for a regression lesson JSON seed.

The seed JSON is the reviewed source of truth. This utility validates the minimal
lesson contract and writes a stable UTF-8, two-space-indented JSON representation.
It deliberately does not generate or silently alter mathematical content.
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def serialize(source: Path, destination: Path, expected_topic: str) -> None:
    lesson = json.loads(source.read_text(encoding="utf-8"))
    required = {"id", "topicId", "moduleId", "title", "version", "status", "scenes",
                "objectives", "prereq", "refs", "provenance", "revision"}
    missing = sorted(required - lesson.keys())
    if missing:
        raise ValueError(f"{source}: missing required fields: {', '.join(missing)}")
    if lesson["moduleId"] != "regression" or lesson["topicId"] != expected_topic:
        raise ValueError(f"{source}: expected regression topic {expected_topic}")
    if not isinstance(lesson["scenes"], list) or not lesson["scenes"]:
        raise ValueError(f"{source}: scenes must be a non-empty list")
    ids = [scene.get("id") for scene in lesson["scenes"]]
    if None in ids or len(ids) != len(set(ids)):
        raise ValueError(f"{source}: scene IDs must be present and unique")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(lesson, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--topic", required=True)
    args = parser.parse_args()
    serialize(args.source, args.output, args.topic)
    print(f"Serialized {args.topic}: {args.output}")

if __name__ == "__main__":
    main()
