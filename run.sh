#!/bin/bash -x


function cleanup {
  ./clear_logs.sh
}

trap cleanup EXIT

for i in {0..25}
do
  python3 core/src/CDMSim.py >> intervention.log
  python3 core/src/RandomWalk.py >> control.log
done
