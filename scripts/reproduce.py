#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

def run(*args):
    print("$", " ".join(map(str, args)))
    subprocess.run(args, cwd=ROOT, check=True)

run(sys.executable, "scripts/build_figures.py")
run(sys.executable, "scripts/check_temporal_descent.py")
run(sys.executable, "scripts/check_future_orientation.py")
run("tectonic", "paperV_submission_source/main.tex")
run(sys.executable, "scripts/build_arxiv_source.py")
run(sys.executable, "-m", "pytest", "-q")
print("FOUNDATION_PAPER_V_PREPARATION_REPRODUCTION_COMPLETE")
