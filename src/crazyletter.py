import pygame
from pygame.sprite import Sprite
from pygame.locals import *

import constants
from activity import Activity
import common


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
        if mover[0] - 10 >= 0:
            self.rect.x = mover[0] -5
        if mover[1] - 45 >= 0:
            self.rect.y = mover[1] - 10
        if self.color == 0:
            self.image = pygame.image.load(self.image_normal)
        if self.color == 1:
            self.image = pygame.image.load(self.image_close)

class Letters(Sprite):

    def __init__(self, pos, letter, id):
        Sprite.__init__(self)
        self.imagen_normal = constants.images_cletter+'/'+letter+'_normal.png'
        self.imagen_color  = constants.images_cletter+'/'+letter+'_color.png'
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
        if self.color == 1:
            self.image = pygame.image.load(self.imagen_color)
        elif self.color == 0:
            self.image = pygame.image.load(self.imagen_normal)

    def back(self):
        self.rect.x = self.orig[0]
        self.rect.y = self.orig[1]

class Pencil(Sprite):

    def __init__(self):
        Sprite.__init__(self)
        self.image = pygame.image.load(constants.images_cletter+"/lapiz.png")
        self.rect = self.image.get_rect()

    def update(self, mover):
        if mover[0] - 10 >= 0:
            self.rect.x = mover[0] - 10
        if mover[1] - 45 >= 0:
            self.rect.y = mover[1] - 45

class Tippen(Sprite):

    def __init__(self):
        Sprite.__init__(self)
        self.image = pygame.image.load(constants.images_cletter+"/puntalapiz.png")
        self.rect = self.image.get_rect()

    def update(self, mover):
        self.rect.x = mover[0]
        self.rect.y = mover[1]

class View():

    def __init__(self):
       self.pos = 0
       self.size = (800, 600)
       self.screen = pygame.display.set_mode(self.size, 0, 32)
       self.background = pygame.image.load(constants.illustration_002).convert_alpha()
       self.background = pygame.transform.scale(self.background, self.size)
#       self.letrasFijas()

    #def grupoLetras(self):
    #    letras   = pygame.sprite.Group()
    #    letras.add([Letras(223, 263, 'h',1)])
    #    letras.add([Letras(250, 232, 'i',2)])
    #    letras.add([Letras(576, 269, 'g',3)])
    #    letras.add([Letras(327, 177, 'i',4)])
    #    letras.add([Letras(183, 294, 'e',5)])
    #    letras.add([Letras(388, 169, 'n',6)])
    #    letras.add([Letras(605, 223, 'e',7)])
    #    return letras

    def groupContainer(self, positions, word, color):
        containers = pygame.sprite.Group()
        for i in range(len(word)):
            containers.add([Container(positions[i], word[i], color)])
        return containers

    def groupLetters(self):
        letters   = pygame.sprite.Group()
        positions = [(157, 364), (596, 383), (165, 335), \
                      (605, 343), (183, 294), (594, 299), \
                      (576, 269), (223, 263), (250, 232), \
                      (562, 245), (540, 222), (293, 205), \
                      (327, 177), (523, 192), (487, 173), \
                      (388, 169), (446, 165), (184, 264), \
                      (647, 296), (226, 222), (632, 255), \
                      (269, 178), (605, 223), (336, 153), \
                      (569, 172), (414, 133), (500, 145), \
                      (377, 127), (466, 121), (428, 104)]
        stringLetters = 'bacdefghijklilmnopqrsoetuvxwyz'
        for i in range(len(stringLetters)):
            letters.add([Letters(positions[i], stringLetters[i],i)])
        return letters


class CrazyLetterActivity(Activity):
    def __init__(self, screen):
        Activity.__init__(self, screen)

    def setup(self):
        #position of the blue container
        position_blue = [(20,500), (70,500), (130,500), \
                 (180,500), (230,500), (280,500), \
                 (330, 500)]

        #position of the yellow container
        position_yellow = [ (500,500), (550,500), (600,500), \
                    (650,500), (700,500)]
        self.view = View() #cargamos el fondo estatico
        self.pencil = Hand() #cargamos el lapiz
        self.letters = self.view.groupLetters()
        container_blue = self.view.groupContainer(position_blue, 'higiene', 'blue')
        container_yellow = self.view.groupContainer(position_yellow, 'salud', 'yellow')
        self.contenedor = pygame.sprite.Group()
        self.contenedor.add([container_blue, container_yellow])
        self.tippen = Tippen()
        self.sprites = pygame.sprite.OrderedUpdates()
        self.sprites.add([container_blue, container_yellow, self.letters, self.pencil, self.tippen])
        pygame.mouse.set_visible( False ) #oculntar el puntero del mouse
        pygame.display.update()
        #mouse button is down
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
                    self.pencil.update(pos)
                    self.tippen.update(pos)
                    self.view.screen.blit(self.view.background, (0,0))
                    self.sprites.draw(self.view.screen)
                    pygame.display.update()
                if event.type == MOUSEMOTION and self.button_down:
                    selection.update(pos)
                if event.type == MOUSEBUTTONDOWN:
                    self.pencil.change_hand()
                    self.pencil.update()
                    self.view.screen.blit(self.view.background, (0,0))
                    self.sprites.draw(self.view.screen)
                    pygame.display.update()
                if event.type == MOUSEBUTTONUP:
                    self.pencil.change_hand()
                    self.pencil.update()
                    self.view.screen.blit(self.view.background, (0,0))
                    self.sprites.draw(self.view.screen)
                    pygame.display.update()

                if event.type == MOUSEBUTTONUP and selection:
                    self.button_down = 0
                    letter_in_container = pygame.sprite.spritecollideany(selection, self.contenedor)
                    if letter_in_container:
                        if selection.letter == letter_in_container.letter:
                            print "perfecto" 
                        else:
                            selection.back()
                            selection.update(selection.orig)
                            self.view.screen.blit(self.view.background, (0,0))
                            self.sprites.draw(self.view.screen)
                            pygame.display.update()
                    else:
                        selection.color = 0
                        selection.update(pos)
                if event.type == MOUSEBUTTONDOWN:
                    selection = pygame.sprite.spritecollideany(self.tippen, self.letters)
                    if selection:
                        selection.color = 1
                        self.button_down = 1
        
