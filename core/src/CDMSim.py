import pyCDM
import cmm
import turtle3 as cdmTurtle
import patch_turtle_image
import robotTurtle 
import time
import threading

FORWARD_SPEED = 10
SLEEP_TIME    = 1

RED   = 0
GREEN = 1
BLUE  = 2

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

  all_stop   = False
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
    if self._ticks > 5 and self.all_stop:
      return

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
    #pass
    
    # get current charge of robot (yes, I know this should be in python, but it's already been written in C++ and is 
    # running, so may as well use it!)
    charge, temp = self._cdm._cdm.getChargeTemp()

    if charge < 0.1:
      # battery dead
      self.all_stop = True
      self.centre_led(255,255,0) # yellow

    if temp > 55:
      # overheated
      self.all_stop = True
      self.centre_led(0,255,255) # cyan



  def move(self, seekRed, seekGreen, seekBlue, fleeRed, fleeGreen, fleeBlue):
    # this method needs writing and calibrating according to the real robot characteristics (see page 100-101 of 
    # thesis)
    print("move")
    # need chromotaxis algorithm implementing here, then we can calibrate according to empirical data
    if seekRed:
      self.seek_colour(RED)
    elif seekGreen:
      self.seek_colour(GREEN)
    elif seekBlue:
      self.seek_colour(BLUE)
    elif fleeRed:
      self.flee_colour(RED)
    elif fleeGreen:
      self.flee_colour(GREEN)
    elif fleeBlue:
      self.flee_colour(BLUE)
    else:
      self._robot.fd(1.0)
    while (self.charging and self.wantCharge) or (self.cooling and self.avoidTemp): 
      time.sleep(SLEEP_TIME)

  def seekflee_colour_aux(self, colourToSeek, invert=False):
    last = self.get_last_value(colourToSeek)
    now  = self.get_colour(colourToSeek, invert)

    if not invert:
      if now > last:
        self._robot.fd(FORWARD_SPEED)
        time.sleep(SLEEP_TIME)
      else:
        self.check_direction(colourToSeek, invert)
    else:
      if now < last:
        self._robot.fd(FORWARD_SPEED)
        time.sleep(SLEEP_TIME)
      else:
        self.check_direction(colourToSeek, invert)


  def seek_colour(self, colourToSeek):
    self.seekflee_colour_aux(colourToSeek, False)

  def flee_colour(self, colourToFlee):
    self.seekflee_colour_aux(colourToFlee, True)

  def get_last_value(self, colourToSeek):
    return self.last_rgb[colourToSeek]

  def get_colour(self, colourToSeek, invert=False):
    if colourToSeek == RED:
      if inverted: self.centre_led(0,255,255)
      else:        self.centre_led(255,0,0)
    elif colourToSeek == GREEN:
      if inverted: self.centre_led(255,0,255)
      else:        self.centre_led(0,255,0)
    elif colourToSeek == BLUE:
      if inverted: self.centre_led(255,255,0)
      else:        self.centre_led(0,0,255)

    self.poll_sensors() # update current and last RGB values
    return self.rgb[colourToSeek]

  def check_direction(self, colourToSeek, invert=False):
    BRANCH_LENGTH  = 10
    BRANCH_ANGLE   = 35

    this_heading = self._robot.heading
    start = self.get_colour(colourToSeek, invert)

    self._robot.lt(BRANCH_ANGLE)
    self._robot.fd(BRANCH_LENGTH)
    left  = self.get_colour(colourToSeek, invert)

    self._robot.bk(BRANCH_LENGTH)
    self._robot.rt(BRANCH_ANGLE)
    self._robot.fd(BRANCH_LENGTH)
    right = self.get_colour(colourToSeek, invert)
      
#    self._robot.bk(BRANCH_LENGTH)
    # if we run the above, we should be back where we started, facing the same direction, but we don't because if 
    # this is the direction we want to go in then it doesn't make sense to reverse again

    if not invert:      
      if start > left and start > right:
        # turn around
        self._robot.bk(BRANCH_LENGTH)
        self._robot.lt(180)
        self._robot.fd(FORWARD_SPEED)
      else:
        if left > right: # turn left
          self._robot.bk(BRANCH_LENGTH)
          self._robot.lt(BRANCH_ANGLE)
          self._robot.fd(FORWARD_SPEED)
        else:
          self._robot.fd(FORWARD_SPEED)
    else:
      if start < left and start < right:
        # turn around
        self._robot.bk(BRANCH_LENGTH)
        self._robot.lt(180)
        self._robot.fd(FORWARD_SPEED)
      else:
        if left < right: # turn left
          self._robot.bk(BRANCH_LENGTH)
          self._robot.lt(BRANCH_ANGLE)
          self._robot.fd(FORWARD_SPEED)
        else:
          self._robot.fd(FORWARD_SPEED)
        










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
    top     = (h // 2) - b
    bottom  = -top

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
