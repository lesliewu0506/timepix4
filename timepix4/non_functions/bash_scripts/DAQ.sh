set -euo pipefail

DAQ_IP="192.168.1.108"
OUT_ROOT="/localstore/tpx4/user/lesliewu/Laser Measurements 4"

echo 'Running Tpx4daq'
tpx4daq -c $DAQ_IP -q 1000 -t 2

echo 'Converting to ROOT'
tpx4maketree -lcr -o "$OUT_ROOT"
