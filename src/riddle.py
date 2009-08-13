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

class Riddle(Activity):
    def __init__(self, screen):
        Activity.__init__(self, screen)

        self.screen = screen
        path = os.path.join(constants.data_folder, "backgrounds",
                            'illustration_031.png')
        self.background, rect = common.load_image(path)

        title = u"Adivina, adivinanza ..."
        instructions = (u"Lee esta adivinanza, luego une los puntos de ",
				        u"cada figura siguiendo el orden de mayor a menor. ",
                        u"Así descubrirás la respuesta.")
		riddle = (u"Te quito la sed, ", u"te quito el calor", u"por mi eres limpio,",
				  u"grato eres también;", u"donde yo no existo", 
				  u"el mundo triste es:", u"adivina quién puede ser.", u"¿Quién soy?")

        font_title = pygame.font.SysFont(constants.font_title[0],
                                         constants.font_title[1])
        font_default = pygame.font.SysFont(constants.font_default[0],
                                           constants.font_default[1])

        tsize = font_title.size(title)
        isize = font_default.size(instructions[0])[1]

        title_pos = (constants.screen_mode[0]/2.0 - tsize[0]/2.0, 0)
        instruction_pos = (10, title_pos[1] + tsize[1])
        riddle_pos = (50, 200)
        title = font_title.render(title, True, (102, 102, 102))
        
        instructions_ = []
        for i in instructions:
            line = font_default.render(i, True, (102, 102, 102))
            instructions_.append(line)

		riddle_ = []
		for i in riddle:
            line = font_default.render(i, True, (102, 102, 102))
			riddle_.append(line)

        self.text = (((title,), title_pos), (instructions_, instruction_pos),
					 (riddle_, riddle_pos))

        self.icons      = pygame.sprite.Group()
        self.icons.add([Icons('stop')])
        self.pointer = Pointer()
        self.sprites = sprite.OrderedUpdates()
        self.sprites.add([self.icons, self.pointer])
        self.lines = []

        points = (
                (649, 158),
                (638, 170),
                (627, 186),
                (582, 199),
                (548, 254),
                (551, 262),
                (534, 296),
                (527, 331),
                (509, 346),
                (508, 386),
                (521, 378),
                (513, 416),
                (496, 442),
                (466, 467),
                (485, 467),
                (447, 494),
                (427, 516),
                (430, 535),
                (447, 552),
                (485, 563),
                (538, 572),
                (583, 571),
                (629, 553),
                (649, 534),
                (647, 511),
                (629, 492),
                (604, 476),
                (571, 467),
                (563, 440),
                (561, 413),
                (579, 429),
                (575, 397),
                (595, 403),
                (581, 357),
                (579, 318),
                (590, 328),
                (585, 305),
                (579, 278),
                (593, 269),
                (602, 237),
            )
        size = (8, 8)
        self.points = []
        for i in points:
            rect = Rect(i, size)
            rect.center = i
            self.points.append(rect)
            
        self.couple = []
        self.line = None

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

    def setup(self):
        self.draw_text()
        self.sprites.draw(self.screen)

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
                if pygame.sprite.spritecollideany(self.pointer, self.icons):
                    self.quit = True
                    return
                for i in range(0, len(self.points)):
                    if self.points[i].collidepoint(mouse_pos):
                        self.couple.append(i)

                        if len(self.couple) == 1:
                            start = self.points[i].center
                            self.line = Line(surface=self.screen, start=start,
                                    end=start, width=3)
                        elif len(self.couple) == 2:
                            are_adjacent = (self.couple[0] - self.couple[1])**2
                            if are_adjacent == 1:
                                if not (self.line in self.lines):
                                    start = self.points[self.couple[0]].center
                                    end = self.points[self.couple[1]].center
                                    self.lines.append(Line(surface=self.screen, 
                                                      start=start, end=end, width=3))

                            self.line = None
                            self.couple = []
            if event.type == MOUSEMOTION:
                if self.line:
                    end = pygame.mouse.get_pos()
                    self.line.update(end=end)

                self.screen.blit(self.background, (0, 0))
#        for i in self.points:
#            pygame.draw.rect(self.screen, (100, 100, 100), i)

        if len(self.lines) == 39:
            self.finished_ = True
            self.sprites.add(Check(zoom=2))
            self.pointer.kill()
            self.sprites.add(self.pointer)

        self.screen.blit(self.background, (0, 0))
        self.draw_text()
        if self.line:
            self.line.update()
        for i in self.lines:
            i.update()
        self.pointer.update(mouse_pos)
        self.sprites.draw(self.screen)
        pygame.display.flip()

    
class Pointer(sprite.Sprite):
    def __init__(self, pos = None):
        sprite.Sprite.__init__(self) 
        path = os.path.join(constants.data_folder, "cursors", 
							"gartoon", "draw-freehand.png")
        self.image, self.rect = common.load_image(path)

        if not pos:
            pos = map(lambda x: x/2.0, constants.screen_mode)
        
        pygame.mouse.set_pos(pos)
        self.update(pos)

    def update(self, pos):
        self.rect.bottomleft = pos

class Line:
    def __init__(self, surface, start=(0, 0), end=(0, 0), color=(0,0,0),
                 width=1):
        self.surface = surface
        self.start = start
        self.end = end
        self.color = color
        self.width = width

        self.update()

        return

    def update(self, start=None, end=None):
        if start:
            self.start = start
        if end:
            self.end = end

        pygame.draw.line(self.surface, self.color, self.start, self.end,
                         self.width)



if __name__ == "__main__":
	pygame.init()

	screen = pygame.display.set_mode(constants.screen_mode, 32)
    riddle = Riddle(screen)
	riddle.run()
 
