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

class bodyPart(Sprite):
    def __init__(self, name, pos=(0,0)):
        Sprite.__init__(self)
        image_name = os.path.join(constants.data_folder, "missing",
                                  name  + ".png")
        self.image, self.rect = common.load_image(image_name)
        self.size_x, self.size_y = self.image.get_size()
        self.rect.move_ip(pos)
        self.orig = pos
        self.name = name
        self.image_small = pygame.transform.scale(self.image,
                (self.size_x/2, self.size_y/2))
        self.image_orig = self.image
        self.image = self.image_small
        self.small = 1

    def change_size(self):
        if self.small == 1:
            self.image = self.image_orig
            self.small = 0
        else:
	        self.image = self.image_small
            self.small = 1
	
    def update(self, pos):
        self.rect.topleft = pos


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
        self.rect.topleft = mover
        if self.color == 0:
            self.image = self.normal
        if self.color == 1:
            self.image = self.close


class Missing(Activity):
    def __init__(self, screen):
        Activity.__init__(self, screen)
        self.background = common.load_image(constants.illustration_001)[0]
        self.instruction_text()

    def groupbodyparts(self, pos_bodyparts):
        bodyparts = pygame.sprite.Group()
        for name in pos_bodyparts:
            bodyparts.add([bodyPart(name, pos_bodyparts[name])])
        return bodyparts

    def instruction_text(self):
        font_title = pygame.font.SysFont(constants.font_title[0], constants.font_title[1])
        font_instructions = pygame.font.SysFont(constants.font_default[0], constants.font_default[1])
        title = u"¿Qué le falta a Kiko en cada figura?"
        instructions = [u"A Kiko le desaparecieron algunas partes de su cuerpo", 
                u"¿Puedes unirlas arrastrando las partes?"]
        text = font_title.render(title, True, constants.font_title_color)
        text_pos = (142, 35)
        self.background.blit(text, text_pos)

        y = 45
        line_width, line_height = font_instructions.size(instructions[0])
        for line in instructions:
            text = font_instructions.render(line, True, constants.font_default_color)
            y += line_height
            text_pos = (154, y)
            self.background.blit(text, text_pos)

    def setup(self):
        self.cont = None
        self.selection = None
        self.sprites  = pygame.sprite.OrderedUpdates()
        self.pos_bodyparts = {'legs': (367, 200), 'arms': (380, 270), \
                'chest': (400, 320), 'head': (396, 370)}
        # list of all bodyparts and positions on the screen
        self.correctbodyparts = ['legs', 'arms', 'chest', 'head']
        self.correct = [0, 0, 0, 0]
        self.hand = Hand() #load hand
        self.icons = pygame.sprite.Group()
        self.icons.add([Icons('stop')])
        self.checked = pygame.sprite.Group()
        self.bodyparts = self.groupbodyparts(self.pos_bodyparts)
        self.containers = [pygame.Rect(145, 257, 185, 103), \
                pygame.Rect(557, 182, 145, 79), pygame.Rect(195, 431, \
                58, 77), pygame.Rect(575, 349, 73, 81)]
        self.sprites = pygame.sprite.OrderedUpdates()
        self.sprites.add([self.icons, self.bodyparts, self.hand])
        pygame.mouse.set_visible( False ) #hide pointer
        self.button_down = 0
        pos = pygame.mouse.get_pos()
        self.hand.update(pos)
        self.sprites.draw(self.screen)
        pygame.event.clear()

    def handle_events(self):
        for event in self.get_event():
            pos = pygame.mouse.get_pos()
            if event.type == QUIT:
                self.quit = True
                return
            elif event.type == KEYUP:
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
                self.hand.change_hand()
                self.hand.update(pos)
            if event.type == MOUSEBUTTONUP:
                self.hand.change_hand()
                self.hand.update(pos)
            if event.type == MOUSEBUTTONUP and self.selection:
                self.button_down = 0
                bodypart_in_container = \
                        self.selection.rect.collidelistall(self.containers)
                if bodypart_in_container:
                    if self.selection.name == \
                            self.correctbodyparts[bodypart_in_container[0]]:
                                self.selection.kill()
                                self.selection.add(self.sprites)
                                self.selection.rect = \
                                        pygame.Rect((self.containers[bodypart_in_container[0]][0], \
                                        self.containers[bodypart_in_container[0]][1]), \
                                        (0, 0))
                                self.correct[bodypart_in_container[0]] = 1
                                self.checked.add([Check(self.containers[bodypart_in_container[0]].center)])
                                self.sprites.add([self.checked])
                    else:
                        self.selection.change_size()
                        self.selection.update((self.selection.orig))
                else:
                    self.selection.change_size()
                    self.selection.update((self.selection.orig))
                    self.selection.color = 0
            if event.type == MOUSEBUTTONDOWN:
                self.selection = pygame.sprite.spritecollideany(self.hand, \
                        self.bodyparts)
                if self.selection:
                    self.button_down = 1
                    self.selection.change_size()
                    self.selection.remove(self.sprites)
                    self.selection.add(self.sprites)
            if self.cont != 4:
                self.cont = 0
            if self.cont == 0:
                for i in range(0,4):
                    if self.correct[i] == 1:
                        self.cont = self.cont + 1
            if self.cont == 4:
                self.finished_ = True
            self.hand.remove(self.sprites)
            self.hand.add(self.sprites)
            self.screen.blit(self.background, (0,0))
            self.sprites.draw(self.screen)
            pygame.display.update()
