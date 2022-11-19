import random
import time
from threading import Thread


class ColorUpdater(Thread):
    def __init__(self, widget):
        Thread.__init__(self)
        self.widget = widget
        self.running = True

    def run(self):
        for i in range(0, 100):
            if not self.running:
                break
            r = lambda: random.randint(0, 255)
            self.widget.set_background_color('#%02X%02X%02X' % (r(), r(), r()))
            time.sleep(1)

    def kill(self):
        self.running = False
