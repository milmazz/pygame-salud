# vim:ts=4:sts=4:et:nowrap:tw=77
# -*- coding: utf-8 -*-

import os
import pygame
from pygame.locals import *
import constants
import common

class Icons(pygame.sprite.Sprite):
   def __init__(self, id):
       pygame.sprite.Sprite.__init__(self)
       path = os.path.join(constants.icons_folder, "gartoon",
                           "process-stop.png")
       self.image, self.rect = common.load_image(path)
       x = constants.screen_mode[0] - self.image.get_width()
       y = 0
       self.rect.topleft = [x,y]
       self.id = id


class Check(pygame.sprite.Sprite):
    def __init__(self, pos=None, zoom=0, size=None):
        pygame.sprite.Sprite.__init__(self)
        self.path_check = os.path.join(constants.data_folder, \
                'icons', "check.png")
        self.image, self.rect = common.load_image(self.path_check)
        if zoom != 0:
            size = self.rect[2] * zoom, self.rect[3] * zoom
            self.image = pygame.transform.scale(self.image, size)
        if zoom == 0 and size:
            self.image = pygame.transform.scale(self.image, size)
        if not pos:
            pos = map(lambda x: x/2.0, constants.screen_mode)
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]

class Navigation(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.path_next = os.path.join(constants.icons_folder, 'gartoon',
                                    "next.png")
        self.path_prev = os.path.join(constants.icons_folder, 'gartoon',
                                    "prev.png")
        self.next, self.next_rect = common.load_image(self.path_next)
        self.prev, self.prev_rect = common.load_image(self.path_prev)
        self.next_rect.move_ip(constants.screen_mode[0] - \
                self.next_rect[2] - 5, constants.screen_mode[1] - \
                self.next_rect[3] - 5)
        self.prev_rect.move_ip(5, constants.screen_mode[1] - \
                self.prev_rect[3] - 5)
        self.image = self.next
        self.rect = self.next_rect

    def update(self):
        if self.image == self.next:
            self.image = self.prev
            self.rect = self.prev_rect
        else:
            self.image = self.next
            self.rect = self.next_rect
