#!/usr/bin/env python3
"""Aggregate CI gate for lesson, theorem and mastery-pool mathematical audits."""
from verify_probability_foundations import main as probability_main
from verify_inference_raoblackwell import main as raoblackwell_main
from verify_inference_second_pass import main as second_pass_main
from verify_inference_decision_precision import main as decision_precision_main
from verify_inference_mastery_alignment import main as mastery_alignment_main

def main():
    probability_main()
    raoblackwell_main()
    second_pass_main()
    decision_precision_main()
    mastery_alignment_main()

if __name__ == "__main__":
    main()
