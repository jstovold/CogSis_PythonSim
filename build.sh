#!/bin/bash -x -e

g++ native/src/*.cpp native/src/CDMSim/*.cpp -o native/target/libCDMSim.so -fPIC -shared -std=c++11
