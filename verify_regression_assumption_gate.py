#!/usr/bin/env python3
"""Trigger the regression assumption and complete math audit checks."""
from verify_regression_assumption_precision import main
from verify_full_math_audit_gate import main as full_main
if __name__ == "__main__":
    main()
    full_main()
