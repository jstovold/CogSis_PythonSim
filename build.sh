#!/bin/bash -xe

g++ native/src/*.cpp native/src/CDMSim/*.cpp -o native/target/libCDMSim.so -fPIC -shared -std=c++11 -include /usr/include/c++/11/limits
