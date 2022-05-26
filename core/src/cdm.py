## cdm.py
## ==
## Bridge / python wrapper for native C++ code
## ==
## author: Dr James Stovold
## date  : May 26, 2022
## ==


from ctypes import *

def main():
  lib = cdll.LoadLibrary('../../native/target/libCDMSim.so')
  lib.createCDM.restype 	= POINTER(c_int)
  lib.setRgbReadings.restype 	= c_bool 
  lib.getRgbReadings.restype    = POINTER(c_int * 3)
  cdm = lib.createCDM()
  print(cdm)
  print(lib.setRgbReadings(cdm, 4, 5, 6))
  rgb_ptr = lib.getRgbReadings(cdm)
  print([i for i in rgb_ptr.contents])
  rgb_ptr = lib.getRgbReadings(cdm)
  print([i for i in rgb_ptr.contents])
  print(lib.setRgbReadings(cdm, 4, 23, 6))
  rgb_ptr = lib.getRgbReadings(cdm)
  print([i for i in rgb_ptr.contents])

if __name__ == "__main__":
  main()
