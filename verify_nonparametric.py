#!/usr/bin/env python3
"""Run every independent numerical verifier for Non-parametric topics 5.1–5.8."""
import subprocess
import sys

for topic in range(1, 9):
    script = f"verify_nonparam_t{topic}.py"
    print(f"\n=== Non-parametric topic 5.{topic}: {script} ===", flush=True)
    subprocess.run([sys.executable, "-I", script], check=True)

print("\nPASS: all eight Non-parametric topic verifiers completed.")
