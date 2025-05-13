set -euo pipefail

STAGE_HOST="fastspa@192.16.192.109"
DAQ_HOST="tpx4@dskt-gst-022.nikhef.nl"
DAQ_IP="192.168.1.108"
OUT_ROOT="/localstore/tpx4/user/lesliewu/YFocus 3.5 V"
# ───────────────────────────────

# scan parameters (mm)
y_start=42.500
y_end=42.275
step=0.005

# convert 46.250 → 46p250 for filenames
mangle() { printf '%0.3f' "$1" | tr '.' 'p'; }

# Single-host loop: already on DAQ host, only connect to stage
y=$y_start
while (( $(echo "$y >= $y_end" | bc -l) )); do
    echo '──────────────────────────────────────────────'
    printf '🔹  Moving to Y = %.3f mm\n' "$y"

    # 1. move the stage
    ssh "$STAGE_HOST" "python3 /home/fastspa/adhartog/motion-control-thorlabs-stages-master/software/SPA/move.py -y $y"

    # 2. acquire data locally on DAQ host
    tag=$(printf '%0.3f' "$y" | tr '.' 'p')
    base="$OUT_ROOT/focus_$tag"

    echo '📡  Running Tpx4daq …  (→ '"$base"'.tpx)'
    tpx4daq -c $DAQ_IP -q 1000 -t 1

    echo '🌳  Converting to ROOT … (→ '"$base"'.root)'
    tpx4maketree -lcr -o "$base"

    # 3. next position
    y=$(echo "$y - $step" | bc -l)
done
