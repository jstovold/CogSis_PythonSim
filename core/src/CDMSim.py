import pyCDM
import cmm
import turtle3 as cdmTurtle
import patch_turtle_image
import robotTurtle 
import time
import threading

#class CogSisTurtle(robotTurtle.Turtle):
#  def __init__(self):
#    super.__init__()
  
class CDMEnv():
  _screen 	= None
  _scale	= 1.0
  _turtles	= []
  _cdm 		= None
  _tickRate 	= 5
  _ticks	= 0
  _arenaWidth   = 0  # these store the scaled size of the arena
  _arenaHeight  = 0 
  def __init__(self, arenaWidth = 60, arenaHeight = 60, scale = 1.0):
    self._screen = cdmTurtle.Screen().setup(width = arenaWidth * scale, 
					    height = arenaHeight * scale,
					    startx = 250 * scale, 
					    starty = None)
    self._arenaWidth  = arenaWidth * scale
    self._arenaHeight = arenaHeight * scale
    self._scale = scale
    llx, lly = (0, 0)
    urx, ury = (self._arenaWidth, self._arenaHeight)
    cdmTurtle.setworldcoordinates(llx, lly, urx, ury)
    cdmTurtle.bgpic('core/src/bgimage.jpg')
    #cdmTurtle.mode('logo')
    self._cdm 	  = pyCDM.pyCDM('/Users/jamesstovold/Documents/Code/CDM_PythonSim/native/target/libCDMSim.so')
    self._ticks   = 0
    i = 0
    returnArr = self._cdm.getCurrentXY()
    for x,y,h in returnArr:
      print(x * scale,y * scale, h)
      turtle = cdmTurtle.Turtle()
      turtle.color("white")
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
  _cdm    = None  
  
  _arenaWidth  = 0
  _arenaHeight = 0

  # need to store the turtle's environment in a bitmap image, then set that image as the turtle background to show what 
  # is going on to the user

  avoidTemp  = False
  wantCharge = False
  charging   = False
  cooling    = False

  last_rgb   = None
  rgb        = None
  cLED       = None

  def __init__(self, cdmEnv, scale = 1.0, startx = 0, starty = 0):
    self._cdm    = cdmEnv
    self._arenaWidth  = 224
    self._arenaHeight = 108
    self._robot  = robotTurtle.robotTurtle(self._arenaWidth, self._arenaHeight, scale, startx, starty)
    #self._robot.mode('logo')

    self._robot.addLightSource((0,10), 50, 'red')
    self._robot.addLightSource((224,50), 50, 'blue')
    self._screen = self._robot._screen
    print(self._screen)

    self._cmm    = cmm.cmm(2, 3)
    self._ticks  = 0;    
    print("polling...")
    # make sure there are some values in the buffer and that we are connected to the CDM and the env
    self.poll_sensors()  
    print("polling...")
    self.poll_sensors()  
    print("polled.")
    self._robot.goto(-75 * 4, 30 * 4)
    self._robot.setheading(125)

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

    self.avoid_collisions()
      
    if self.wantCharge:
      self.centre_led(0,0,255)
    if self.avoidTemp:
      self.centre_led(0,255,0)
    if self.wantCharge and self.avoidTemp:
      self.centre_led(0,255,255)
    if not(self.wantCharge or self.avoidTemp):
      self.centre_led(255,255,255)

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
    self.printChargeTemp()
    self._ticks += 1

  def poll_sensors(self):

    # store current rgb values
    self.last_rgb = self.rgb

    # get new rgb values
    self.rgb = self._robot.valueHere()

    # pass to cdm
    self._cdm._cdm.setRgbReadings(self.rgb[0], self.rgb[1], self.rgb[2])

    # get current state of cdm
    self.wantCharge, self.avoidTemp = self._cdm._cdm.getCDMOutput()
    # check IR sensors for walls
    pass



  def move(self, seekRed, seekGreen, seekBlue, fleeRed, fleeGreen, fleeBlue):
    self._robot.fd(10.0)


  def printChargeTemp(self):
    print(self.wantCharge, self.avoidTemp)
    print(self._robot.valueHere())
    print(self._cdm._cdm.getChargeTemp())

  def avoid_collisions(self):
    # if the robot gets within 10 of the wall, turn them away
    # tune the 10 according to behaviour
    
    b       = 10    # boundary size

    x       = self._robot.xcor()
    y       = self._robot.ycor()
    w       = self._arenaWidth
    h       = self._arenaHeight
    heading = self._robot.heading()

    right   = (w // 2) - b
    left    = -right
    top  = (h // 2) - b
    bottom     = -top

    print(x, y, left, right, top, bottom)

    if x > right:
      if heading > 0 and heading < 180:   # not already turned
        if heading > 90:
          self._robot.rt(90)
        else:
          self._robot.lt(90)
        return

    if x < left:
      if heading < 360 and heading > 180:   # not already turned
        if heading > 270:
          self._robot.rt(90)
        else:
          self._robot.lt(90)
        return

    if y < bottom:
      if heading > 90 and heading < 270:   # not already turned
        if heading > 180:
          self._robot.rt(90)
        else:
          self._robot.lt(90)
        return

    if y > top:
      if heading < 90 or heading > 270:   # not already turned
        if heading < 90:
          self._robot.rt(90)
        else:
          self._robot.lt(90)
        return


  def centre_led(self, r, g, b):
    print('centre_led')
    self.cLED = (r, g, b)
    self.update_leds()


  def update_leds(self):
    # check led status
    # update colour of turtle to match
    print('update_leds')    
    if self.cLED is not None:
      self._robot.color(self.cLED)
      self.cLED = None
      print("leds updated")

    





def main():
    cdmEnv   = CDMEnv(60, 60, 4.0);
    robotEnv = RobotEnv(cdmEnv, scale = 4.0, startx = 25);

    while(1):
      cdmEnv.tick()  
      robotEnv.tick()



if __name__ == "__main__":
  main()
