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
        wrong_pos = (
                (498, 277, 509, 298),
                (522, 282, 577, 318),
                (587, 292, 605, 310),
                (605, 322, 618, 356),
                (445, 318, 480, 330),
                (443, 362, 462, 377),
                (468, 374, 490, 420),
                (510, 372, 584, 400),
#                (633, 368, 631, 412),
                (521, 426, 576, 474),
                (513, 475, 539, 505),
                (470, 506, 498, 526),
#                (548, 518, 563, 542),
                (642, 448, 680, 477),
                (740, 329, 765, 360),
                (660, 199, 675, 217),
                (726, 181, 736, 193),
                (733, 211, 742, 223),
#                (590, 288, 602, 307),
                (630, 368, 636, 419),
                (540, 518, 569, 542),
                )
        self.wrong_pos = []
        for i in wrong_pos:
            rect = (i[0], i[1], i[2] - i[0], i[3] - i[1])
            self.wrong_pos.append(Rect(rect))

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

    def setup(self):
        self.draw_text()
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
                    self.xs.add(Xs(mouse_pos))
                    for i in range(len(self.wrong_pos)):
                        if self.wrong_pos[i].collidepoint(mouse_pos):
                            self.check.add(Check(mouse_pos))
                            del(self.wrong_pos[i])
                            break

        if not self.wrong_pos:
            self.finished_ = True

        self.screen.blit(self.background, (0, 0))
        self.draw_text()
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
        
        pygame.mouse.set_pos(pos)
        self.update(pos)

    def update(self, pos):
        pos = pos[0], pos[1] - self.rect[3] / 2.0
        self.rect.midtop = pos


class Check(Xs):
    def __init__(self, pos = None):
        sprite.Sprite.__init__(self) 
        path = os.path.join(constants.data_folder, "room", "check.png")
        self.image, self.rect = common.load_image(path)
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()

        if not pos:
            pos = map(lambda x: x/2.0, constants.screen_mode)
        
        pygame.mouse.set_pos(pos)
        self.update(pos)

if __name__ == "__main__":
	pygame.init()

	screen = pygame.display.set_mode(constants.screen_mode, 32)
    room = Room(screen)
    room.run()
