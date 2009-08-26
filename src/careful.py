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
from icons import *

class Text(Sprite):
    def __init__(self, id, finalRect, initPos):
        Sprite.__init__(self)
        image_path = os.path.join(constants.data_folder,\
          'careful', 'text_'+id+'.png')
        self.image, self.rect = common.load_image(image_path)
        self.id = id
        self.finalRect = finalRect
        self.update(initPos)

    def update(self, move):
        self.rect.x = move[0]
        self.rect.y = move[1]


class Hand(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image_normal = os.path.join(constants.data_folder,\
          'cursors', "hand-open.png")
        self.image_close = os.path.join(constants.data_folder,\
          'cursors', "hand-close.png")
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
        self.rect.x = mover[0] 
        self.rect.y = mover[1] 
        if self.color == 0:
            self.image = pygame.image.load(self.image_normal)
        if self.color == 1:
            self.image = pygame.image.load(self.image_close)


class CarefulActivity(Activity):
    def __init__(self, screen):
        Activity.__init__(self, screen)

    def setup_background(self):
        self.background = common.load_image(constants.illustration_018)[0]
        self.instruction_text()

    def instruction_text(self):
        if pygame.font:
            font = pygame.font.SysFont('dejavusans', 24)
            title = unicode("Cuidado con los accidentes", 'utf-8')
            text = font.render(title, True, (0, 0, 0))
            textRect = text.get_rect()
            x, y = 25, 520
            textRect.topleft = (x, y)
            self.background.blit(text, textRect)

            messages = ["Arrastra hasta los globitos lo que dice cada",
            "personaje en cada situación."]
            
            y += font.get_linesize()
            font = pygame.font.SysFont("dejavusans", 16)
            font_height = font.get_linesize()

            for message in messages:
                message = unicode(message, 'utf-8')
                text = font.render(message, True, (122, 122, 122))
                textRect = text.get_rect()
                textRect.topleft = (x, y)
                y += font_height
                self.background.blit(text, textRect)

    def setup(self):
        """Turn off the mouse pointer"""
        pygame.mouse.set_visible( False )
        """change the mouse pointer by a hand"""
        self.button_down = 0
        self.rectList = [ 
                pygame.Rect(218, 60, 106, 67),
                pygame.Rect(372, 278, 87, 52),
                pygame.Rect(552, 247, 77, 57),
                ]
        self.sprites = pygame.sprite.OrderedUpdates()
        self.icons = pygame.sprite.Group()
        self.icons.add([Icons('stop')])
        image_check = image_normal = os.path.join(constants.icons_folder,\
                "check.png")
        self.checkImage, self.checkRect = common.load_image\
          (image_check)
        self.hand = Hand()

        self.text = pygame.sprite.Group()
        self.text.add([\
          Text('1', self.rectList[0], (10, 20)),
          Text('2', self.rectList[1], (10, 160)),
          Text('3', self.rectList[2], (10, 300)),
          ])
        self.sprites.add([self.icons, self.text, self.hand])
        pos = pygame.mouse.get_pos()
        self.sprites.draw(self.screen)
        self.down = 0
        self.selection = None

    def handle_events(self):
        verify_rect = None
        for event in self.get_event():
            pos = pygame.mouse.get_pos()
            if event.type == QUIT:
                self.quit = True
                return
            elif event.type == MOUSEMOTION:
                if self.down == 1:
                    self.selection = pygame.sprite.spritecollideany\
                      (self.hand, self.text)
                    if self.selection:
                        self.selection.update(pos)
                self.hand.update(pos)
            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    self.quit = True
                    return
            elif event.type == MOUSEBUTTONUP:
                self.down = 0
                if self.selection:
                    verify_rect = self.selection.rect.collidelistall\
                      (self.rectList)
                    if verify_rect and\
                      self.selection.finalRect == self.rectList[verify_rect[0]]:
                        self.background.blit(self.selection.\
                            image, self.selection.finalRect)
                        """If the selection is a valid object,
                        delete the object from the list"""
                        objectSelected = self.rectList[verify_rect[0]]
                        self.selection.kill()
                        del self.rectList[verify_rect[0]]
                        """draw the check image in the center
                        of the rect selected"""
                        self.background.blit(self.checkImage,\
                        (objectSelected.centerx - self.checkRect.centerx,\
                        objectSelected.centery - self.checkRect.centery))

                self.selection = None

            elif event.type == MOUSEBUTTONDOWN:
                self.down = 1
                if pygame.sprite.spritecollideany\
                  (self.hand, self.icons):
                    self.quit = True
                    return

        self.screen.blit(self.background, (0,0))
        self.sprites.draw(self.screen)
        pygame.display.update()

        if len(self.rectList) == 0:
            self.finished_ = True
