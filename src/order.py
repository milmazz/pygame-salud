# vim:ts=4:sts=4:et:nowrap:tw=77
# -*- coding: utf-8 -*-

import os
import time

import pygame
from pygame.locals import *
from pygame.sprite import Sprite

import constants
from activity import Activity
import common
from icons import Icons

class ImagePuzzle(Sprite):
    def __init__(self, x, y, id, numimage):
        Sprite.__init__(self)
        self.imagen_normal = os.path.join('..', 'data', 'order',
                numimage+'.png')
        self.image, self.rect = common.load_image(self.imagen_normal)
        self.rect.x = x
        self.rect.y = y
        self.id = id #id to compare between images
        self.fix = 0 #fix if the correct image is in the correct position

    def update(self, pos=(0,0)):
        self.rect.x = pos[0]
        self.rect.y = pos[1]

class Hand(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image_normal = os.path.join(constants.images_puzzle,
                                         "all-scroll2.png")
        self.image_close =  os.path.join(constants.images_puzzle,
                                         "grabbing2.png")
        self.normal, self.rect = common.load_image(self.image_normal)
        self.image = self.normal
        self.close, rect = common.load_image(self.image_close)
        self.color = 0

    def change_hand(self):
        if self.color == 0:
            self.color = 1
        else:
            self.color = 0

    def update(self, mover=(0,0)):
        self.rect.x = mover[0] - self.image.get_width() / 2
        self.rect.y = mover[1] - self.image.get_height() / 2
        if self.color == 0:
            self.image = self.normal
        if self.color == 1:
            self.image = self.close


class OrderActivity(Activity):
    def __init__(self, screen):
        Activity.__init__(self, screen)

    def setup_background(self):
        self.background, rect = common.load_image('../data/backgrounds/illustration_009.jpg')

    def informative_text(self):
        if pygame.font:
            font = pygame.font.SysFont('dejavusans', 32)
            font.set_bold(True)
            title = unicode("¿Qué va primero?", 'utf-8')
            text = font.render(title, 1, (0, 0, 0))
            textRect = text.get_rect()
            textRect.centerx = self.screen.get_rect().centerx
            textRect.centery = 20
            self.screen.blit(text, textRect)

            messages = ["Ordena los dibujos y numéralos (1, 2, 3, 4 y 5)", \
                "en cada cuadro siguiendo la secuencia."]
            
            y = font.get_linesize()
            font = pygame.font.SysFont("dejavusans", 20)
            font_height = font.get_linesize()

            for message in messages:
                message = unicode(message, 'utf-8')
                text = font.render(message, True, (122, 122, 122))
                y += font_height 
                textRect.midtop = (300, y) 
                self.screen.blit(text, textRect)

    def setup(self):
        """Turn off the mouse pointer"""
        pygame.mouse.set_visible( False )
        """change the mouse pointer by a hand"""
        self.button_down = 0
        self.selection = 0
        self.hand = Hand()
        self.sprites    = pygame.sprite.OrderedUpdates()
        self.pictures   = pygame.sprite.Group() #picture that can be move
        self.transparent= pygame.sprite.Group() #picture that cann't be move
        self.icons      = pygame.sprite.Group()
        self.icons.add([Icons('stop')])
        self.transparent.add([\
          ImagePuzzle(188,522,1,"6"),\
          ImagePuzzle(432,409,2,"6"),\
          ImagePuzzle(694,520,3,"6"),\
          ImagePuzzle(688,312,4,"6"),\
          ImagePuzzle(194,299,5,"6")])
        """add the 4 pictures to the sprite groups"""
        self.pictures.add([\
          ImagePuzzle(310,550,1,"1"),\
          ImagePuzzle(355,550,2,"2"),\
          ImagePuzzle(400,550,3,"3"),\
          ImagePuzzle(445,550,4,"4"),\
          ImagePuzzle(490,550,5,"5")])
        self.informative_text()
        self.sprites.add([self.transparent, self.pictures, self.icons, self.hand])
        self.sprites.draw(self.screen)

    def handle_events(self):
            for event in [ pygame.event.wait() ] + pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == QUIT:
                    self.quit = True
                    return
                elif event.type == KEYUP:
                   if event.key == K_ESCAPE:
                       self.quit = True
                       return
                elif event.type == MOUSEBUTTONDOWN and self.button_down == 0:
                    if pygame.sprite.spritecollideany(self.hand, self.icons):
                        self.quit = True
                        return
                    self.button_down = 1
                    self.selection = pygame.sprite.spritecollideany\
                      (self.hand, self.pictures)
                    #print self.selection
                    """put the picture select and the hand in the
                     front of the queue"""
                    if self.selection and self.selection.fix == 0:
                        """This is necesary to have ever the selection picture
                           and the hand in the front"""
                        self.selection.kill()
                        self.hand.kill()
                        self.pictures.add([self.selection])
                        self.sprites.add([self.selection])
                        self.sprites.add([self.hand])
                    self.hand.change_hand() #change de open hand by the close hand
                    self.hand.update(pos) 
                    self.screen.blit(self.background, (0,0))
                    self.sprites.draw(self.screen)
                elif event.type == MOUSEBUTTONUP and self.button_down == 1:
                    if self.selection:
                        verify_correct = pygame.sprite.spritecollideany\
                          (self.selection, self.transparent)
                        if verify_correct and verify_correct.id == self.selection.id:
                            self.selection.fix = 1
                            self.selection.rect = verify_correct.rect
                    self.button_down = 0
                    self.selection = 0
                    self.hand.change_hand() #change the close hand by the open hand
                    self.hand.update(pos)
                    self.screen.blit(self.background, (0,0))
                    self.sprites.draw(self.screen)
                elif event.type == MOUSEMOTION:
                    if self.selection and self.selection.fix == 0\
                      and self.button_down == 1:   
                        self.selection.update(pos)
                    self.hand.update(pos)
                    self.screen.blit(self.background, (0,0))
                    self.sprites.draw(self.screen)
                self.informative_text()
                """update all the screen"""
                pygame.display.update()

class OrderActivity2(Activity):
    def __init__(self, screen):
        Activity.__init__(self, screen)

    def setup_background(self):
        self.background, rect = common.load_image('../data/backgrounds/illustration_013.jpg')

    def informative_text(self):
        if pygame.font:
            font = pygame.font.SysFont('dejavusans', 26)
            #font.set_bold(True)
            title = unicode("Nuestro cuerpo cambia", 'utf-8')
            text = font.render(title, 1, (0, 0, 0))
            textRect = text.get_rect()
            textRect.centerx = self.screen.get_rect().centerx
            textRect.centery = 20
            self.screen.blit(text, textRect)

            font_height = font.get_linesize()
            title = unicode("cuando crecemos", 'utf-8')
            text = font.render(title, True, (0, 0, 0))
            textRect = text.get_rect()
            textRect.centerx = self.screen.get_rect().centerx
            textRect.centery = 15 + font_height
            self.screen.blit(text, textRect)

            messages = ["Cuando eras un bebé, tomabas tetero y usabas",
            "pañal. Eras chiquito, cada",
            "año creces un poco y te vas haciendo más alto.",
            "Ordena del más pequeño al más grande,",
            "pon 1, 2, 3 y 4 en los círculos correspondientes."]
            
            y = font.get_linesize()
            font = pygame.font.SysFont("dejavusans", 20)
            font_height = font.get_linesize()

            for message in messages:
                message = unicode(message, 'utf-8')
                text = font.render(message, True, (122, 122, 122))
                y += font_height 
                textRect.midtop = (300, y) 
                self.screen.blit(text, textRect)

    def setup(self):
        """Turn off the mouse pointer"""
        pygame.mouse.set_visible( False )
        """change the mouse pointer by a hand"""
        self.button_down = 0
        self.selection = 0
        self.hand = Hand()
        self.sprites    = pygame.sprite.OrderedUpdates()
        self.pictures   = pygame.sprite.Group() #picture that can be move
        self.transparent= pygame.sprite.Group() #picture that cann't be move
        self.icons      = pygame.sprite.Group()
        self.icons.add([Icons('stop')])
        self.transparent.add([\
          ImagePuzzle(690,547,1,"7"),\
          ImagePuzzle(204,285,2,"7"),\
          ImagePuzzle(613,284,3,"7"),\
          ImagePuzzle(385,542,4,"7")])
        """add the 4 pictures to the sprite groups"""
        self.pictures.add([\
          ImagePuzzle(100,500,1,"1"),\
          ImagePuzzle(145,500,2,"2"),\
          ImagePuzzle(100,540,3,"3"),\
          ImagePuzzle(145,540,4,"4")])
        self.informative_text()
        self.sprites.add([self.transparent, self.pictures, self.icons, self.hand])
        self.sprites.draw(self.screen)

    def handle_events(self):
            for event in [ pygame.event.wait() ] + pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == QUIT:
                    self.quit = True
                    return
                elif event.type == KEYUP:
                   if event.key == K_ESCAPE:
                       self.quit = True
                       return
                elif event.type == MOUSEBUTTONDOWN and self.button_down == 0:
                    if pygame.sprite.spritecollideany(self.hand, self.icons):
                        self.quit = True
                        return
                    self.button_down = 1
                    self.selection = pygame.sprite.spritecollideany\
                      (self.hand, self.pictures)
                    #print self.selection
                    """put the picture select and the hand in the
                     front of the queue"""
                    if self.selection and self.selection.fix == 0:
                        """This is necesary to have ever the selection picture
                           and the hand in the front"""
                        self.selection.kill()
                        self.hand.kill()
                        self.pictures.add([self.selection])
                        self.sprites.add([self.selection])
                        self.sprites.add([self.hand])
                    self.hand.change_hand() #change de open hand by the close hand
                    self.hand.update(pos) 
                    self.screen.blit(self.background, (0,0))
                    self.sprites.draw(self.screen)
                elif event.type == MOUSEBUTTONUP and self.button_down == 1:
                    if self.selection:
                        verify_correct = pygame.sprite.spritecollideany\
                          (self.selection, self.transparent)
                        if verify_correct and verify_correct.id == self.selection.id:
                            self.selection.fix = 1
                            self.selection.rect = verify_correct.rect
                    self.button_down = 0
                    self.selection = 0
                    self.hand.change_hand() #change the close hand by the open hand
                    self.hand.update(pos)
                    self.screen.blit(self.background, (0,0))
                    self.sprites.draw(self.screen)
                elif event.type == MOUSEMOTION:
                    if self.selection and self.selection.fix == 0\
                      and self.button_down == 1:   
                        self.selection.update(pos)
                    self.hand.update(pos)
                    self.screen.blit(self.background, (0,0))
                    self.sprites.draw(self.screen)
                self.informative_text()
                """update all the screen"""
                pygame.display.update()
