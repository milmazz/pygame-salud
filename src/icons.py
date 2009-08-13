# vim:ts=4:sts=4:et:nowrap:tw=77
# -*- coding: utf-8 -*-

import os
import pygame
from pygame.locals import *
from pygame.sprite import Sprite
import constants
import common

class Icons(Sprite):
   def __init__(self, id):
       Sprite.__init__(self)
       path = os.path.join(constants.icons_folder, "gartoon",
                           "process-stop.png")
       self.image, self.rect = common.load_image(path)
       x = constants.screen_mode[0] - self.image.get_width()
       y = 0
       self.rect.topleft = [x,y]
       self.id = id


class Check(Sprite):
    def __init__(self, pos=None, zoom=None):
        Sprite.__init__(self)
        self.path_check = os.path.join(constants.data_folder, \
                'icons', "check.png")
        self.image, self.rect = common.load_image(self.path_check)
        if zoom:
            size = self.rect[2] * zoom, self.rect[3] * zoom
            self.image = pygame.transform.scale(self.image, size)

        if not pos:
            pos = map(lambda x: x/2.0, constants.screen_mode)
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]

