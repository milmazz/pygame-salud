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

class bodyPart(Sprite):
    def __init__(self, name, pos=(0,0)):
        Sprite.__init__(self)
        image_name = os.path.join(constants.data_folder, "missing",
                                  name  + ".png")
        self.image, self.rect = common.load_image(image_name)
        self.size_x, self.size_y = self.image.get_size()
        self.rect.move_ip(pos)
        self.orig_x, self.orig_y = pos
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
                'missing', "correct.png")
        self.image, self.rect = common.load_image(self.path_correct)
        self.rect.move_ip(pos)


class Missing(Activity):
    def __init__(self, screen):
        Activity.__init__(self, screen)
        self.background = common.load_image(constants.illustration_001)[0]

    def groupbodyparts(self, pos_bodyparts):
        bodyparts = pygame.sprite.Group()
        for name in pos_bodyparts:
            bodyparts.add([bodyPart(name, pos_bodyparts[name])])
        return bodyparts

    def instruction_text(self):
        font_title = pygame.font.SysFont("dejavusans", 35)
        font_instructions = pygame.font.SysFont("dejavusans", 20)
        title = u"¿Qué le falta a Kiko en cada figura?"
        instructions = [u"A Kiko le desaparecieron algunas partes de"\
                u" su cuerpo.", u"¿Puedes unirlas?"]
        text = font_title.render(title, True, (102, 102, 102))
        text_pos = (290, 25)
        self.screen.blit(text, text_pos)
        y = 45
        line_width, line_height = font_instructions.size(instructions[0])
        for line in instructions:
            text = font_instructions.render(line, True, (102, 102, 102))
            y += line_height
            text_pos = (300, y)
            self.screen.blit(text, text_pos)

    def setup(self):
        self.sprites  = pygame.sprite.OrderedUpdates()
        self.pos_bodyparts = {'legs': (325, 150), 'arms': (350, 220), \
                'chest': (380, 270), 'head': (380, 320)}
        # list of all bodyparts and positions on the screen
        self.correctbodyparts = ['legs', 'arms', 'chest', 'head']
        self.hand = Hand() #load hand
        self.icons = pygame.sprite.Group()
        self.icons.add([Icons('stop')])
        self.correct = pygame.sprite.Group()
        self.bodyparts = self.groupbodyparts(self.pos_bodyparts)
        self.containers = [pygame.Rect(46, 239, 316, 104), \
                pygame.Rect(459, 194, 237, 71), pygame.Rect(152, 429, \
                97, 82), pygame.Rect(489, 369, 115, 74)]
        self.sprites = pygame.sprite.OrderedUpdates()
        self.sprites.add([self.icons, self.bodyparts, self.hand])
        pygame.mouse.set_visible( False ) #hide pointer
        self.button_down = 0
        self.screen.blit(self.background, (0,0))
        self.sprites.draw(self.screen)
        self.instruction_text()
        pygame.display.update()

    def handle_events(self):
        pygame.event.clear()
        while True:
            for event in [ pygame.event.wait() ] + pygame.event.get():
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
                    selection.update(pos)
                if event.type == MOUSEBUTTONDOWN:
                    if pygame.sprite.spritecollideany(self.hand, self.icons):
                        self.quit = True
                        return
                    self.hand.change_hand()
                    self.hand.update()
                if event.type == MOUSEBUTTONUP:
                    self.hand.change_hand()
                    self.hand.update()
                if event.type == MOUSEBUTTONUP and selection:
                    self.button_down = 0
                    bodypart_in_container = \
                            selection.rect.collidelistall(self.containers)
                    if bodypart_in_container:
                        if selection.name == \
                                self.correctbodyparts[bodypart_in_container[0]]:
                                    left, top, width, height = self.containers[bodypart_in_container[0]]
                                    selection.rect = \
                                            pygame.Rect(left + (width - \
                                            selection.size_x)/2, top + (height - \
                                            selection.size_y)/2, 0, 0)
                                    self.correct.add([correct((left + ((width
                                        - 76) / 2), top))])
                                    self.sprites.remove([self.hand])
                                    self.sprites.add([self.correct, self.hand])
                        else:
                            selection.change_size()
                            selection.update((selection.orig_x, selection.orig_y))
                    else:
                        selection.change_size()
                        selection.update((selection.orig_x, selection.orig_y))
                        selection.color = 0
                if event.type == MOUSEBUTTONDOWN:
                    selection = pygame.sprite.spritecollideany(self.hand, \
                            self.bodyparts)
                    if selection:
                        self.button_down = 1
                        selection.change_size()
                        selection.remove(self.sprites)
                        selection.add(self.sprites)
                self.hand.remove(self.sprites)
                self.hand.add(self.sprites)
                self.screen.blit(self.background, (0,0))
                self.instruction_text()
                self.sprites.draw(self.screen)
                pygame.display.update()
