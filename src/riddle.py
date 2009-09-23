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

class RiddleBase(Activity):
    def __init__(self, screen):
        Activity.__init__(self, screen)

        self.screen = screen

        self.title = ("¿Qué será, qué será?",)
        self.instructions = ("Lee esta adivinanza, luego une los puntos de",
                        "cada figura siguiendo el orden de mayor a menor.",
                        "Así descubrirás la respuesta.")
		self.riddle = ("Agua pasó por aquí,", 
                        "¡cate! Que yo la ví.",)


        self.icons      = pygame.sprite.Group()
        self.icons.add([Icons('stop')])
        self.pointer = Pointer()
        self.sprites = sprite.OrderedUpdates()
        self.sprites.add([self.icons, self.pointer])
        self.lines = []

        self.points_reference = (
                (655, 225), #1
                (634, 303), #2
                (654, 378), #3
                (642, 460), #4
                (583, 533), #5
                (518, 554), #6
                (452, 551), #7
                (531, 482), #8
                (575, 420), #9
                (592, 354), #10
                (597, 292), #11
                (620, 196), #12
                (576, 211), #13
                (543, 251), #14
                (507, 300), #15
                (462, 345), #16
                (438, 401), #17
                (428, 467), #18
                (441, 542), #19
                (377, 475), #20
                (371, 412), #21
                (387, 356), #22
                (441, 303), #23
                (489, 264), #24
                (523, 215), #25
                (577, 184), #26
                (621, 184), #27
                (636, 152), #28
                (655, 124), #29
                (669, 133), #30
                (651, 158), #31
                (630, 183), #32
            )
        self.size = (8, 8)
        self.points = []
        self.couple = []
        self.line = None
        self.exist = None
        self.pos = None
        self.total_lines = 31

    def info_text(self, messages, pos, size=constants.font_default[1], bg=None):
        font = pygame.font.SysFont(constants.font_default[0], size)
        font_height = font.get_linesize()

        for message in messages:
            message = unicode(message, 'utf-8')
            text = font.render(message, True, constants.font_default_color)
            text_pos = pos
            bg.blit(text, text_pos)
            pos[1] += font_height
 
    def informative_text(self, title, instructions, riddle):
        font_title = pygame.font.SysFont(constants.font_title[0],
                                         constants.font_title[1])

        tsize = font_title.size(title[0])

        title_pos = [(constants.screen_mode[0] - tsize[0]) / 2.0, 0]
       
        tsize = font_title.get_linesize()
        instructions_pos = [10, title_pos[1] + 1.5 * tsize]

        self.info_text(title, title_pos, size=constants.font_title[1], bg=self.background)
        self.info_text(instructions, instructions_pos, bg=self.background)
        self.info_text(riddle, [50, 200], bg=self.background)

    def setup_background(self):
        self.background, rect = common.load_image(constants.illustration_029a)
 
    def setup(self):
        self.lastcouple = False
        for i in self.points_reference:
            rect = Rect(i, self.size)
            rect.center = i
            self.points.append(rect)
        self.informative_text(self.title, self.instructions, self.riddle)
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
                if self.icons.sprites()[0].rect.collidepoint(mouse_pos):
                    self.quit = True
                    return
                for pos in range(0, len(self.points)):
                    if self.points[pos].collidepoint(mouse_pos):
                        self.pos = pos
                if self.pos != None:
                    self.couple.append(self.pos)
                    if len(self.couple) == 1:
                        start = self.points[self.pos].center
                        self.line = Line(surface=self.screen, \
                                start=start, end=start, width=3)
                    elif len(self.couple) == 2:
                        are_adjacent = (self.couple[0] - self.couple[1])**2
                        if are_adjacent == 1:
                            start = self.points[self.couple[0]].center
                            end = self.points[self.couple[1]].center
                            self.line = Line(surface=self.screen, \
                                    start=start, end=end, width=3)
                            if len(self.lines) == 0:
                                self.lines.append(self.line)
                                self.couple[0] = self.couple[1]
                                self.couple.pop()
                                start = self.points[self.couple[0]].center
                                self.line = Line(surface=self.screen, \
                                        start=start, end=start, width=3)
                            else:
                                for i in range(0,len(self.lines)):
                                    if (((self.line.end == self.lines[i].end) and
                                        (self.line.start == self.lines[i].start)) or
                                        ((self.line.end == self.lines[i].start) and
                                        (self.line.start == self.lines[i].end))):
                                            self.exist = True
                                    else:
                                        self.exist = False
                                if not self.exist:
                                    self.lines.append(self.line)
                                    self.couple[0] = self.couple[1]
                                    self.couple.pop()
                                    start = self.points[self.couple[0]].center
                                    self.line = Line(surface=self.screen, \
                                            start=start, end=start, width=3)
                                else:
                                    self.couple = []
                                    self.line = None
                        else:
                            self.couple = []
                            self.line = None
            if event.type == MOUSEMOTION:
                if self.line:
                    end = pygame.mouse.get_pos()
                    self.line.update(end=end)

                self.screen.blit(self.background, (0, 0))

        if len(self.lines) == self.total_lines:
            self.finished_ = True
            self.line = None
            self.sprites.add(Check(zoom=2))
            self.pointer.kill()
            self.sprites.add(self.pointer)

        self.screen.blit(self.background, (0, 0))
        if self.line:
            self.line.update()
        for i in self.lines:
            i.update()
        self.pointer.update(mouse_pos)
        self.sprites.draw(self.screen)
        pygame.display.flip()

# Activity 24-1
class Riddle1(RiddleBase):
    def __init__(self, screen):
        RiddleBase.__init__(self, screen)

# Activity 24-2
class Riddle2(RiddleBase):
    def __init__(self, screen):
        RiddleBase.__init__(self, screen)
        self.points_reference = (
                (439, 103), #1
                (465, 185), #2
                (488, 268), #3
                (506, 311), #4
                (545, 323), #5
                (589, 327), #6
                (633, 342), #7
                (671, 383), #8
                (689, 415), #9
                (690, 452), #10
                (675, 488), #11
                (647, 516), #12
                (609, 527), #13
                (573, 546), #14
                (531, 561), #15
                (495, 557), #16
                (455, 540), #17
                (428, 515), #18
                (412, 477), #19
                (417, 430), #20
                (437, 389), #21
                (470, 351), #22
                (467, 304), #23
                (458, 251), #24
                (434, 199), #25
                (407, 151), #26
                (372, 88), #27
                (409, 133), #28
                (452, 199), #29
                (427, 141), #30
            )
        self.total_lines = 29
        self.instructions = ("Lee esta adivinanza, luego une los puntos de",
                        "cada figura siguiendo el orden",
                        "de mayor a menor.",
                        "Así descubrirás la respuesta.")
		self.riddle = ("Una hoja entre muchas",
                  "hojas, buscando una hoja",
                  "se llora.")

    def setup_background(self):
        self.background, rect = common.load_image(constants.illustration_029b)

# Activity 24-3
class Riddle3(RiddleBase):
    def __init__(self, screen):
        RiddleBase.__init__(self, screen)
        self.points_reference = (
                (302, 432), #1
                (318, 390), #2
                (346, 342), #3
                (380, 286), #4
                (405, 259), #5
                (439, 245), #6
                (474, 203), #7
                (516, 168), #8
                (569, 133), #9
                (631, 105), #10
                (672, 115), #11
                (688, 143), #12
                (646, 190), #13
                (599, 235), #14
                (578, 269), #15
                (560, 304), #16
                (535, 349), #17
                (512, 388), #18
                (504, 426), #19
                (475, 483), #20
                (448, 539), #21
                (418, 561), #22
                (402, 510), #23
                (371, 466), #24
                (316, 448), #25
                (293, 449), #26
                (307, 483), #27
                (332, 513), #28
                (365, 547), #29
                (402, 562), #30
            )
        self.total_lines = 29
		self.riddle = ("El que sabe, sabe",
                  "¿Con qué se hace el casabe?",)

    def setup_background(self):
        self.background, rect = common.load_image(constants.illustration_030a)

# Activity 24-4
class Riddle4(RiddleBase):
    def __init__(self, screen):
        RiddleBase.__init__(self, screen)
        self.points_reference = (
                (697, 261), #1
                (690, 348), #2
                (682, 432), #3
                (674, 499), #4
                (560, 516), #5
                (441, 522), #6
                (330, 507), #7
                (315, 490), #8
                (305, 457), #9
                (305, 395), #10
                (328, 328), #11
                (389, 300), #12
                (478, 282), #13
                (570, 272), #14
                (682, 258), #15
                (612, 224), #16
                (532, 200), #17
                (463, 193), #18
                (384, 198), #19
                (340, 215), #20
                (302, 292), #21
                (287, 386), #22
            )
        self.total_lines = 21
		self.riddle = ("Que sólo será",
                  "que no lo será,",
                  "si no lo adivinas",
                  "el ratón se lo comerá.",)

    def setup_background(self):
        self.background, rect = common.load_image(constants.illustration_030b)

# Activity 25
class Riddle5(RiddleBase):
    def __init__(self, screen):
        RiddleBase.__init__(self, screen)
        self.points_reference = (
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
        self.total_lines = 39
        self.title = ("Adivina, adivinanza...",)
		self.riddle = ("Te quito la sed,",
                    "te quito el calor",
                    "por mi eres limpio,",
                    "grato eres también;",
                    "donde yo no existo",
                    "el mundo triste es:",
                    "adivina quién puede ser.",
                    "¿Quién soy?")

    def setup_background(self):
        self.background, rect = common.load_image(constants.illustration_031a)

class Riddle6(RiddleBase):
    def __init__(self, screen):
        RiddleBase.__init__(self, screen)
        self.points_reference = (
                (431, 207), #1
                (399, 201), #2
                (347, 217), #3
                (304, 249), #4
                (275, 299), #5
                (265, 358), #6
                (270, 415), #7
                (298, 465), #8
                (363, 489), #9
                (400, 522), #10
                (438, 534), #11
                (466, 527), #12
                (505, 538), #13
                (541, 521), #14
                (589, 508), #15
                (624, 497), #16
                (656, 462), #17
                (677, 426), #18
                (684, 392), #19
                (686, 351), #20
                (682, 312), #21
                (669, 273), #22
                (646, 234), #23
                (609, 206), #24
                (574, 192), #25
                (522, 192), #26
                (483, 205), #27
                (499, 220), #28
                (485, 239), #29
                (456, 244), #30
            )
        self.total_lines = 29
        self.title = ("Adivina, adivinanza...",)
		self.riddle = ("Te quito la sed, ",
                    "te quito el calor",
                    "por mi eres limpio,",
                    "grato eres también;",
                    "donde yo no existo", 
                    "el mundo triste es:",
                    "adivina quién puede ser.",
                    "¿Quién soy?")

    def setup_background(self):
        self.background, rect = common.load_image(illustration_031b)

class Pointer(sprite.Sprite):
    def __init__(self, pos = None):
        sprite.Sprite.__init__(self) 
        self.image, self.rect = common.load_image(constants.draw_freehand)

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
