#!/usr/bin/env bash
# focus_scan.sh  ──  Fine-step Z scan + TPX-4 acquisition
# Updated: 2025-04-25  (fixed output path)

set -euo pipefail

# ───────────────────────────────
# 0.  EDIT THESE THREE VARIABLES
# ───────────────────────────────
STAGE_HOST="stagepc"                    # motion-control PC
DAQ_HOST="daqpc"                        # TPX-4 DAQ PC
DAQ_IP="192.168.1.108"                  # detector address
OUT_ROOT="/localstore/tpx4/user/lesliewu/Focus"   # ← DO NOT CREATE
# ───────────────────────────────

# scan parameters (mm)
z_start=50.000
z_end=40.000
step=0.025                              # 25 µm

# convert 46.250 → 46p250 for filenames
mangle() { printf '%0.3f' "$1" | tr '.' 'p'; }

z=$z_start
while (( $(echo "$z >= $z_end" | bc -l) )); do
    echo "──────────────────────────────────────────────"
    printf "🔹  Moving to Z = %.3f mm\n" "$z"

    # 1. move the stage
    ssh "$STAGE_HOST" "python3 /path/to/move.py -z $z"

    # 2. acquire data
    tag=$(mangle "$z")                       # e.g. 46p250
    base="${OUT_ROOT}/focus_${tag}"

    echo "📡  Running Tpx4daq …  (→ ${base}.tpx)"
    ssh "$DAQ_HOST" "Tpx4daq -c $DAQ_IP -q 1000 -t 1 -o ${base}"

    echo "🌳  Converting to ROOT … (→ ${base}.root)"
    ssh "$DAQ_HOST" "Tpx4maketree -lcr -o ${base}"

    # 3. next position
    z=$(echo "$z - $step" | bc -l)
done