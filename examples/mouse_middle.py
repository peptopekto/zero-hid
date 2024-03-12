from zero_hid import Mouse
from time import sleep


with Mouse() as m:
    sleep(5)
    m.middle_press()
    m.move(0, 300)
    sleep(3)
    m.middle_release()