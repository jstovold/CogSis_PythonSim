## cdm.py
## ==
## Bridge / python wrapper for native C++ code
## ==
## author: Dr James Stovold
## date  : May 26, 2022
## ==

from ctypes import *
class pyCDM():
  _cdm = None
  _lib  = None
  n_agents = 0
  def __init__(self):
    self._lib = cdll.LoadLibrary('../../native/target/libCDMSim.so')
    self._lib.createCDM.restype 	= POINTER(c_int)
    self._cdm = self._lib.createCDM()

    self._lib.setRgbReadings.restype 	= c_bool 
    self._lib.getRgbReadings.restype 	= POINTER(c_int * 3)
    self._lib.getChargeTemp.restype  	= POINTER(c_float * 2)
    self._lib.tick.restype		= c_bool
    self._lib.destroyCDM.restype	= c_bool
    self._lib.getNumAgents.restype	= c_int

    self.n_agents = self._lib.getNumAgents(self._cdm)
    self._lib.getCurrentXY.restype	= POINTER(c_float * 30) #self.n_agents * 2)
    

  def __del__(self):
    self._lib.destroyCDM(self._cdm)
    _cdm = 0;

  def setRgbReadings(self, r, g, b):
    return(self._lib.setRgbReadings(self._cdm, r, g, b))

  def getRgbReadings(self):
    rgb_ptr = self._lib.getRgbReadings(self._cdm)
    returnList = [i for i in rgb_ptr.contents]
    return(returnList)
  
  def getChargeTemp(self):
    ct_ptr = self._lib.getChargeTemp(self._cdm)
    returnList = [i for i in ct_ptr.contents]
    return(returnList)
    
  def tick(self):
    return(self._lib.tick(self._cdm))

  def getCurrentXY(self):
    xy_ptr = self._lib.getCurrentXY(self._cdm)
    xy_list = [i for i in xy_ptr.contents]
    returnList = []

    ff = False
    saved = None
    for i in xy_list:
      if ff:
        returnList.append((saved, i))
        ff = False
      else:
        saved = i
        ff = True
    return(returnList)

def main():

 cdm = pyCDM()
 print(cdm)
 print(cdm.getRgbReadings())
 cdm.setRgbReadings(500,213,1)
 print(cdm.getCurrentXY())
 print(cdm.getChargeTemp())
 print(cdm.tick())
 print(cdm.getChargeTemp())
 print(cdm.tick())
 print(cdm.getChargeTemp())
 print(cdm.tick())
 print(cdm.getChargeTemp())
 print(cdm.tick())
 print(cdm.getChargeTemp())
 print(cdm.getCurrentXY())
 print(cdm.n_agents)



 del cdm

 if False:

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
