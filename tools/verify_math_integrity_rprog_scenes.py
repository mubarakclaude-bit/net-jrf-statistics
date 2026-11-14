#!/usr/bin/env python3
"""Check R lesson worked steps match their stated prompts and explanations."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def scene(file_name, scene_id):
    data = json.loads((ROOT / "seed" / file_name).read_text(encoding="utf-8"))
    return next(s for s in data["scenes"] if s["id"] == scene_id)


def main():
    s6 = scene("lesson_rprog_t6.json", "s6")
    assert "c(NA,4,NA,8,10)" in s6["problem"]
    assert "4, 8 and 10" in s6["solution"][0]["math"]
    assert s6["solution"][1]["say"] == "Count observed values."
    assert "2 + 6 + 10" not in json.dumps(s6, ensure_ascii=False)

    s8 = scene("lesson_rprog_t6.json", "s8")
    assert "c(1,NA,3,9)" in s8["problem"]
    assert "1, 3 and 9" in s8["solution"][0]["math"]
    assert "13/3" in s8["solution"][2]["math"]
    assert s8["solution"][0]["say"] == "List the observed values."
    assert s8["solution"][2]["say"] == "Compute the mean and median."

    fmt = scene("lesson_rprog_t7.json", "s8")
    assert "format(x,nsmall=2)" in fmt["problem"]
    assert "character representation" in fmt["solution"][0]["math"]
    assert "x[[1]]" not in json.dumps(fmt, ensure_ascii=False)
    assert "format() returns character output" in fmt["solution"][0]["why"]

    io = scene("lesson_rprog_t8.json", "s6")
    assert "sample.csv" in io["problem"]
    assert "read.csv" in io["solution"][0]["math"]
    assert "write.csv" in io["solution"][1]["math"]
    assert io["solution"][0]["say"] == "Import the CSV file."

    docs = scene("lesson_rprog_t9.json", "s8")
    assert "tracked edits" in docs["problem"]
    assert "Track Changes" in docs["solution"][0]["math"]
    assert "reference manager" in docs["solution"][2]["math"]
    assert docs["solution"][1]["say"] == "Add reviewer feedback."

    print("PASS: R missing-value examples match their vectors and summaries")
    print("PASS: format(), CSV I/O and document-review steps match their prompts")


if __name__ == "__main__":
    main()
