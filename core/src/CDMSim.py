import pyCDM
import cmm
import turtle3 as cdmTurtle
import patch_turtle_image
import robotTurtle 
import time
import math
import threading

FORWARD_SPEED = 10
SLEEP_TIME    = 10

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
  _scale       = 1.0

  # need to store the turtle's environment in a bitmap image, then set that image as the turtle background to show what 
  # is going on to the user

  ticksToSleepFor = 0
  sleeping   = False
  all_stop   = False
  avoidTemp  = False
  wantCharge = False
  charging   = False
  cooling    = False

  last_rgb   = None
  rgb        = None
  cLED       = None

  def print(self, *str, suppress=True):
    if not suppress:
      print(*str)


  def __init__(self, cdmEnv, scale = 1.0, startx = 0, starty = 0):
    self._cdm    = cdmEnv
    self._arenaWidth  = 224
    self._arenaHeight = 108
    self._scale       = scale
    self._robot  = robotTurtle.robotTurtle(self._arenaWidth, self._arenaHeight, scale, startx, starty)
    #self._robot.mode('logo')

    self._robot.addLightSource((0,10), 50, 'red')
    self._robot.addLightSource((224,50), 50, 'blue')
    self._screen = self._robot._screen
    self.print(self._screen)

    self._cmm    = cmm.cmm(2, 3)

    # cheat for now, build training later...
    self._cmm.addAssociation([False, True], [False, False, True])
    self._cmm.addAssociation([True, False], [True, False, False])

#    self._cmm.addAssociation([True, True], [True, False, False])

    self._ticks  = 0;    
    self.print("polling...")
    # make sure there are some values in the buffer and that we are connected to the CDM and the env
    self.poll_sensors()  
    self.print("polling...")
    self.poll_sensors()  
    self.print("polled.")
    self._robot.goto(-75 * 4, 30 * 4)
    self._robot.setheading(125)

  def train(self):
    pass

  def tick(self):
    # check cdm output
    # pass to cmm input
    # threshold cmm output
    # pass through RGBs to wheels

    if self.sleeping and self.ticksToSleepFor > 0:
      self.ticksToSleepFor -= 1
      self.print('z', suppress=False)
      if self.ticksToSleepFor == 0:
        self.sleeping = False
      else:
        return

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

#    inputs    = [self.avoidTemp * -1, self.wantCharge * 1]
    inputs    = [self.avoidTemp * 1, self.wantCharge * 1]
    outputs   = self._cmm.recall(inputs)
    behaviour = self._cmm.thresholdResults(outputs, 1, False)
    seekRed   = behaviour[0]
    seekGreen = behaviour[1]
    seekBlue  = behaviour[2]
    self.print("behaviour" + str(behaviour), suppress=False)

    behaviour = self._cmm.thresholdResults(outputs, 1, True)
    fleeRed   = behaviour[0]
    fleeGreen = behaviour[1]
    fleeBlue  = behaviour[2]
    self.print("!behaviour" + str(behaviour), suppress=False)
    
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

    self.charging, self.cooling = self._cdm._cdm.isChargingCooling()

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


  def sleep(self, timeToSleep):
    # used in place of time.sleep() so that we can continue running certain parts of the code while other parts are 
    # sleeping without having to argue with multi-threading
    self.ticksToSleepFor += timeToSleep
    self.sleeping         = True


  def move(self, seekRed, seekGreen, seekBlue, fleeRed, fleeGreen, fleeBlue):
    # this method needs writing and calibrating according to the real robot characteristics (see page 100-101 of 
    # thesis)
    self.print("move")
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
      self.fd(FORWARD_SPEED)

#   if (self.charging and self.wantCharge) or (self.cooling and self.avoidTemp): 
    if (self.charging and self.wantCharge) or (not self.cooling and self.avoidTemp):  # seekTemp, obviously
      self.sleep(SLEEP_TIME)

  def seekflee_colour_aux(self, colourToSeek, invert=False):

    now  = self.get_colour(colourToSeek, invert)
    last = self.get_last_value(colourToSeek)

    if not invert:
      if now > last:
        self.fd(FORWARD_SPEED)
        #self.sleep(SLEEP_TIME)
      else:
        self.check_direction(colourToSeek, invert)
    else:
      if now < last:
        self.fd(FORWARD_SPEED)
        #self.sleep(SLEEP_TIME)
      else:
        self.check_direction(colourToSeek, invert)


  def seek_colour(self, colourToSeek):
    self.print("seek: " + str(colourToSeek))
    self.seekflee_colour_aux(colourToSeek, False)

  def flee_colour(self, colourToFlee):
    self.print("flee: " + str(colourToFlee))
    self.seekflee_colour_aux(colourToFlee, True)

  def get_last_value(self, colourToSeek):
    return self.last_rgb[colourToSeek]

  def get_colour(self, colourToSeek, invert=False):
    if colourToSeek == RED:
      if invert: self.centre_led(0,255,255)
      else:      self.centre_led(255,0,0)
    elif colourToSeek == GREEN:
      if invert: self.centre_led(255,0,255)
      else:      self.centre_led(0,255,0)
    elif colourToSeek == BLUE:
      if invert: self.centre_led(255,255,0)
      else:      self.centre_led(0,0,255)

    self.poll_sensors() # update current and last RGB values
    return self.rgb[colourToSeek]

  def check_direction(self, colourToSeek, invert=False):
    BRANCH_LENGTH  = 10
    BRANCH_ANGLE   = 35

    this_heading = self._robot.heading
    start = self.get_colour(colourToSeek, invert)

    self._robot.lt(BRANCH_ANGLE)
    if not self.fd(BRANCH_LENGTH):
      return
    left  = self.get_colour(colourToSeek, invert)

    self.bk(BRANCH_LENGTH)
    self._robot.rt(BRANCH_ANGLE * 2)
    if not self.fd(BRANCH_LENGTH):
      # clear buffers
      self.poll_sensors()
      self.poll_sensors()
      return
    right = self.get_colour(colourToSeek, invert)
      
#    self.bk(BRANCH_LENGTH)
    # if we run the above, we should be back where we started, facing the same direction, but we don't because if 
    # this is the direction we want to go in then it doesn't make sense to reverse again

    if not invert:      
      if start > left and start > right:
        # turn around
        self.bk(BRANCH_LENGTH)
        self._robot.rt(180 - BRANCH_ANGLE)
        self.fd(FORWARD_SPEED)
      else:
        if left > right: # turn left
          self.bk(BRANCH_LENGTH)
          self._robot.lt(BRANCH_ANGLE * 2)
          self.fd(FORWARD_SPEED)
        else:
          self.fd(FORWARD_SPEED)
    else:
      if start < left and start < right:
        # turn around
        self.bk(BRANCH_LENGTH)
        self._robot.rt(180 - BRANCH_ANGLE)
        self.fd(FORWARD_SPEED)
      else:
        if left < right: # turn left
          self.bk(BRANCH_LENGTH)
          self._robot.lt(BRANCH_ANGLE * 2)
          self.fd(FORWARD_SPEED)
        else:
          self.fd(FORWARD_SPEED)
        

  # override robot fd/bk commands to allow the avoid collisions function to subsume the behaviour accordingly 
  # (subsume? be subsumed? whatever.)

  def fd(self, distance):
    if self.avoid_collisions(distance, invert=False):
      self.print("cancelled fd")
      return False
    else:
      self._robot.fd(distance * self._scale)
      self.print("not cancelled fd")
      return True


  def bk(self, distance):
    if self.avoid_collisions(distance, invert=True):
      self.print("cancelled bk")

      return False
    else:
      self._robot.bk(distance * self._scale)
      self.print("not cancelled bk")

      return True








  def printChargeTemp(self):
    self.print("wantCharge: " + str(self.wantCharge), "find/avoidTemp: " + str(self.avoidTemp), "isCharging: " + str(self.charging), "isCooling/warming: " + str(self.cooling),  suppress=False)
    self.print(self._robot.valueHere(), suppress=False)
    self.print(self._cdm._cdm.getChargeTemp(), suppress=False)

  def avoid_collisions(self, distance = 0, invert=False):
    # if the robot gets within 10 of the wall, turn them away
    # tune the 10 according to behaviour
    
    b       = 10    # boundary size

    x       = self._robot.xcor()
    y       = self._robot.ycor()
    w       = self._arenaWidth
    h       = self._arenaHeight
    heading = self._robot.heading()
    
    if invert:
      heading += 180.0
      if heading > 360.0:
        heading -= 360

    conv    = math.pi / 180.0
    dx      = distance * math.cos(heading * conv)
    dy      = distance * math.sin(heading * conv)

    right   = (w // 2) - b
    left    = -right
    top     = (h // 2) - b
    bottom  = -top

    self.print(x, y, x+dx, y + dy, heading, left, right, top, bottom)

    x       += dx
    y       += dy


    if x > right:
      if heading > 0 and heading < 180:   # not already turned
        if heading > 90:
          self._robot.rt(90)
        else:
          self._robot.lt(90)
        if invert:
          self._robot.bk(FORWARD_SPEED * self._scale)
        else:
          self._robot.fd(FORWARD_SPEED * self._scale)
        return True

    if x < left:
      if heading < 360 and heading > 180:   # not already turned
        if heading > 270:
          self._robot.rt(90)
        else:
          self._robot.lt(90)
        if invert:
          self._robot.bk(FORWARD_SPEED * self._scale)
        else:
          self._robot.fd(FORWARD_SPEED * self._scale)
        return True

    if y < bottom:
      if heading > 90 and heading < 270:   # not already turned
        if heading > 180:
          self._robot.rt(90)
        else:
          self._robot.lt(90)
        if invert:
          self._robot.bk(FORWARD_SPEED * self._scale)
        else:
          self._robot.fd(FORWARD_SPEED * self._scale)
        return True

    if y > top:
      if heading < 90 or heading > 270:   # not already turned
        if heading < 90:
          self._robot.rt(90)
        else:
          self._robot.lt(90)
        if invert:
          self._robot.bk(FORWARD_SPEED * self._scale)
        else:
          self._robot.fd(FORWARD_SPEED * self._scale)
        return True


  # all of these headings assume we are travelling forwards...



    return False


  def centre_led(self, r, g, b):
    self.cLED = (r, g, b)
    self.update_leds()


  def update_leds(self):
    # check led status
    # update colour of turtle to match
    if self.cLED is not None:
      self._robot.color(self.cLED)
      self.cLED = None

    





def main():
    cdmEnv   = CDMEnv(60, 60, 4.0);
    robotEnv = RobotEnv(cdmEnv, scale = 4.0, startx = 25);

    while(1):
      cdmEnv.tick()  
      robotEnv.tick()



if __name__ == "__main__":
  main()
