#!/bin/bash

# Loop through q values from 4000 to 5300 with a step of 100.
for q_value in $(seq 4000 100 5300); do
    echo "Executing tpx4daqtpdo with q = ${q_value}"
    ./tpx4daqtpdo -c 192.168.1.108 -q "${q_value}" -t 1

    echo "Executing tpx4maketree for q = ${q_value} and closing ROOT file with .q"
    # Pipe '.q' into tpx4maketree to automatically close the ROOT file after opening.
    echo ".q" | tpx4maketree -lcrR -o /localstore/tpx4/user/lesliewu/data/
done