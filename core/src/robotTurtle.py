import math
import time
from PIL import Image
import turtle2 as turtle

class robotTurtle(turtle.Turtle):
  _img    = None
  _pixels = None
  _scale  = 1.0
  def __init__(self, width=400,height=300, scale=1.0, startx = 0, starty = 0):
    super().__init__()
    self._scale = scale
    self._screen.mode('logo')
    self._screen.setup(width * self._scale,height * self._scale, startx = startx, starty = starty)
    w = super()._screen.window_width()
    h = super()._screen.window_height()
    self.penup()

    # set up background
    self._img    = Image.new('RGB', (w, h), 'black')
    self._pixels = self._img.load()
    self._screen.bgpic(self._img)
    self.color("white")
    self._screen.colormode(255)
    self.turtlesize(self._scale)

  def updateBackground(self):
    self._screen.bgpic(self._img)

  def setBackground(self, bg_img):
    self._img = bg_img
    self._screen.bgpic(self._img)
  

  def valueAt(self,x,y,convertToCanvas=True):
    if convertToCanvas:
      x_canv, y_canv = self.convertToCanvas(x,y)
    else:
      x_canv, y_canv = x,y
    return self._pixels[x_canv, y_canv]

  def valueHere(self, convertToCanvas=True):  
    return self.valueAt(round(self.xcor()),round(self.ycor()), convertToCanvas)

  def getValueAt(self,x,y, convertToCanvas=True):
    return self.valueAt(x,y, convertToCanvas)


  def setValueHere(self,v):
    self.setValueAt(round(self.xcor()), round(self.ycor()), v)

  def setValueAt(self,x,y,v, convertToCanvas=True):
    if convertToCanvas:
      x_canv, y_canv = self.convertToCanvas(x,y)    
    else:
      x_canv, y_canv = x,y
    self._pixels[x_canv, y_canv] = v



  def xcor(self):
    return(super().xcor() / self._scale)

  def ycor(self):
    return(super().ycor() / self._scale)


  # these functions convert between the canvas and turtle coordinate systems
  def convertToCanvas(self, x,y):
    w = super()._screen.window_width()
    h = super()._screen.window_height()

    return (x + w//2, -y + h//2)

  def convertToTurtle(self,x,y):
    w = super()._screen.window_width()
    h = super()._screen.window_height()
    return (x - w//2, -y - h//2)

  def addLightSource(self, centre, spread, colour):
    centre = self.scaleCoords(centre)
    spread = spread * self._scale
    width  = self._img.width
    height = self._img.height

    for x in range(width):
      for y in range(height):
        this_dist = math.sqrt((centre[0] - x)**2 + (centre[1] - y)**2)
        light = gaussian(this_dist, spread) * 20000 * self._scale
        currentLight = self.getValueAt(x, y, False)
        newLight = ()
        if colour == "red":
          newLight = (round(currentLight[0] + light), currentLight[1], currentLight[2])
        elif colour == "green":
          newLight = (currentLight[0], round(currentLight[1] + light), currentLight[2])
        else:
          newLight = (currentLight[0], currentLight[1], round(currentLight[2] + light))
        self.setValueAt(x,y,newLight, False)
    self.updateBackground()

  def scaleCoords(self, coords):
    return (coords[0] * self._scale, coords[1] * self._scale)


def gaussian(x_mu, sig):
  return math.exp((-0.5 * x_mu ** 2)/sig**2)/math.sqrt(2*math.pi*sig**2) 


def main():
  robot = robotTurtle(224,108, 4.0)
  robot.addLightSource((0,10), 50, 'red')
  robot.addLightSource((224,50), 50, 'blue')
  robot.updateBackground()
  while 1:
   robot.fd(1)
   time.sleep(0.2)

  robot.penup()
  for x in range(25):
    robot.fd(90)
    robot.rt(14)
    print(robot.position())
    robot.setValueHere((0,100,0))
    robot.updateBackground()

  robot.updateBackground()


if __name__ == "__main__":
  main()
