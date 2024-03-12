from zero_hid import Mouse
import struct

file = open( "/dev/input/mice", "rb" );
m = Mouse()
def getMouseEvent():
  buf = file.read(3)
  button = buf[0]
  bLeft = button & 0x1
  bMiddle = ( button & 0x4 ) > 0
  bRight = ( button & 0x2 ) > 0
  x,y = struct.unpack( "bb", buf[1:] )
  print ("L:%d, M: %d, R: %d, x: %d, y: %d\n" % (bLeft,bMiddle,bRight, x, y) )
  # return stuff

  m.move(x,y)


while( 1 ):
  getMouseEvent()
file.close()

