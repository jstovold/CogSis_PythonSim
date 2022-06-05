import pyCDM
import cmm
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
      turtle.speed(0)     # disable animation
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
  _ticks  = 0
  _cmm    = None
  
  # need to store the turtle's environment in a bitmap image, then set that image as the turtle background to show what 
  # is going on to the user

  avoidTemp  = False
  wantCharge = False
  charging   = False
  cooling    = False

  def __init__(self, scale = 1.0):
    self._screen = robotTurtle.Screen().setup(width  = 200 * scale, 
					      height = 140 * scale, 
					      startx = 25  * scale, 
					      starty = None)
    self._robot = robotTurtle.Turtle()
    self._cmm   = cmm(2, 3)
    self._ticks = 0;    


  def train(self):
    pass

  def tick(self):
    # check cdm output
    # pass to cmm input
    # threshold cmm output
    # pass through RGBs to wheels

    self.poll_sensors()
    # pass sensor readings to CDM
    # read current output from CDM
    inputs    = [self.avoidTemp * -1, self.wantCharge * 1]
    outputs   = self._cmm.recall(inputs)
    behaviour = self._cmm.thresholdResults(outputs, 1, False)
    seekRed   = behaviour[0]
    seekGreen = behaviour[1]
    seekBlue  = behaviour[2]

    behaviour = self._cmm.thresholdResults(outputs, 1, True)
    fleeRed   = behaviour[0]
    fleeGreen = behaviour[1]
    fleeBlue  = behaviour[2]
    
    self.move(seekRed, seekGreen, seekBlue, fleeRed, fleeGreen, fleeBlue)

    self._ticks += 1

  def poll_sensors(self):
    # store current rgb values
    # get new rgb values
    # pass to cdm
    # check IR sensors for walls
    pass

  def move(self, seekRed, seekGreen, seekBlue, fleeRed, fleeGreen, fleeBlue):
    pass

  def avoid_collisions(self):
    pass

  def update_leds(self):
    # check led status
    # update colour of turtle to match
    pass






def main():

    cdmenv   = CDMEnv(4.0);
    robotEnv = RobotEnv(4.0);

    while(1):
      cdmenv.tick()  
      robotEnv.tick()



if __name__ == "__main__":
  main()
