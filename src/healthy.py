# vim:ts=4:sts=4:et:nowrap:tw=77
# -*- coding: utf-8 -*-

import os
import sys
import pygame
from pygame.sprite import Sprite
from pygame.locals import *

import constants
from activity import Activity
import common
from icons import Icons

class textLine(Sprite):
    def __init__(self, textline, pos=(0,0)):
        Sprite.__init__(self)
        image_name = os.path.join(constants.data_folder, "healthy",
                                  textline  + ".png")
        self.image, self.rect = common.load_image(image_name)
        self.size_x, self.size_y = self.image.get_size()
        self.rect.move_ip(pos)
        self.name = textline
		
    def update(self, pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]


class Hand(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image_normal = os.path.join(constants.data_folder, 'cursors',
                                    "hand-open.png")
        self.image_close = os.path.join(constants.data_folder, 'cursors', 
                                    "hand-close.png")
        self.normal, self.rect = common.load_image(self.image_normal)
        self.close, self.rect = common.load_image(self.image_close)
        self.image = self.normal
        self.color = 0

    def change_hand(self):
        if self.color == 0:
            self.color = 1
        else:
            self.color = 0

    def update(self, mover=(0,0)):
        if mover[0] - 10 >= 0:
            self.rect.x = mover[0]
        if mover[1] - 15 >= 0:
            self.rect.y = mover[1]
        if self.color == 0:
            self.image = self.normal
        if self.color == 1:
            self.image = self.close


class correct(Sprite):
    def __init__(self, pos=(0,0)):
        Sprite.__init__(self)
        self.path_correct = os.path.join(constants.data_folder, \
                'healthy', "correct.png")
        self.image, self.rect = common.load_image(self.path_correct)
        self.rect.move_ip(pos)


class changeButtons(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.path_next = os.path.join(constants.data_folder, 'healthy',
                                    "next.png")
        self.path_prev = os.path.join(constants.data_folder, 'healthy', 
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


class View():
    def __init__(self):
        self.back1 = common.load_image(constants.illustration_005)[0]
        self.back2 = common.load_image(constants.illustration_006)[0]
        self.background = self.back1

    def update(self):
        if self.background == self.back1:
            self.background = self.back2
        else:
            self.background = self.back1

    def grouptextlines(self, pos_textlines):
        textlines = pygame.sprite.Group()
        for name in pos_textlines:
            textlines.add([textLine(name, pos_textlines[name])])
        return textlines


class Healthy(Activity):
    def __init__(self, screen):
        Activity.__init__(self, screen)
        self.selection = None

    def instruction_text(self):
        font_title = pygame.font.SysFont("dejavusans", 40)
        font_instructions = pygame.font.SysFont("dejavusans", 20)
        title = u"Para estar sano debo..."
        title_width, title_height = font_title.size(title)
        instructions = [u"Todas estas actividades sirven para que"\
                u"tengas buena salud.", u"¿Qué hace cada niño?"\
                u"Arrastra la palabra que falta debajo del dibujo"]
        y = title_height / 2
        text = font_title.render(title, True, (102, 102, 102))
        text_pos = (constants.screen_mode[0]/2.0 - title_width/2.0, y)
        self.screen.blit(text, text_pos)
        y += title_height
        line_width, line_height = font_instructions.size(instructions[0])
        for line in instructions:
            text = font_instructions.render(line, True, (102, 102, 102))
            y += line_height
            text_pos = (50, y)
            self.screen.blit(text, text_pos)

    def setup(self):
        self.sprites  = pygame.sprite.OrderedUpdates()
        self.pos_textlines1 = {'study': (50, 90), 'eat': (50, 140), \
                'sport': (50, 115)}
        self.pos_textlines2 = {'brush': (50,90), 'wash': (50, 115), \
                'shower': (50,140)}
        self.pos_textlines = self.pos_textlines1
        # list of all textlines and positions on the screen
        self.correctlines1 = ['study', 'eat', 'sport']
        self.correctlines2 = ['brush', 'wash', 'shower']
        self.correctlines = self.correctlines1
        self.view = View() #load static background
        self.hand = Hand() #load hand
        self.change = pygame.sprite.Group()
        self.change.add([changeButtons()]) #load next and prev buttons
        self.icons = pygame.sprite.Group()
        self.icons.add([Icons('stop')])
        self.correct = pygame.sprite.Group()
        self.textlines = self.view.grouptextlines(self.pos_textlines1)
        self.containers1 = [pygame.Rect(70, 555, 250, 40), \
                pygame.Rect(240, 285, 250, 40), pygame.Rect(510, 515, 250, 40)]
        self.containers2 = [pygame.Rect(50, 495, 250, 40), \
                pygame.Rect(285, 280, 250, 40), pygame.Rect(500, 535, 250, 40)]
        self.containers = self.containers1
        self.sprites = pygame.sprite.OrderedUpdates()
        self.sprites.add([self.icons, self.textlines, self.change, self.hand])
        pygame.mouse.set_visible( False ) #hide pointer
        self.button_down = 0
        self.screen.blit(self.view.background, (0,0))
        self.sprites.draw(self.screen)
        self.instruction_text()
        pygame.display.update()

    def handle_events(self):
        for event in self.get_event():
            pos = pygame.mouse.get_pos()
            if event.type == QUIT:
                self.quit = True
                return
            elif event.type == KEYUP:
                self.changed = False
                if event.key == K_ESCAPE:
                    self.quit = True
                    return
            if event.type == MOUSEMOTION:
                self.hand.update(pos)
            if event.type == MOUSEMOTION and self.button_down:
                self.selection.update(pos)
            if event.type == MOUSEBUTTONDOWN:
                if pygame.sprite.spritecollideany(self.hand, self.icons):
                    self.quit = True
                    return
                if pygame.sprite.spritecollideany(self.hand, self.change):
                    self.view.update()
                    self.change.update()
                    if self.correctlines == self.correctlines1:
                        self.pos_textlines = self.pos_textlines2
                        self.correctlines = self.correctlines2
                        self.containers = self.containers2
                    else:
                        self.pos_textlines = self.pos_textlines1
                        self.correctlines = self.correctlines1
                        self.containers = self.containers1
                    self.sprites.remove([self.textlines, self.correct, \
                            self.hand])
                    self.correct.empty()
                    self.textlines = self.view.grouptextlines(self.pos_textlines)
                    self.sprites.add([self.textlines, self.hand])
                self.hand.change_hand()
                self.hand.update()
            if event.type == MOUSEBUTTONUP:
                self.hand.change_hand()
                self.hand.update()
            if event.type == MOUSEBUTTONUP and self.selection:
                self.button_down = 0
                textline_in_container = \
                        self.selection.rect.collidelistall(self.containers)
                if textline_in_container:
                    if self.selection.name == \
                            self.correctlines[textline_in_container[0]]:
                                left, top, width, height = self.containers[textline_in_container[0]]
                                self.selection.rect = \
                                pygame.Rect(left + (width - \
                                self.selection.size_x)/2, top + (height - \
                                self.selection.size_y)/2, 0, 0)
                                self.correct.add([correct((left + (width \
                                        /2) - 25, top - 150))])
                                self.sprites.remove([self.hand])
                                self.sprites.add([self.correct, self.hand])
                    else:
                        pass
                else:
                    self.selection.color = 0
                    self.selection.update(pos)
            if event.type == MOUSEBUTTONDOWN:
                self.selection = pygame.sprite.spritecollideany(self.hand, \
                        self.textlines)
                if self.selection:
                    self.selection.color = 1
                    self.button_down = 1
            self.screen.blit(self.view.background, (0,0))
            self.instruction_text()
            self.sprites.draw(self.screen)
            pygame.display.update()
