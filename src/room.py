# vim:ts=4:sts=4:et:nowrap:tw=77
# -*- coding: utf-8 -*-

import sys
import os
import math

import pygame
from pygame import *
from pygame.locals import *

import constants
import common
from activity import Activity
from icons import Icons, Check


class Room(Activity):
    def __init__(self, screen):
        Activity.__init__(self, screen)
        self.wrong_pos = [
                Rect(490, 272, 21, 29),
                Rect(439, 315, 47, 21),
                Rect(435, 355, 34, 29),
                Rect(458, 376, 45, 47),
                Rect(517, 372, 63, 36),
                Rect(614, 370, 37, 41),
                Rect(525, 421, 33, 30),
                Rect(567, 454, 25, 20),
                Rect(510, 473, 34, 33),
                Rect(467, 505, 36, 23),
                Rect(541, 516, 33, 28),
                Rect(639, 432, 53, 45),
                Rect(738, 329, 41, 23),
                Rect(722, 206, 29, 21),
                Rect(713, 176, 33, 20),
                Rect(653, 196, 30, 26),
                Rect(519, 271, 61, 52),
                Rect(583, 290, 24, 22),
                Rect(591, 318, 29, 38),
                Rect(401, 536, 105, 61),
                Rect(720, 248, 74, 33),
                ]

        self.found = 0

        self.screen = screen
        path = os.path.join(constants.data_folder, "backgrounds", 'illustration_020_021.png')
        self.background, rect = common.load_image(path)

        self.title = ("¡Orden en mi habitación!",)
        self.instructions = ("Observa estas dos habitaciones. Una está ordenada",
                "y la otra desordenada: descubre las 21 diferencias y",
                "márcalas con una X en la habitación desordenada")

        self.icons = pygame.sprite.Group()
        self.icons.add([Icons('stop')])

        self.pointer_ = Xs()
        self.pointer = sprite.RenderUpdates([self.pointer_, self.icons])
        self.xs = sprite.RenderUpdates()

        self.xs.draw(self.screen)
        self.pointer.draw(self.screen)

        self.check = sprite.RenderUpdates()
        
        self.room = Rect(403, 129, 393, 467)
        pygame.display.update()

    def info_text(self, messages, pos, size=constants.font_default[1], bg=None):
        font = pygame.font.SysFont(constants.font_default[0], size)
        font_height = font.get_linesize()

        for message in messages:
            message = unicode(message, 'utf-8')
            text = font.render(message, True, constants.font_default_color)
            text_pos = pos
            bg.blit(text, text_pos)
            pos[1] += font_height
 
    def informative_text(self, title, instructions):
        font_title = pygame.font.SysFont(constants.font_title[0],
                                         constants.font_title[1])

        tsize = font_title.size(title[0])

        title_pos = [(constants.screen_mode[0] - tsize[0]) / 2.0, 0]
       
        tsize = font_title.get_linesize()
        instructions_pos = [10, title_pos[1] + tsize]

        self.info_text(title, title_pos, size=constants.font_title[1], bg=self.background)
        self.info_text(instructions, instructions_pos, bg=self.background)

    def setup(self):
        self.informative_text(self.title, self.instructions)
        self.pointer.draw(self.screen)

    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        for event in self.get_event():
            mouse_pos = pygame.mouse.get_pos()
            if event.type == QUIT:
                self.quit = True
                return
            elif event.type == KEYUP:
                self.changed = False
                if event.key == K_ESCAPE:
                    self.quit = True                        
                    return
            elif event.type == MOUSEBUTTONDOWN:
                if pygame.sprite.spritecollideany(self.pointer_, self.icons):
                    self.quit = True
                    return
                if self.room.collidepoint(mouse_pos):
                    for i in range(len(self.wrong_pos)):
                        if self.wrong_pos[i].collidepoint(mouse_pos):
                            pos = self.wrong_pos[i].center
                            self.xs.add(Xs(pos))
                            del self.wrong_pos[i]
                            break

        if not self.wrong_pos:
            center = (constants.screen_mode[0]/2.0, 
                      constants.screen_mode[0]/2.0)
            self.xs.add(Check(pos=center, zoom=2))
            self.finished_ = True

        self.screen.blit(self.background, (0, 0))
        self.xs.draw(self.screen)
        self.check.draw(self.screen)
        self.pointer_.update(mouse_pos)
        self.pointer.draw(self.screen)
        pygame.display.flip()

    def draw_text(self):
        x, y = 0, 0
        for i in self.text:
            x = i[1][0]
            y = i[1][1]
            surfaces = i[0]
            for surface in surfaces:
                pos = (x, y)
                self.screen.blit(surface, pos)
                y = y + surface.get_height()

class Xs(sprite.Sprite):
    def __init__(self, pos = None):
        sprite.Sprite.__init__(self) 
        path = os.path.join(constants.data_folder, "room", "xs.png")
        self.image, self.rect = common.load_image(path)

        if not pos:
            pos = map(lambda x: x/2.0, constants.screen_mode)
        
        self.update(pos)

    def update(self, pos):
        pos = pos[0], pos[1] - self.rect[3] / 2.0
        self.rect.midtop = pos


if __name__ == "__main__":
	pygame.init()

	screen = pygame.display.set_mode(constants.screen_mode, 32)
    room = Room(screen)
    room.run()
