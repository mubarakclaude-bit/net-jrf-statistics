#!/usr/bin/env python3
"""Aggregate CI gate for the focused mathematical audit verifiers."""
from verify_probability_foundations import main as probability_main
from verify_inference_raoblackwell import main as raoblackwell_main
from verify_inference_second_pass import main as second_pass_main
from verify_inference_decision_precision import main as decision_precision_main

def main():
    probability_main()
    raoblackwell_main()
    second_pass_main()
    decision_precision_main()

if __name__ == "__main__":
    main()
