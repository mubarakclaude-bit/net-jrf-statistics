#!/usr/bin/env python3
"""Check the syllabus and lesson references recorded for Stats formula.pdf."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent

# The learning-material worksheet contains 31 covered concepts. These are its
# topic/lesson references; the remaining four concepts were marked outside.
COVERED = [
    ("probability-t5", "probabilityt5"),
    ("probability-t6", "probabilityt6"),
    ("probability-t12", "probabilityt12"),
    ("probability-t10", "probabilityt10"),
    ("probability-t2", "probabilityt2"),
    ("probability-t3", "probabilityt3"),
    ("probability-t3", "probabilityt3"),
    ("probability-t7", "probabilityt7"),
    ("probability-t5", "probabilityt5"),
    ("probability-t4", "probabilityt4"),
    ("multivariate-t1", "multivariatet1"),
    ("probability-t9", "probabilityt9"),
    ("inference-t5", "inferencet5"),
    ("inference-t4", "mle"),
    ("inference-t13", "inferencet13"),
    ("nonparam-t7", "nonparamt7"),
    ("inference-t9", "inferencet9"),
    ("inference-t7", "inferencet7"),
    ("inference-t2", "inferencet2"),
    ("inference-t8", "inferencet8"),
    ("regression-t2", "regressiont2"),
    ("regression-t4", "regressiont4"),
    ("stochastic-t1", "stochastict1"),
    ("stochastic-t5", "stochastict5"),
    ("timeseries-t1", "timeseriest1"),
    ("timeseries-t8", "timeseriest8"),
    ("timeseries-t5", "timeseriest5"),
    ("timeseries-t7", "timeseriest7"),
    ("probability-t6", "probabilityt6"),
    ("maths-t4", "mathst4"),
    ("probability-t5", "probabilityt5"),
]


def main():
    catalog = json.loads((ROOT / "seed/catalog.json").read_text(encoding="utf-8"))
    topics = {
        topic["id"]
        for module in catalog["modules"]
        for topic in module["topics"]
    }
    lessons = {}
    for path in (ROOT / "seed").glob("lesson_*.json"):
        lesson = json.loads(path.read_text(encoding="utf-8"))
        lessons[lesson["id"]] = lesson["topicId"]

    assert len(COVERED) == 31
    assert len(COVERED) + 4 == 35
    for topic_id, lesson_id in COVERED:
        assert topic_id in topics, f"Unknown syllabus topic: {topic_id}"
        assert lessons.get(lesson_id) == topic_id, (
            f"Lesson {lesson_id} does not belong to {topic_id}"
        )
    print("PASS: 31 covered concepts map to syllabus topics and their lessons; 4 are outside.")


if __name__ == "__main__":
    main()
