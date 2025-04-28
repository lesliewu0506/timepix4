#!/usr/bin/env bash
# focus_scan.sh  ──  Fine-step Z scan + TPX-4 acquisition
# Updated: 2025-04-28  (single SSH to DAQ host, then connect to stage)

set -euo pipefail

# ───────────────────────────────
# 0.  EDIT THESE THREE VARIABLES
# ───────────────────────────────
STAGE_HOST="fastspa@192.16.192.109"
DAQ_HOST="tpx4@dskt-gst-022.nikhef.nl"
DAQ_IP="192.168.1.108"
OUT_ROOT="/localstore/tpx4/user/lesliewu/Focus2"
# ───────────────────────────────

# scan parameters (mm)
z_start=43.000
z_end=42.000
step=0.025                              # 25 µm

# convert 46.250 → 46p250 for filenames
mangle() { printf '%0.3f' "$1" | tr '.' 'p'; }

# Single-host loop: already on DAQ host, only connect to stage
z=$z_start
while (( $(echo "$z >= $z_end" | bc -l) )); do
    echo '──────────────────────────────────────────────'
    printf '🔹  Moving to Z = %.3f mm\n' "$z"

    # 1. move the stage
    ssh "$STAGE_HOST" "python3 /home/fastspa/adhartog/motion-control-thorlabs-stages-master/software/SPA/move.py -z $z"

    # 2. acquire data locally on DAQ host
    tag=$(printf '%0.3f' "$z" | tr '.' 'p')
    base="$OUT_ROOT/focus_$tag"

    echo '📡  Running Tpx4daq …  (→ '"$base"'.tpx)'
    tpx4daq -c $DAQ_IP -q 1000 -t 1

    echo '🌳  Converting to ROOT … (→ '"$base"'.root)'
    tpx4maketree -lcr -o "$base"

    # 3. next position
    z=$(echo "$z - $step" | bc -l)
done