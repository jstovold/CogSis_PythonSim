#!/bin/bash -xe

for i in {0..100}
do
  python3 traversal.py >> outputlog10c_leq.log
done

