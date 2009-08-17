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
from icons import *

class textLine(Sprite):
    def __init__(self, textline, pos=(0,0)):
        Sprite.__init__(self)
        image_name = os.path.join(constants.data_folder, "healthy",
                                  textline  + ".png")
        self.image, self.rect = common.load_image(image_name)
        self.rect.center = pos
        self.orig = pos
        self.name = textline
		
    def update(self, pos):
        self.rect.centerx, self.rect.centery = pos


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
        self.rect.x, self.rect.y = mover
        if self.color == 0:
            self.image = self.normal
        if self.color == 1:
            self.image = self.close


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


class Healthy(Activity):
    def __init__(self, screen):
        Activity.__init__(self, screen)
        self.back1 = common.load_image(constants.illustration_005)[0]
        self.back2 = common.load_image(constants.illustration_006)[0]
        self.background = self.back1

    def update_background(self):
        if self.background == self.back1:
            self.background = self.back2
        else:
            self.background = self.back1

    def instruction_text(self):
        font_title = pygame.font.SysFont("dejavusans", 40)
        font_instructions = pygame.font.SysFont("dejavusans", 20)
        title = u"Para estar sano debo..."
        title_width, title_height = font_title.size(title)
        instructions = [u"Todas estas actividades sirven para que"\
                u" tengas buena salud.", u" ¿Qué hace cada niño?"\
                u" Arrastra la palabra que falta debajo del dibujo."]
        y = title_height / 2
        text = font_title.render(title, True, (102, 102, 102))
        text_pos = (constants.screen_mode[0]/2.0 - title_width/2.0, y)
        self.background.blit(text, text_pos)
        y += title_height
        line_width, line_height = font_instructions.size(instructions[0])
        for line in instructions:
            text = font_instructions.render(line, True, (102, 102, 102))
            y += line_height
            text_pos = (50, y)
            self.background.blit(text, text_pos)

    def setup(self):
        self.cont = None
        self.selection = None
        self.sprites  = pygame.sprite.OrderedUpdates()
        self.pos_textlines1 = {'study': (50, 190), 'eat': (50, 150), \
                'sports': (50, 230)}
        self.pos_textlines2 = {'teeth': (150,155), 'hands': (250, 160), \
                'body': (50,160)}
        self.pos_textlines = self.pos_textlines1
        # list of all textlines and positions on the screen
        self.correctlines1 = ['study', 'eat', 'sports']
        self.correctlines2 = ['teeth', 'hands', 'body']
        self.correct1 = [0, 0, 0]
        self.correct2 = [0, 0, 0]
        self.correct = self.correct1
        self.correctlines = self.correctlines1
        self.hand = Hand() #load hand
        self.change = pygame.sprite.Group()
        self.change.add([changeButtons()]) #load next and prev buttons
        self.icons = pygame.sprite.Group()
        self.icons.add([Icons('stop')])
        self.checked = pygame.sprite.Group()
        self.textlines = pygame.sprite.Group()
        for name in self.pos_textlines:
            self.textlines.add([textLine(name, self.pos_textlines[name])])
        self.containers1 = [pygame.Rect(115, 562, 95, 25), \
                pygame.Rect(371, 457, 78, 25), pygame.Rect(675, 525, 101, 25)]
        self.containers2 = [pygame.Rect(181, 503, 84, 25), \
                pygame.Rect(448, 464, 73, 25), pygame.Rect(697, 550, 79, 25)]
        self.containers = self.containers1
        self.sprites = pygame.sprite.OrderedUpdates()
        self.sprites.add([self.icons, self.textlines, self.change, self.hand])
        pygame.mouse.set_visible( False ) #hide pointer
        self.button_down = 0
        pos = pygame.mouse.get_pos()
        self.hand.update(pos)
        self.instruction_text()
        self.screen.blit(self.background, (0,0))
        self.sprites.draw(self.screen)
        pygame.display.update()
        pygame.event.clear()

    def handle_events(self):
        for event in self.get_event():
            pos = pygame.mouse.get_pos()
            self.hand.update(pos)
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
                    self.sprites.empty()
                    self.sprites.add([self.icons, self.change])
                    self.update_background()
                    self.instruction_text()
                    self.change.update()
                    self.checked.empty()
                    self.textlines.empty()
                    if self.correctlines == self.correctlines1:
                        self.pos_textlines = self.pos_textlines2
                        self.correctlines = self.correctlines2
                        self.containers = self.containers2
                        self.correct = self.correct2
                    else:
                        self.pos_textlines = self.pos_textlines1
                        self.correctlines = self.correctlines1
                        self.containers = self.containers1
                        self.correct = self.correct1
                    for i in range(0,3):
                        if self.correct[i] == 1:
                            self.auxtextline = textLine(self.correctlines[i], \
                                    self.containers[i].center)
                            self.checked.add([Check((self.containers[i].centerx, \
                                    self.containers[i].centery - 75))])
                            self.textlines.add([self.auxtextline])
                        if self.correct[i] == 0:
                            self.textlines.add([textLine(self.correctlines[i], \
                                    self.pos_textlines[self.correctlines[i]])])
                    self.sprites.add([self.textlines, self.checked])
                self.hand.change_hand()
                self.hand.update(pos)
            if event.type == MOUSEBUTTONUP:
                self.hand.change_hand()
                self.hand.update(pos)
            if event.type == MOUSEBUTTONUP and self.selection:
                self.button_down = 0
                textline_in_container = \
                        self.selection.rect.collidelistall(self.containers)
                if textline_in_container:
                    if self.selection.name == \
                            self.correctlines[textline_in_container[0]]:
                                self.selection.kill()
                                self.selection.add(self.sprites)
                                self.selection.rect = \
                                        pygame.Rect((self.containers[textline_in_container[0]][0], \
                                        self.containers[textline_in_container[0]][1]), \
                                        (0, 0))
                                self.correct[textline_in_container[0]] = 1
                                self.checked.add([Check((self.containers[textline_in_container[0]].centerx, \
                                        self.containers[textline_in_container[0]].centery - 75))])

                                self.sprites.add([self.checked])
                    else:
                        self.selection.update((self.selection.orig))
                else:
                    self.selection.update((self.selection.orig))
                    self.selection.color = 0
            if event.type == MOUSEBUTTONDOWN:
                self.selection = pygame.sprite.spritecollideany(self.hand, \
                        self.textlines)
                if self.selection:
                    self.selection.color = 1
                    self.button_down = 1
                    self.selection.remove(self.sprites)
                    self.selection.add(self.sprites)
            if self.cont != 6:
                self.cont = 0
            if self.cont == 0:
                for i in range(0,3):
                    if self.correct1[i] == 1:
                        self.cont = self.cont + 1
                    if self.correct2[i] == 1:
                        self.cont = self.cont + 1
            if self.cont == 6:
                self.finished_ = True
            self.hand.remove(self.sprites)
            self.hand.add(self.sprites)
            self.screen.blit(self.background, (0,0))
            self.sprites.draw(self.screen)
            pygame.display.update()
