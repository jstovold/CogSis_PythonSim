from turtle4 import TurtleScreenBase
from PIL import ImageTk

@staticmethod
def _image(filename):
    return ImageTk.PhotoImage(file=filename)

TurtleScreenBase._image = _image

