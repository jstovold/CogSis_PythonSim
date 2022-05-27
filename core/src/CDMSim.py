import pyCDM
import turtle2 as robotTurtle
import turtle as cdmTurtle
import time
import threading

class CogSisTurtle(robotTurtle.Turtle):
  def __init__(self):
    super.__init__()
  
class CDMEnv():
  _screen 	= None
  _scale	= 1.0
  _turtles	= []
  _cdm 		= None
  _tickRate 	= 5
  _ticks	= 0
  
  def __init__(self, scale = 1.0):
    self._screen  = cdmTurtle.Screen().setup(width  = 140 * scale,
					     height = 140 * scale, 
					     startx = 250 * scale, 
					     starty = None)
    self._scale = scale
    #cdmTurtle.mode('logo')
    self._cdm 	  = pyCDM.pyCDM('/Users/jamesstovold/Documents/Code/CDM_PythonSim/native/target/libCDMSim.so')
    self._ticks   = 0
    i = 0
    returnArr = self._cdm.getCurrentXY()
    for x,y,h in returnArr:
      print(x * scale,y * scale, h)
      turtle = cdmTurtle.Turtle()
      turtle.penup()
      turtle.setpos(x * scale,y * scale)
      turtle.setheading(h)
      self._turtles.append(turtle)
      
  def __del__(self):
    del self._cdm

  def tick(self):
    for t in range(self._tickRate):
      self._cdm.tick()
      self._ticks += 1

    self.drawEnvironment()

  def drawEnvironment(self):
    coordList = self._cdm.getCurrentXY()
    i = 0
    for x,y,h in coordList:
      self._turtles[i].setpos(x * self._scale, y * self._scale)
      self._turtles[i].setheading(h)
      i += 1




class RobotEnv():
  _screen = None
  _robot  = None
  def __init__(self, scale = 1.0):
    _screen = robotTurtle.Screen().setup(width  = 200 * scale, 
					 height = 140 * scale, 
					 startx = 25  * scale, 
					 starty = None)
    _robot = robotTurtle.Turtle()
    





def robotThread():
  while(1):
    time.sleep(1)

def cdmThread():
  pass
def main():
    # robotenv = RobotEnv(4.0);

    # t1 = threading.Thread(target=robotThread)
    # t2 = threading.Thread(target=cdmThread)
    # t1.start()
    # t2.start()

    cdmenv   = CDMEnv(4.0);

    while(1):
      cdmenv.tick()  




if __name__ == "__main__":
  main()
