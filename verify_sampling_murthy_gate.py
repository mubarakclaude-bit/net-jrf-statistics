#!/usr/bin/env python3
"""Trigger the Murthy variance and full Paper 2 mathematical audit gates."""
from verify_sampling_murthy_variance import main
from verify_full_math_audit_gate import main as full_main
if __name__ == "__main__":
    main()
    full_main()
