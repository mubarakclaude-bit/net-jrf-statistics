#!/usr/bin/env python3
"""Single CI entry point for the focused Paper 2 mathematical audit gates."""
from verify_inference_mastery_gate import main as inference_main
from verify_inference_remaining_precision import main as inference_precision_main
from verify_timeseries_precision import main as timeseries_precision_main
from verify_timeseries_identification import main as timeseries_identification_main
from verify_timeseries_variance import main as timeseries_variance_main
from verify_unit_root_acf_precision import main as unit_root_main

def main():
    inference_main()
    inference_precision_main()
    timeseries_precision_main()
    timeseries_identification_main()
    timeseries_variance_main()
    unit_root_main()

if __name__ == "__main__":
    main()
