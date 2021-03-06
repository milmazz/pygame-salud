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
    def __init__(self, x, y, id, numimage, numpuzzle=''):
        Sprite.__init__(self)
        self.imagen_normal = os.path.join(constants.images_puzzle,
                'puzzle'+numpuzzle+'_p'+numimage+'.png')
        self.image, self.rect = common.load_image(self.imagen_normal)
        self.rect.x = x
        self.rect.y = y
        self.id = id # id to compare between images
        self.fix = 0 # fix if the correct image is in the correct position

    def update(self, pos=(0, 0)):
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


class PuzzleBase(Activity):
    def __init__(self, screen):
        Activity.__init__(self, screen)
        self.count = 0
        self.id = ""
        # Change the mouse pointer by a hand
        self.button_down = 0
        self.selection = 0
        self.hand = Hand()
        self.sprites    = pygame.sprite.OrderedUpdates()
        self.pictures   = pygame.sprite.Group() # Picture that can be move
        self.transparent= pygame.sprite.Group() # Picture that cann't be move
        self.icons      = pygame.sprite.Group()
        self.icons.add([Icons('stop')])
        self.transparent.add([ \
          ImagePuzzle(302, 100, 1, "5"), \
          ImagePuzzle(500, 100, 2, "5"), \
          ImagePuzzle(302, 250, 3, "5"), \
          ImagePuzzle(500, 250, 4, "5")]
        )

    def setup_background(self):
        self.background, rect = common.load_image(constants.illustration_puzzle)

    def informative_text(self):
        if pygame.font:
            font = pygame.font.SysFont(constants.font_title[0], constants.font_title[1])
            text = font.render("Arma las piezas del rompecabezas", True, constants.font_title_color)
            textRect = text.get_rect()
            textRect.centerx = self.screen.get_rect().centerx
            textRect.centery = font.get_linesize() / 2.0
            self.background.blit(text, textRect)

            y = 1.5 * font.get_linesize()
            font = pygame.font.SysFont(constants.font_default[0], constants.font_default[1])
            instructions = [u"Arrastra las piezas con el ratón hacia el" \
                    + u" recuadro."]
            line_height = font.get_linesize()

            for line in instructions:
                text = font.render(line, True, constants.font_default_color)
                self.background.blit(text, (20, y))
                y += line_height

    def setup(self):
        """Turn off the mouse pointer"""
        pygame.mouse.set_visible(False)
        """add the 4 pictures to the sprite groups"""
        self.pictures.add([\
          ImagePuzzle(550, 450, 1, "1", self.id), \
          ImagePuzzle(300, 450, 2, "2", self.id), \
          ImagePuzzle(50, 150, 3, "3", self.id), \
          ImagePuzzle(50, 350, 4, "4", self.id)])
        self.informative_text()
        self.screen.blit(self.background, (0, 0))
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
                        verify_correct = pygame.sprite.spritecollide\
                          (self.selection, self.transparent, False)
                        if len(verify_correct) == 1 and\
                          verify_correct[0].id == self.selection.id and\
                          self.selection.fix == 0:
                                self.selection.fix = 1
                                self.selection.rect = verify_correct[0].rect
                                self.count += 1 
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
                if self.count == 4:
                    ok_button = pygame.image.load("../data/puzzle/ok.png").convert_alpha()
                    self.screen.blit(ok_button, (300,101))
                    self.finished_ = True
                """update all the screen"""
                pygame.display.update()

class PuzzleActivity(PuzzleBase):
    def __init__(self, screen):
        PuzzleBase.__init__(self, screen)

class Puzzle2Activity(PuzzleBase):
    def __init__(self, screen):
        PuzzleBase.__init__(self, screen)
        self.id = '2'

class Puzzle3Activity(PuzzleBase):
    def __init__(self, screen):
        PuzzleBase.__init__(self, screen)
        self.id = '3'

class Puzzle4Activity(PuzzleBase):
    def __init__(self, screen):
        PuzzleBase.__init__(self, screen)
        self.id = '4'
