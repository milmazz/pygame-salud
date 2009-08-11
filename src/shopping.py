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

class Food(Sprite):
    def __init__(self, name, pos=(0,0)):
        Sprite.__init__(self)
        image_name = os.path.join(constants.data_folder, "shopping",
                                  name + ".png")
        self.image, self.rect = common.load_image(image_name)
        self.size_x, self.size_y = self.image.get_size()
        self.rect.move_ip(pos)
        self.orig_x, self.orig_y = pos
        self.name = name
        self.image_small = pygame.transform.scale(self.image,
                (self.size_x/2, self.size_y/2))
        self.image_orig = self.image
        self.small = 0
		
    def change_size(self):
        if self.small == 1:
            self.image = self.image_orig
            self.small = 0
        else:
	        self.image = self.image_small
            self.small = 1
	
    def update(self, pos):
        self.rect.x, self.rect.y = pos


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


class check(Sprite):
    def __init__(self, pos=(0,0)):
        Sprite.__init__(self)
        self.path_check = os.path.join(constants.data_folder, \
                'shopping', "check.png")
        self.image, self.rect = common.load_image(self.path_check)
#        self.size_x, self.size_y = self.image.get_size()
        self.rect.move_ip(pos)
#        self.image_small = pygame.transform.scale(self.image,
#                (self.size_x/2, self.size_y/2))
#        self.image = self.image_small


class Shopping(Activity):
    def __init__(self, screen):
        Activity.__init__(self, screen)
        self.background = common.load_image(constants.illustration_025)[0]

    def groupfood(self, pos_food):
        food = pygame.sprite.Group()
        for name in pos_food:
            food.add([Food(name, pos_food[name])])
        return food

    def instruction_text(self):
        font_title = pygame.font.SysFont("dejavusans", 32)
        font_title.set_bold(True)
        font_instructions = pygame.font.SysFont("dejavusans", 20)
        title = u"¡De compras!"
        title_width, title_height = font_title.size(title)
        instructions = [u"Coloca en cada carrito de mercado los"\
                u" alimentos que corresponden.", u"Arrastra el" \
                u" alimento al carrito respectivo"]
        y = 5
        text = font_title.render(title, True, (102, 102, 102))
        text_pos = (constants.screen_mode[0]/2.0 - title_width/2.0, y)
        self.screen.blit(text, text_pos)
        y = 20
        line_width, line_height = font_instructions.size(instructions[0])
        for line in instructions:
            text = font_instructions.render(line, True, (102, 102, 102))
            y += line_height
            text_pos = (35, y)
            self.screen.blit(text, text_pos)

    def setup(self):
        self.cont = None
        self.selection = None
        self.correct_container = None
        self.sprites  = pygame.sprite.OrderedUpdates()
        self.pos_vegetables = {'beetroot': (52, 162), 'carrot': (295, 238), \
                'cauliflower': (57, 347), 'x': (295, 450)}
        self.pos_fruits = {'banana': (252, 165), 'watermelon': (46, 220), \
                'pineapple': (239, 324), 'pear': (53, 440), 'grape': (50, \
                520), 'apple': (448, 529)}
        self.pos_meats = {'chicken': (247, 124), 'fish': (57, 287), \
                'meat': (278, 508)}
        self.pos_milks = {'milk': (142, 126), 'milk2': (160, 387), \
                'cheese': (415, 239), 'cheese2': (155, 475)}
        # list of all food and positions on the screen
        self.correct_vegetables = ['beetroot', 'carrot', 'cauliflower', 'x']
        self.correct_fruits = ['banana', 'watermelon', 'pineapple', \
                'pear', 'grape', 'apple']
        self.correct_meats = ['chicken', 'fish', 'meat']
        self.correct_milks = ['milk', 'milk2', 'cheese', 'cheese2']
        self.checked_vegetables = 0
        self.checked_fruits = 0
        self.checked_meats = 0
        self.checked_milks = 0
        self.hand = Hand() #load hand
        self.icons = pygame.sprite.Group()
        self.icons.add([Icons('stop')])
        self.checked = pygame.sprite.Group()
        self.vegetables = pygame.sprite.Group()
        self.fruits = pygame.sprite.Group()
        self.meats = pygame.sprite.Group()
        self.milks = pygame.sprite.Group()
        self.vegetables = self.groupfood(self.pos_vegetables)
        self.fruits = self.groupfood(self.pos_fruits)
        self.meats = self.groupfood(self.pos_meats)
        self.milks = self.groupfood(self.pos_milks)
        self.containers = [pygame.Rect(425, 80, 190, 100), \
                pygame.Rect(575, 205, 190, 100), \
                pygame.Rect(423, 313, 190, 100), \
                pygame.Rect(560, 449, 190, 100)]
        self.sprites = pygame.sprite.OrderedUpdates()
        self.sprites.add([self.icons, self.vegetables, self.fruits, \
                self.meats, self.milks, self.hand])
        pygame.mouse.set_visible( False ) #hide pointer
        self.button_down = 0
        pos = pygame.mouse.get_pos()
        self.hand.update(pos)
        self.screen.blit(self.background, (0,0))
        self.sprites.draw(self.screen)
        self.instruction_text()
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
                self.hand.change_hand()
                self.hand.update(pos)
            if event.type == MOUSEBUTTONUP:
                self.hand.change_hand()
                self.hand.update(pos)
            if event.type == MOUSEBUTTONUP and self.selection:
                self.button_down = 0
                food_in_container = \
                        self.selection.rect.colliderect(self.containers[self.correct_container])
                if food_in_container:
                    if self.correct_container == 0:
                        self.checked_vegetables = self.checked_vegetables + 1
                        if self.checked_vegetables >= 4:
                            self.checked.add([check((self.containers[self.correct_container][0], \
                                    self.containers[self.correct_container][1]))])
                            self.checked_vegetables = -1
                    if self.correct_container == 1:
                        self.checked_fruits = self.checked_fruits + 1
                        if self.checked_fruits >= 6:
                            self.checked.add([check((self.containers[self.correct_container][0], \
                                    self.containers[self.correct_container][1]))])
                            self.checked_fruits = -1
                    if self.correct_container == 2:
                        self.checked_meats = self.checked_meats + 1
                        if self.checked_meats >= 3:
                            self.checked.add([check((self.containers[self.correct_container][0], \
                                    self.containers[self.correct_container][1]))])
                            self.checked_meats = -1
                    if self.correct_container == 3:
                        self.checked_milks = self.checked_milks + 1
                        if self.checked_milks >= 4:
                            self.checked.add([check((self.containers[self.correct_container][0], \
                                    self.containers[self.correct_container][1]))])
                            self.checked_milks = -1
                    self.selection.rect = ((pos), (0, 0))
                    self.selection.kill()
                    self.selection.add(self.sprites)
                    """if self.checked_vegetables == 4:
                        self.checked.add([check((self.containers[0][0], \
                                self.containers[0][1]))])
                    if self.checked_fruits == 6:
                        self.checked.add([check((self.containers[1][0], \
                                self.containers[1][1]))])
                    if self.checked_meats == 3:
                        self.checked.add([check((self.containers[2][0], \
                                self.containers[2][1]))])
                    if self.checked_milks == 4:
                        self.checked.add([check((self.containers[3][0], \
                                self.containers[3][1]))])"""
#                    self.selection.rect = ((self.selection.orig_x, \
#                            self.selection.orig_y), (0, 0))
#                    self.checked.add([check((self.selection.orig_x + \
#                            (self.selection.size_x - 76)/2, \
#                            self.selection.orig_y + (self.selection.size_y - \
#                            70)/2))])
#                    self.checked.add([check((pos))])
                    self.sprites.add([self.checked])
                else:
                    self.selection.change_size()
                    self.selection.update((self.selection.orig_x, self.selection.orig_y))
            if event.type == MOUSEBUTTONDOWN:
                self.selection = pygame.sprite.Group()
                if pygame.sprite.spritecollideany(self.hand, \
                        self.vegetables):
                    self.selection = pygame.sprite.spritecollideany(self.hand, \
                            self.vegetables)
                    self.correct_container = 0
                if pygame.sprite.spritecollideany(self.hand, \
                        self.fruits):
                    self.selection = pygame.sprite.spritecollideany(self.hand, \
                            self.fruits)
                    self.correct_container = 1
                if pygame.sprite.spritecollideany(self.hand, \
                        self.meats):
                    self.selection = pygame.sprite.spritecollideany(self.hand, \
                            self.meats)
                    self.correct_container = 2
                if pygame.sprite.spritecollideany(self.hand, \
                        self.milks):
                    self.selection = pygame.sprite.spritecollideany(self.hand, \
                            self.milks)
                    self.correct_container = 3
                if self.selection:
                    self.selection.change_size()
                    self.button_down = 1
                    self.selection.remove(self.sprites)
                    self.selection.add(self.sprites)
            if self.checked_vegetables == -1 and self.checked_fruits == -1 \
                    and self.checked_meats == -1 and self.checked_milks == -1:
                        self.finished_ = True
            self.hand.remove(self.sprites)
            self.hand.add(self.sprites)
            self.screen.blit(self.background, (0,0))
            self.instruction_text()
            self.sprites.draw(self.screen)
            pygame.display.update()
