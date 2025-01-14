#!/usr/bin/python

from threading import Lock, Thread
import time
from busylight.lights.embrava import Blynclight


class BlyncLightRunner:
    """Wrapper of BlyncLight with threadding."""
    red, blue, green, yellow, magenta, cyan, silver, violet, azure, orange, rose, blank = (
        255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 255, 0), (255, 0, 255), (0, 255, 255), (
        127, 127, 127), (127, 0, 255), (0, 127, 255), (255, 127, 0), (255, 0, 127), (0, 0, 0)

    def __init__(self, logger, color=(0, 0, 0), flash=0, flash_speed=4, dim=False):
        self.__blight = Blynclight.first_light()
        self.__logger = logger
        self.__mutex = Lock()
        self.__color = color
        self.__flash = flash
        self.__flash_speed = flash_speed
        self.__dim = dim
        self.__on = False
        self.stop_light()

    @property
    def colorname(self):
        """Get the string representation of the color
        """
        return self.__colorname_from_tuple(self.color)

    @colorname.setter
    def colorname(self, value):
        """Sets the string name to represent the light color
        Args:
            value: String
        """
        new_val = self.__colortuple(value)
        if self.color != new_val:
            self.logger.debug("``hit colorname setter``")
            self.color = new_val
            self.reload_light_settings()

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, value):
        """Sets the Tuple to represent the light color
        Args:
            value: Tuple
        """
        if self.__color != value:
            self.logger.debug("``hit color``")
            self.__color = value
            self.reload_light_settings()

    @property
    def on(self):
        return self.__on

    @on.setter
    def on(self, value):
        if self.__on == value:
            return
        if value:
            t = Thread(target=self.run_light)
            t.start()
        else:
            self.logger.debug("setting light to off")
            self.stop_light()
            time.sleep(1)

    @property
    def flash(self) -> int:
        return self.__flash

    @flash.setter
    def flash(self, value: int):
        if self.__flash != value:
            self.logger.debug("``hit flash setter``")
            self.__flash = value
            self.reload_light_settings()

    @property
    def flashspeed(self) -> int:
        return self.__flash_speed

    @flashspeed.setter
    def flashspeed(self, value: int):
        if self.__flash_speed != value:
            self.logger.debug("``hit flashspeed setter``")
            self.__flash_speed = value
            self.reload_light_settings()

    @property
    def dim(self):
        return self.__dim

    @dim.setter
    def dim(self, value):
        if self.__dim != value:
            self.logger.debug("``hit dim setter``")
            self.__dim = value
            self.reload_light_settings()

    @property
    def __light(self) -> Blynclight:
        return self.__blight

    @property
    def logger(self):
        return self.__logger

    @property
    def __lock(self) -> Lock:
        return self.__mutex

    def reload_light_settings(self):
        self.logger.debug("===Reloading light settings===")
        self.update_light()

    def update_light(self):
        with self.__light.batch_update():
            self.logger.debug("Light is: " + str(self.on))

            self.__light.color = self.color
            self.logger.debug("Setting light color to: " + self.colorname)
            self.logger.debug("Setting light color to: " + str(self.color))

            self.__light.flash = self.flash
            self.logger.debug("Setting light flash to: " + str(self.flash))

            self.__light.speed = self.flashspeed
            self.logger.debug("setting light flashspeed to: %s" % (self.flashspeed))

            self.__light.dim = self.dim
            self.logger.debug("Setting light dim value to: " + str(self.dim))

    def print_light_settings(self):
        self.logger.debug("Light is: " + str(self.on))
        self.logger.debug("Light color value: " + self.colorname)
        self.logger.debug("Light color tuple values: " + str(self.color))
        self.logger.debug("Light flash value: " + str(self.flash))
        self.logger.debug("Light flashspeed value: " + str(self.flashspeed))
        self.logger.debug("Light dim value: " + str(self.dim))

    def __colorname_from_tuple(self, color_tuple):
        if color_tuple == self.red:
            return 'red'
        elif color_tuple == self.blue:
            return 'blue'
        elif color_tuple == self.green:
            return 'green'
        elif color_tuple == self.yellow:
            return 'yellow'
        elif color_tuple == self.magenta:
            return 'magenta'
        elif color_tuple == self.cyan:
            return 'cyan'
        elif color_tuple == self.silver:
            return 'silver'
        else:
            return 'blank'

    def __colortuple(self, color_name):
        if color_name == 'red':
            return self.red
        elif color_name == 'blue':
            return self.blue
        elif color_name == 'green':
            return self.green
        elif color_name == 'yellow':
            return self.yellow
        elif color_name == 'magenta':
            return self.magenta
        elif color_name == 'cyan':
            return self.cyan
        elif color_name == 'silver':
            return self.silver
        else:
            self.logger.debug("no color found, returning blank")
            return self.blank

    def stop_light(self):
        self.logger.debug("Caught stop_light")
        self.color = self.blank
        self.__on = False

    def run_light(self):
        self.__lock.acquire()
        self.__on = True
        self.logger.debug("===========lock acquired===========")
        reload_int = 0
        try:
            self.update_light()
            with self.__light.batch_update():
                self.__light.reset(flush=True)
                if self.flash == 1:
                    self.__light.blink(color=self.color, speed=self.flashspeed)
                else:
                    self.__light.on(color=self.color)

            while(self.on):
                if reload_int > 10:
                    self.print_light_settings()
                    reload_int = 0
                time.sleep(1)
                reload_int += 1
        finally:
            self.on = False
            self.logger.debug("===========lock released===========")
            self.__lock.release()
