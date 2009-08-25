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

class Ingredient(Sprite):
    def __init__(self, name, pos=(0,0)):
        Sprite.__init__(self)
        image_name = os.path.join(constants.data_folder, "cooking",
                                  name + ".png")
        self.image, self.rect = common.load_image(image_name)
        self.size_x, self.size_y = self.image.get_size()
        self.rect.move_ip(pos)
        self.orig = pos
        self.name = name
	
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


class Cooking(Activity):
    def __init__(self, screen):
        Activity.__init__(self, screen)
        self.background = common.load_image(constants.illustration_024)[0]
        self.instruction_text()

    def groupingredients(self, pos_ingredients):
        ingredients = pygame.sprite.Group()
        for name in pos_ingredients:
            ingredients.add([Ingredient(name, pos_ingredients[name])])
        return ingredients

    def instruction_text(self):
        font_title = pygame.font.SysFont("dejavusans", 32)
        font_instructions = pygame.font.SysFont("dejavusans", 20)
        title = u"¡A Cocinar!"
        title_width, title_height = font_title.size(title)
        instructions = [u"Vamos a hacer una torta...", \
                u"Observa los ingredientes", \
                u"que se necesitan", \
                u"y arrástralos hasta la mesa."]
        y = 5
        text = font_title.render(title, True, (102, 102, 102))
        text_pos = (constants.screen_mode[0]/2.0 - title_width/2.0, y)
        self.background.blit(text, text_pos)
        y = 450
        line_width, line_height = font_instructions.size(instructions[0])
        for line in instructions:
            text = font_instructions.render(line, True, (102, 102, 102))
            y += line_height
            text_pos = (15, y)
            self.background.blit(text, text_pos)

    def setup(self):
        self.selection = None
        self.sprites  = pygame.sprite.OrderedUpdates()
        self.pos_ingredients = {'butter': (15, 210), 'eggs': (750, 185), \
                'milk': (75, 170), 'flour': (667, 180), 'sugar': \
                (580, 170), 'mayonnaise': (715, 175), 'ketchup': \
                (555, 163), 'pepper': (645, 197)}
        # list of all food and positions on the screen
        self.correct_ingredients = ['butter', 'eggs', 'milk', 'flour', \
                'sugar']
        self.checked_ingredients = 0
        self.hand = Hand() #load hand
        self.icons = pygame.sprite.Group()
        self.icons.add([Icons('stop')])
        self.checked = pygame.sprite.Group()
        self.ingredients = self.groupingredients(self.pos_ingredients)
        self.container = pygame.Rect(370, 315, 225, 65)
        self.sprites = pygame.sprite.OrderedUpdates()
        self.sprites.add([self.icons, self.ingredients, self.hand])
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
                correct = False
                for i in range(0, len(self.correct_ingredients)):
                    if self.selection.name == self.correct_ingredients[i]:
                        correct = True
                ingredient_in_container = \
                        self.container.colliderect(self.selection.rect)
                if ingredient_in_container and correct:
                    if self.selection.name == 'butter':
                        self.selection.rect.topleft = (self.container[0] \
                                , self.container[1] + 10)
                    elif self.selection.name == 'eggs':
                        self.selection.rect.topleft = (self.container[0] \
                                + 45, self.container[1] + 20)
                    elif self.selection.name == 'milk':
                        self.selection.rect.topleft = (self.container[0] \
                                + 85, self.container[1] - 20)
                    elif self.selection.name == 'flour':
                        self.selection.rect.topleft = (self.container[0] \
                                + 125, self.container[1] + 15)
                    elif self.selection.name == 'sugar':
                        self.selection.rect.topleft = (self.container[0] \
                                + 160, self.container[1] - 30)
                    self.selection.rect.size = (0, 0)
                    self.selection.kill()
                    self.selection.add(self.sprites)
                    self.checked_ingredients += 1
                    if self.checked_ingredients >= 5:
                        self.sprites.add([Check(self.container.center)])
                        self.finished_ = True
                else:
                    self.selection.update((self.selection.orig))
            if event.type == MOUSEBUTTONDOWN:
                self.selection = pygame.sprite.Group()
                if pygame.sprite.spritecollideany(self.hand, \
                        self.ingredients):
                    self.selection = pygame.sprite.spritecollideany(self.hand, \
                            self.ingredients)
                if self.selection:
                    self.button_down = 1
                    self.selection.remove(self.sprites)
                    self.selection.add(self.sprites)
            self.hand.remove(self.sprites)
            self.hand.add(self.sprites)
            self.screen.blit(self.background, (0,0))
            self.sprites.draw(self.screen)
            pygame.display.update()
