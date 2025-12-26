#!/usr/bin/env python3
import os
import shutil
import re
from pathlib import Path

# operates in the directory where this script sits
folder = Path(__file__).resolve().parent

# variant suffixes to create
VARIANTS = ["_communist", "_fascist", "_monarchy", "_republic"]

# match base files exactly 3 alphanumeric chars before .tga (case-insensitive)
base_re = re.compile(r'^([A-Za-z0-9]{3})\.tga$', re.IGNORECASE)

created = []
skipped = []
errors = []

for entry in os.listdir(folder):
    if not entry.lower().endswith('.tga'):
        continue
    m = base_re.match(entry)
    if not m:
        continue  # not a base file (skip ideology variants or other names)
    base_name = m.group(1)  # keep as-is from filename (preserve case)
    src_path = folder / entry
    # create variants
    for suf in VARIANTS:
        tgt_name = f"{base_name}{suf}.tga"
        tgt_path = folder / tgt_name
        if tgt_path.exists():
            skipped.append(tgt_name)
            continue
        try:
            shutil.copy2(src_path, tgt_path)
            created.append(tgt_name)
        except Exception as e:
            errors.append((tgt_name, str(e)))

# summary
print("Done.\n")
if created:
    print("Created:")
    for n in created:
        print("  " + n)
else:
    print("No new variant files were created.")

if skipped:
    print("\nSkipped (already existed):")
    # show a few then count if many
    for n in skipped[:200]:
        print("  " + n)
    if len(skipped) > 200:
        print(f"  ... and {len(skipped)-200} more")

if errors:
    print("\nErrors:")
    for n, msg in errors:
        print(f"  {n}: {msg}")

input("\nPress Enter to exit...")
