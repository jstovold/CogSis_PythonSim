#!/bin/bash -x


function cleanup {
  ./clear_logs.sh
}

trap cleanup EXIT

python3 core/src/CDMSim.py
