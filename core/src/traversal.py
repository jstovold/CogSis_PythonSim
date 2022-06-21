import robotTurtle
import time
import math
import random

FORWARD_SPEED = 5

RED   = 0
GREEN = 1
BLUE  = 2

class TraversalEnv():
  _screen = None
  _robot  = None
  _ticks  = 0

  _arenaWidth  = 0
  _arenaHeight = 0
  _scale       = 1.0

  last_rgb = None
  rgb      = None
  all_stop = False

  sleeping        = False
  ticksToSleepFor = 0

  def print(self, *str, suppress=True):
    if not suppress:
      print(*str)

  def __init__(self):
    self._arenaWidth  = 224
    self._arenaHeight = 108
    self._scale       = 4.0
    self._robot       = robotTurtle.robotTurtle(self._arenaWidth,
						self._arenaHeight,
						self._scale)
    self._robot.addLightSource((0,10), 50, 'red')
    self._robot.addLightSource((224,50), 50, 'blue')
    self._screen = self._robot._screen

    self._ticks = 0
    self.initialise_robot()
    self.poll_sensors()
    self.poll_sensors()


  def initialise_robot(self):
    min_x, max_x = -110, -80
    min_y, max_y = -40, 40
    randx = (random.random() * (min_x - max_x) + max_x) * self._scale
    randy = (random.random() * (max_y - min_y) + min_y) * self._scale
    randh = random.random() * 180

    self._robot.goto(randx, randy)
    self._robot.setheading(randh)


  def poll_sensors(self):
    self.last_rgb = self.rgb
    self.rgb = self._robot.valueHere()



  def tick(self):

    if self.rgb[BLUE] > 30:
      self.all_stop = True


    if self._ticks > 5 and self.all_stop:
      return


    if self.sleeping and self.ticksToSleepFor > 0:
      self._ticks += 1
      self.ticksToSleepFor -= 1
      self.print('z', suppress=False)
      if self.ticksToSleepFor == 0:
        self.sleeping = False
      else:
        return

    self.poll_sensors()
    self.avoid_collisions()
    self.move()

  def move(self):
    self.seek_colour(BLUE)




  def seekflee_colour_aux(self, colourToSeek, invert=False):

    last = self.get_last_value(colourToSeek)
    now  = self.get_colour(colourToSeek, invert)

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
    BRANCH_LENGTH  = 5
    BRANCH_ANGLE   = 35

    this_heading = self._robot.heading
    start = self.get_colour(colourToSeek, invert)

    self._robot.lt(BRANCH_ANGLE)
    if not self.fd(BRANCH_LENGTH):
      return
    left  = self.get_colour(colourToSeek, invert)

    self.bk(BRANCH_LENGTH)
    self._robot.rt(BRANCH_ANGLE)
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
        self._robot.rt(180)
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
        self._robot.rt(180)
        self.fd(FORWARD_SPEED)
      else:
        if left < right: # turn left
          self.bk(BRANCH_LENGTH)
          self._robot.lt(BRANCH_ANGLE)
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
      self._ticks += distance * self._scale
      self.print("not cancelled fd")
      return True


  def bk(self, distance):
    if self.avoid_collisions(distance, invert=True):
      self.print("cancelled bk")

      return False
    else:
      self._robot.bk(distance * self._scale)
      self._ticks += distance * self._scale
      self.print("not cancelled bk")

      return True




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
          self._ticks += FORWARD_SPEED * self._scale

        else:
          self._robot.fd(FORWARD_SPEED * self._scale)
          self._ticks += FORWARD_SPEED * self._scale
        return True

    if x < left:
      if heading < 360 and heading > 180:   # not already turned
        if heading > 270:
          self._robot.rt(90)
        else:
          self._robot.lt(90)
        if invert:
          self._robot.bk(FORWARD_SPEED * self._scale)
          self._ticks += FORWARD_SPEED * self._scale
        else:
          self._robot.fd(FORWARD_SPEED * self._scale)
          self._ticks += FORWARD_SPEED * self._scale
        return True

    if y < bottom:
      if heading > 90 and heading < 270:   # not already turned
        if heading > 180:
          self._robot.rt(90)
        else:
          self._robot.lt(90)
        if invert:
          self._robot.bk(FORWARD_SPEED * self._scale)
          self._ticks += FORWARD_SPEED * self._scale
        else:
          self._robot.fd(FORWARD_SPEED * self._scale)
          self._ticks += FORWARD_SPEED * self._scale
        return True

    if y > top:
      if heading < 90 or heading > 270:   # not already turned
        if heading < 90:
          self._robot.rt(90)
        else:
          self._robot.lt(90)
        if invert:
          self._robot.bk(FORWARD_SPEED * self._scale)
          self._ticks += FORWARD_SPEED * self._scale
        else:
          self._robot.fd(FORWARD_SPEED * self._scale)
          self._ticks += FORWARD_SPEED * self._scale
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
    traversalEnv = TraversalEnv()
    while(not traversalEnv.all_stop):
      traversalEnv.tick()
    print(traversalEnv._ticks)


if __name__ == "__main__":
  main()
