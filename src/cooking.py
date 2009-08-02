# vim:ts=4:sts=4:et:nowrap:tw=77
# -*- coding: utf-8 -*-

import os
import pygame
from pygame.sprite import Sprite
from pygame.locals import *

import constants
from activity import Activity
import common
from common import *

class Ingredients(Sprite):
    def __init__(self, pos, ingredient):
        Sprite.__init__(self)
        image_name = os.path.join(constants.data_folder, "cooking",
                                  ingredient  + ".png")

        self.image, self.rect = common.load_image(image_name)
        self.rect.move_ip(pos)
        self.name = ingredient
        self.orig = pos
		
    def update(self, pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def back(self):
        self.rect.x = self.orig[0]
        self.rect.y = self.orig[1]


class Hand(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image_normal = os.path.join(constants.data_folder, 'cursors',
                                    "hand-open.png")
        self.image_close =  os.path.join(constants.data_folder, 'cursors', 
                                    "hand-close.png")
        self.normal,  self.rect = common.load_image(self.image_normal)
        self.close,  self.rect = common.load_image(self.image_close)
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


class View():
    def __init__(self):
       self.pos = 0
       self.size = (800, 600)
       self.screen = pygame.display.set_mode(self.size, 0, 32)
       self.background = pygame.image.load(constants.illustration_024).convert_alpha()
       self.background = pygame.transform.scale(self.background, self.size)

    def groupIngredients(self, pos_ingredients):
        ingredients = pygame.sprite.Group()
        for name in pos_ingredients:
            ingredients.add([Ingredients(pos_ingredients[name], name)])
        return ingredients


class Cooking(Activity):
    def __init__(self, screen):
        Activity.__init__(self, screen)

    def setup(self):
        #position of the container
        pos_ingredients = {'sugar': (400, 300)}
        self.view = View() #load static background
        self.hand = Hand() #load hand
        self.ingredients = self.view.groupIngredients(pos_ingredients)
        self.container = pygame.Rect(400, 400, 100, 100)
        self.sprites = pygame.sprite.OrderedUpdates()
        self.sprites.add([self.ingredients, self.hand])
        pygame.mouse.set_visible( False ) #hide pointer
        #mouse button is up
        self.button_down = 0

    def handle_events(self):
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
                    self.hand.change_hand()
                    self.hand.update()
                if event.type == MOUSEBUTTONUP:
                    self.hand.change_hand()
                    self.hand.update()
                if event.type == MOUSEBUTTONUP and selection:
                    self.button_down = 0
                    ingredients_in_container = \
                            self.container.colliderect(selection.rect)
                    if ingredients_in_container:
#                        print "Ingrediente: " + selection.name + " esta adentro"
                        pass
                    else:
                        selection.color = 0
                        selection.update(pos)
                if event.type == MOUSEBUTTONDOWN:
                    selection = pygame.sprite.spritecollideany(self.hand, \
                            self.ingredients)
                    if selection:
                        selection.color = 1
                        self.button_down = 1
                self.view.screen.blit(self.view.background, (0,0))
                self.sprites.draw(self.view.screen)
                pygame.display.update()
