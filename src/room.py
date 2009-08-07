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
from icons import Icons


class Room(Activity):
    def __init__(self, screen):
        Activity.__init__(self, screen)
        self.wrong_pos = (
                (446, 322, 481, 330),
                (493, 273, 507, 293),
                (523, 278, 574, 308),
                )
        self.screen = screen
        path = os.path.join(constants.data_folder, "room", 'room.png')
        self.background, rect = common.load_image(path)

        title = u"¡Orden en mi habitación!"
        instructions = (u"Observa estas dos habitaciones. Una está ordenada " +
                u"y la otra desordenada:", u"descubre las diferencias y " + 
                u"márcalas con una X en la habitación desordenada")

        font_title = pygame.font.SysFont(constants.font_title[0],
                                         constants.font_title[1])
        font_default = pygame.font.SysFont(constants.font_default[0],
                                           constants.font_default[1])

        tsize = font_title.size(title)
        isize = font_default.size(instructions[0])[1]

        title_pos = (constants.screen_mode[0]/2.0 - tsize[0]/2.0, 0)
        instruction_pos = (10, title_pos[1] + tsize[1])
        title = font_title.render(title, True, (102, 102, 102))
        
        instructions_ = []
        for i in instructions:
            line = font_default.render(i, True, (102, 102, 102))
            instructions_.append(line)
        self.text = (((title,), title_pos), (instructions_, instruction_pos))

        self.pointer_ = Xs()
        self.pointer = sprite.RenderUpdates(self.pointer_)
        self.xs = sprite.RenderUpdates()

        self.xs.draw(self.screen)
        self.pointer.draw(self.screen)
        pygame.display.update()

    def setup(self):
        self.draw_text()

    def handle_events(self):
        pygame.event.clear()

        for event in [pygame.event.wait()] + pygame.event.get():
            mouse_pos = pygame.mouse.get_pos()
            if event.type == QUIT:
                self.quit = True
                return
            elif event.type == KEYUP:
                self.changed = True
                if event.key == K_ESCAPE:
                    self.quit = True                        
                    return
            elif event.type == MOUSEBUTTONDOWN:
                self.xs.add(Xs(mouse_pos))

        self.screen.blit(self.background, (0, 0))
        self.draw_text()
        self.xs.draw(self.screen)
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
        
        pygame.mouse.set_pos(pos)
        self.update(pos)

    def update(self, pos):
        pos = pos[0], pos[1] - self.rect[3] / 2.0
        self.rect.midtop = pos


if __name__ == "__main__":
	pygame.init()

	screen = pygame.display.set_mode(constants.screen_mode, 32)
    room = Room(screen)
    room.run()
