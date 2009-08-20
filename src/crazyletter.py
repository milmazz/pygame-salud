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


class Container(Sprite):
    """Define a container to the correct word
       pos container position
       letter correct letter that the container contains"""
    def __init__(self, pos, letter, color):
        Sprite.__init__(self)
        image_name = os.path.join(constants.data_folder, "crazyletter",
                                  "container_" + color + ".png")
        self.image, self.rect = common.load_image(image_name)
        self.rect.move_ip(pos)
        self.letter = letter


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


class Letters(Sprite):
    def __init__(self, pos, letter, id):
        Sprite.__init__(self)
        image_name = os.path.join(constants.data_folder, "crazyletter",
                                  letter + ".png")
        self.image, self.rect = common.load_image(image_name)
        self.rect.move_ip(pos)
        self.letter = letter
        self.id = id
        self.orig = pos
        self.fix = 0

    def update(self, pos):
        if self.fix == 0:
            self.rect.x, self.rect.y = pos


class CrazyLetterActivity(Activity):
    def __init__(self, screen):
        Activity.__init__(self, screen)
        self.selection = None
        self.count = 0

    def groupContainer(self, positions, word, color):
        containers = pygame.sprite.Group()
        for i in range(len(word)):
            containers.add([Container(positions[i], word[i], color)])
        return containers

    def groupLetters(self):
        letters   = pygame.sprite.Group()
        positions = [(178, 337), (596, 333), (165, 285), \
                      (605, 294), (183, 244), (580, 255), \
                      (576, 219), (223, 140), (250, 182), \
                      (555, 190), (540, 127), (293, 195), \
                      (317, 177), (523, 192), (269, 138), \
                      (140, 314), (145, 205), (204, 195), \
                      (647, 296), (226, 222), (632, 255), \
                      (650, 345), (615, 213), (336, 133), \
                      (580, 152), (420, 133), (500, 145), \
                      (380, 127), (466, 121), (122, 360)]
        stringLetters = 'bacdefghijklilmnopqrsoetuvxwyz'
        for i in range(len(stringLetters)):
            letters.add([Letters(positions[i], stringLetters[i],i)])
        return letters


    def setup(self):
        self.background = common.load_image(constants.illustration_002)[0]
        #position of the red container
        self.informative_text()
        position_red = [(20,560), (70,560), (120,560), \
                 (170,560), (220,560), (270,560), \
                 (320, 560)]
        #position of the green container
        position_green = [ (500,560), (550,560), (600,560), \
                    (650,560), (700,560)]
        self.hand = Hand() 
        self.icons = pygame.sprite.Group()
        self.icons.add([Icons('stop')])
        self.letters = self.groupLetters()
        container_red = self.groupContainer(position_red, 'higiene',
                'red')
        container_green = self.groupContainer(position_green, 'salud',
                'green')
        self.containers = pygame.sprite.Group()
        self.containers.add([container_red, container_green])
        self.sprites = pygame.sprite.OrderedUpdates()
        self.sprites.add([self.icons, self.containers, self.letters, \
                self.hand])
        pygame.mouse.set_visible( False ) #oculntar el puntero del mouse
        self.button_down = 0
        pos = pygame.mouse.get_pos()
        self.hand.update(pos)
        self.screen.blit(self.background, (0,0))
        self.sprites.draw(self.screen)
        pygame.display.update()
        pygame.event.clear()


    def informative_text(self):
        if pygame.font:
            font = pygame.font.SysFont("dejavusans", 32)
            text = font.render("Letras locas", 1, (0, 0, 0))
            textRect = text.get_rect()
            textRect.centerx = self.screen.get_rect().centerx
            textRect.centery = 20
            self.background.blit(text, textRect)

            font = pygame.font.SysFont("dejavusans", 20)
            instructions = [u"     Busca las letras que conforman la palabra"\
              +  u"\"HIGIENE\" y arrástralas ",
              u"a los cuadros  rojos una por una. También  puedes buscar"\
              + " las  letras",
              u"que   conforman   la  palabra  \"SALUD\" y  arrástralas  a  los "\
              + u" cuadros",
              u"verdes una  por una."]
            y = 39
            for line in instructions:
                text = font.render(line, 1,(0, 0, 0))
                self.background.blit(text, (20, y))
                y+=20

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
                letter_in_container = \
                        pygame.sprite.spritecollideany(self.selection, \
                        self.containers)
                if letter_in_container:
                    if self.selection.letter == letter_in_container.letter:
                        if self.selection.fix == 0:
                            self.count += 1
                            self.selection.fix = 1
                        if self.count == 12:
                            self.finished_ = True
#                        self.selection.rect.x, self.selection.rect.y = \
#                                letter_in_container.rect.x, \
#                                letter_in_container.rect.y
                        self.selection.rect = \
                                letter_in_container.rect
                        check = self.selection.rect.center
                        self.sprites.add(Check(check, 0, (20, 20)))
                    else:
                        self.selection.update(self.selection.orig)
                else:
                    self.selection.color = 0
                    self.selection.update(self.selection.orig)
            if event.type == MOUSEBUTTONDOWN:
                self.selection = pygame.sprite.spritecollideany(self.hand, \
                        self.letters)
                for list in pygame.sprite.spritecollide(self.hand, \
                        self.letters, 0):
                    x = pos[0] + self.hand.rect.width / 2
                    y = pos[1] + self.hand.rect.height / 2
                    if list.rect.collidepoint(x,y):
                        self.selection = list
                if self.selection:
                    self.button_down = 1
            self.hand.remove(self.sprites)
            self.hand.add(self.sprites)
            self.screen.blit(self.background, (0,0))
            self.sprites.draw(self.screen)
            pygame.display.update()
