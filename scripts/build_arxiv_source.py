#!/usr/bin/env python3
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "paperV_submission_source"
with zipfile.ZipFile(ROOT / "arxiv_submission_source.zip", "w", zipfile.ZIP_DEFLATED) as archive:
    for path in sorted(SOURCE.rglob("*")):
        if path.is_file() and path.name != "main.pdf" and not path.name.endswith((".aux", ".log")):
            archive.write(path, path.relative_to(SOURCE))
print("ARXIV_SOURCE_BUILT")
