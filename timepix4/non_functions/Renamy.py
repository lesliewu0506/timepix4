#!/usr/bin/env python3
import sys
import os
from decimal import Decimal, getcontext

def rename_roots(root_dir: str, start: str = "4.000", step: str = "0.025"):
    """Rename all .root files in root_dir:
       sorted alphabetically → 4_000.root, 3_975.root, 3_950.root, ...
    """
    # ensure enough precision for our steps
    getcontext().prec = 6
    start_v = Decimal(start)
    step_v  = Decimal(step)

    # grab and sort all .root files
    files = sorted(f for f in os.listdir(root_dir) if f.endswith(".root"))
    if not files:
        print(f"No .root files found in {root_dir!r}")
        return

    for idx, fname in enumerate(files):
        volt = start_v - step_v * idx
        # format to 3 decimals, then swap "." → "_"
        volt_str = f"{volt:.3f}".replace(".", "_")
        newname = f"{volt_str}.root"

        src = os.path.join(root_dir, fname)
        dst = os.path.join(root_dir, newname)

        if os.path.exists(dst):
            print(f"⚠️  Skipping {fname!r}: target {newname!r} already exists")
        else:
            os.rename(src, dst)
            print(f"{fname!r} → {newname!r}")

if __name__ == "__main__":
    target_dir = "Data/Laser Measurements/Laser Measurements 4 V3"
    rename_roots(target_dir)