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
        self.imagen_normal = constants.images_puzzle+'/puzzle_p'+numimage+'.png'
        self.image = pygame.image.load(self.imagen_normal)
        self.rect = self.image.get_rect()
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
        self.image_normal = constants.images_puzzle+"/all-scroll2.png"
        self.image_close =  constants.images_puzzle+"/grabbing2.png"
        self.image = pygame.image.load(self.image_normal)
        self.color = 0
        self.rect = self.image.get_rect()

    def change_hand(self):
        if self.color == 0:
            self.color = 1
        else:
            self.color = 0

    def update(self, mover=(0,0)):
        self.rect.x = mover[0] - self.image.get_width() / 2
        self.rect.y = mover[1] - self.image.get_height() / 2
        if self.color == 0:
            self.image = pygame.image.load(self.image_normal)
        if self.color == 1:
            self.image = pygame.image.load(self.image_close)


class PuzzleActivity(Activity):
    def __init__(self, screen):
        Activity.__init__(self, screen)

    def setup_background(self):
        self.background = pygame.image.load(constants.illustration_puzzle).convert_alpha()

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
          ImagePuzzle(300,100,1,"5"),\
          ImagePuzzle(500,100,2,"5"),\
          ImagePuzzle(300,250,3,"5"),\
          ImagePuzzle(500,250,4,"5")])
        """add the 4 pictures to the sprite groups"""
        self.pictures.add([\
          ImagePuzzle(100,0,1,"1"),\
          ImagePuzzle(100,150,2,"2"),\
          ImagePuzzle(100,300,3,"3"),\
          ImagePuzzle(100,450,4,"4")])
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
                    if pygame.sprite.spritecollideany\
                      (self.hand, self.icons):
                        self.quit = True
                        return
                    self.button_down = 1
                    self.selection = pygame.sprite.spritecollideany\
                      (self.hand, self.pictures)
                    #print self.selection
                    """put the picture select and the hand in the
                     front of the queue"""
                    if self.selection and self.selection.fix == 0:
                        self.selection.kill()
                        self.hand.kill()
                        self.pictures.add([self.selection])
                        self.sprites.add([self.selection])
                        self.sprites.add([self.hand])
                        #self.sprites.move_to_front(self.selection)
                        #self.sprites.move_to_front(self.hand)
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
                """update all the screen"""
                pygame.display.update()
