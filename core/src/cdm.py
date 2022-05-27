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
  lib.getChargeTemp.restype     = POINTER(c_float * 2)
  lib.tick.restype		= c_bool
  lib.destroyCDM.restype	= c_bool

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
  
  ct_ptr = lib.getChargeTemp(cdm)
  print([i for i in ct_ptr.contents])

  for j in range(50):  
    lib.tick(cdm)
  
    ct_ptr = lib.getChargeTemp(cdm)
    print([i for i in ct_ptr.contents])
    
    if (j == 25):
      lib.setRgbReadings(cdm, 565, 12, 40)
  
  

if __name__ == "__main__":
  main()
