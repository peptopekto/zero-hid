from zero_hid import Mouse
import struct

file = open( "/dev/input/mice", "rb" )
m = Mouse()
lastLeft = 0
lastRight = 0


def getMouseEvent():
  
  # read mouse state
  global lastLeft
  global lastRight
  buf = file.read(3)
  button = buf[0]
  bLeft = button & 0x1
  bMiddle = ( button & 0x4 ) > 0
  bRight = ( button & 0x2 ) > 0
  x,y = struct.unpack( "bb", buf[1:] )
  #print ("L:%d, M: %d, R: %d, x: %d, y: %d\n" % (bLeft,bMiddle,bRight, x, y) )



  # modify and send mouse
  m.move(x,y)

  if bLeft == 1 and lastLeft == 0:
    m.left_press()
    lastLeft = 1
  if bLeft == 0 and lastLeft == 1:
    m.left_release()
    lastLeft = 0

  if bRight == 1 and lastRight == 0:
    m.right_press()
    lastRight = 1
  if bRight == 0 and lastRight == 1:
    m.right_release()
    lastRight = 0

while( 1 ):
  getMouseEvent()
file.close()

