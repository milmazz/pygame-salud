# vim:ts=4:sts=4:et:nowrap:tw=77
# -*- coding: utf-8 -*-
import pygame
from pygame.sprite import Sprite
from pygame.locals import *

import constants
from activity import Activity
import common
from icons import Icons


class Container(Sprite):

    """Define a container to the correct word
       pos container position
       letter correct letter that the container contains"""
    def __init__(self, pos, letter, color):
        Sprite.__init__(self)
        self.container = '../data/crazyletter/container_'+color+'.png'
        self.image = pygame.image.load(self.container)
        self.rect = self.image.get_rect()
        self.rect.move_ip(pos)
        self.letter = letter

class Hand(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image_normal = constants.images_cletter+"/all-scroll2.png"
        self.image_close =  constants.images_cletter+"/grabbing2.png"
        self.image = pygame.image.load(self.image_normal)
        self.color = 0
        self.rect = self.image.get_rect()

    def change_hand(self):
        if self.color == 0:
            self.color = 1
        else:
            self.color = 0

    def update(self, mover=(0,0)):
        self.rect.x = mover[0] 
        self.rect.y = mover[1] 
        if self.color == 0:
            self.image = pygame.image.load(self.image_normal)
        if self.color == 1:
            self.image = pygame.image.load(self.image_close)

class Letters(Sprite):

    def __init__(self, pos, letter, id):
        Sprite.__init__(self)
        self.imagen_normal = constants.images_cletter+'/'+letter+'_normal.png'
        #self.imagen_color  = constants.images_cletter+'/'+letter+'_color.png'
        self.image = pygame.image.load(self.imagen_normal)
        self.rect = self.image.get_rect()
        self.rect.move_ip(pos)
        self.color = 0 #0 normal 1 coloreada 2 terminada
        self.letter = letter
        self.id = id
        self.orig = pos

    def update(self, pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        #if self.color == 1:
        #    self.image = pygame.image.load(self.imagen_color)
        #elif self.color == 0:
        #    self.image = pygame.image.load(self.imagen_normal)

    def back(self):
        self.rect.x = self.orig[0]
        self.rect.y = self.orig[1]

class View():

    def __init__(self):
       self.pos = 0
       #self.size = (800, 600)
       #self.screen = pygame.display.set_mode(self.size, 0, 32)
       self.background = pygame.image.load(constants.illustration_002).convert_alpha()
       #self.background = pygame.transform.scale(self.background, self.size)

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


class CrazyLetterActivity(Activity):
    def __init__(self, screen):
        Activity.__init__(self, screen)

    def setup(self):
        self.informative_text()
        #position of the blue container
        position_blue = [(20,500), (70,500), (130,500), \
                 (180,500), (230,500), (280,500), \
                 (330, 500)]

        #position of the yellow container
        position_yellow = [ (500,500), (550,500), (600,500), \
                    (650,500), (700,500)]
        self.view = View() #cargamos el fondo estatico
        self.hand = Hand() 
        self.icons = pygame.sprite.Group()
        self.icons.add([Icons('stop')])
        self.letters = self.view.groupLetters()
        container_blue = self.view.groupContainer(position_blue, 'higiene', 'blue')
        container_yellow = self.view.groupContainer(position_yellow, 'salud', 'yellow')
        self.contenedor = pygame.sprite.Group()
        self.contenedor.add([container_blue, container_yellow])
        self.sprites = pygame.sprite.OrderedUpdates()
        self.sprites.add([self.icons, container_blue, container_yellow, self.letters, self.hand])
        pygame.mouse.set_visible( False ) #oculntar el puntero del mouse
        self.screen.blit(self.view.background, (0,0))
        self.sprites.draw(self.screen)
        self.informative_text()
        pygame.display.update()
        #mouse button is down
        self.button_down = 0

    def informative_text(self):
        if pygame.font:
            font = pygame.font.SysFont("dejavusans", 32)
            font.set_bold(True)
            text = font.render("Letras locas", 1, (0, 0, 0))
            textRect = text.get_rect()
            textRect.centerx = self.screen.get_rect().centerx
            textRect.centery = 20
            self.screen.blit(text, textRect)


            font = pygame.font.SysFont("dejavusans", 20)
            font.set_bold(False)
            instructions = [u"     Busca entre las letras la palabra \"HIGIENE\" y arrástralas al recuadro.",
                            u"Pregunta a tu profesora, profesor o a tus papás qué significa esa palabra.",
                            u"También puedes buscar la palabra \"SALUD\"."]
            y = 40
            for line in instructions:
                text = font.render(line, 1,(0, 0, 0))
                self.screen.blit(text, (20, y))
                y+=20


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
                    self.screen.blit(self.view.background, (0,0))
                    self.sprites.draw(self.screen)
                    self.informative_text()
                    pygame.display.update()
                if event.type == MOUSEMOTION and self.button_down:
                    selection.update(pos)
                if event.type == MOUSEBUTTONDOWN:
                    if pygame.sprite.spritecollideany(self.hand, self.icons):
                        self.quit = True
                        return
                    self.hand.change_hand()
                    self.hand.update(pos)
                    self.screen.blit(self.view.background, (0,0))
                    self.sprites.draw(self.screen)
                    self.informative_text()
                    pygame.display.update()
                if event.type == MOUSEBUTTONUP:
                    print pos
                    self.hand.change_hand()
                    self.hand.update(pos)
                    self.screen.blit(self.view.background, (0,0))
                    self.sprites.draw(self.screen)
                    self.informative_text()
                    pygame.display.update()
                    #print pos

                if event.type == MOUSEBUTTONUP and selection:
                    self.button_down = 0
                    letter_in_container = pygame.sprite.spritecollideany(selection, self.contenedor)
                    if letter_in_container:
                        if selection.letter != letter_in_container.letter:
                            selection.back()
                            selection.update(selection.orig)
                            self.screen.blit(self.view.background, (0,0))
                            self.sprites.draw(self.screen)
                            self.informative_text()
                            pygame.display.update()
                    else:
                        selection.color = 0
                        selection.update(pos)
                if event.type == MOUSEBUTTONDOWN:
                    selection = pygame.sprite.spritecollideany(self.hand, self.letters)
                    for list in pygame.sprite.spritecollide(self.hand, self.letters,0):
                        x = pos[0] + self.hand.rect.width / 2
                        y = pos[1] + self.hand.rect.height / 2
                        if list.rect.collidepoint(x,y):
                            selection = list
 
                    if selection:
                        selection.color = 1
                        self.button_down = 1
        
