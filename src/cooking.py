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

class Ingredients(Sprite):
    def __init__(self, pos, ingredient):
        Sprite.__init__(self)
        image_name = os.path.join(constants.data_folder, "cooking",
                                  ingredient  + ".png")
        self.image, self.rect = common.load_image(image_name)
        self.rect.move_ip(pos)
        self.name = ingredient
		
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


class View():
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600), 0, 32)
        self.background = common.load_image(constants.illustration_024)[0]

    def groupIngredients(self, pos_ingredients):
        ingredients = pygame.sprite.Group()
        for name in pos_ingredients:
            ingredients.add([Ingredients(pos_ingredients[name], name)])
        return ingredients


class Cooking(Activity):
    def __init__(self, screen):
        Activity.__init__(self, screen)

    def setup(self):
        self.sprites  = pygame.sprite.OrderedUpdates()
        pos_ingredients = {'sugar': (400, 300)} # list of all ingredients and
                                                # positions on the screen
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
                font_title = pygame.font.SysFont("dejavusans", 40)
                font_instructions = pygame.font.SysFont("dejavusans", 20)
                title = u"¡A cocinar!"
                title_width, title_height = font_title.size(title)
                instructions = [u"Vamos a hacer una torta ...",
                                u"Observa los ingredientes que se necesitan",
                                u"y arrástralos hasta la mesa."]
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
                self.sprites.draw(self.view.screen)
                pygame.display.update()

