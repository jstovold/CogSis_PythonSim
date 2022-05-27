import turtle as robotTurtle
import turtle2 as cdmTurtle
import time
import threading

class CogSisTurtle(robotTurtle.Turtle):
  def __init__(self):
    super.__init__()
  
class CDMEnv():
  _screen = None
  _cdm    = None
  def __init__(self, scale = 1.0):
    _screen = cdmTurtle.Screen().setup(width  = 140 * scale,
				       height = 140 * scale, 
				       startx = 250 * scale, 
				       starty = None)
    






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
  while(1):
    time.sleep(1)

def main():
  #  t1 = threading.Thread(target=robotThread)
  #  t2 = threading.Thread(target=cdmThread)
  screen_scale = 4.0
  cdmenv   = CDMEnv(screen_scale);
  robotenv = RobotEnv(screen_scale);

  while (1):
    time.sleep(1)

if __name__ == "__main__":
  main()
