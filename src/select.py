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


class SelectActivity(Activity):
    def __init__(self, screen):
        Activity.__init__(self, screen)

    def setup_background(self):
        self.background = common.load_image(constants.illustration_011)[0]
        self.instruction_text()

    def instruction_text(self):
        if pygame.font:
            font = pygame.font.SysFont(constants.font_title[0], constants.font_title[1])
            title = unicode("Una boca bien sana", 'utf-8')
            text = font.render(title, True, (0, 0, 0))
            textRect = text.get_rect()
            textRect.centerx = self.screen.get_rect().centerx
            textRect.centery = 20
            self.background.blit(text, textRect)

            messages = ["  Selecciona aquellos objetos",
            "que son necesarios para mantener tu boca sana."]
            
            y = font.get_linesize()
            font = pygame.font.SysFont(constants.font_default[0], constants.font_default[1])
            font_height = font.get_linesize()

            for message in messages:
                message = unicode(message, 'utf-8')
                text = font.render(message, True, (122, 122, 122))
                textRect = text.get_rect()
                textRect.centerx = self.screen.get_rect().centerx
                y += font_height 
                textRect.centery = y
                self.background.blit(text, textRect)

    def setup(self):
        """Turn off the mouse pointer"""
        pygame.mouse.set_visible( False )
        """change the mouse pointer by a hand"""
        self.button_down = 0
        self.rectList = [ 
                pygame.Rect(311, 91, 158, 51),
                pygame.Rect(546, 414, 67, 121),
                pygame.Rect(157, 358, 72, 109),
                ]
        self.sprites = pygame.sprite.OrderedUpdates()
        self.icons = pygame.sprite.Group()
        self.icons.add([Icons('stop')])
        image_check = image_normal = os.path.join(constants.icons_folder,\
                "check.png")
        self.checkImage, self.checkRect = common.load_image\
          (image_check)
        self.hand = Hand()
        self.sprites.add([self.icons, self.hand])
        pos = pygame.mouse.get_pos()
        self.sprites.draw(self.screen)

    def handle_events(self):
        verify_rect = None
        for event in self.get_event():
            pos = pygame.mouse.get_pos()
            if event.type == QUIT:
                self.quit = True
                return
            elif event.type == MOUSEMOTION:
                    self.hand.update(pos)

            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    self.quit = True
                    return
            elif event.type == MOUSEBUTTONDOWN:
                if pygame.sprite.spritecollideany\
                  (self.hand, self.icons):
                    self.quit = True
                    return
                verify_rect = self.hand.rect.collidelistall(self.rectList)
                if verify_rect:
                    """If the selection is a valid object,
                    delete the object from the list"""
                    objectSelected = self.rectList[verify_rect[0]]
                    del self.rectList[verify_rect[0]]
                    """draw the check image in the center
                    of the rect selected"""
                    self.background.blit(self.checkImage,\
                     (objectSelected.centerx - self.checkRect.centerx,\
                     objectSelected.centery - self.checkRect.centery))

        self.screen.blit(self.background, (0,0))
        self.sprites.draw(self.screen)
        pygame.display.update()

        if len(self.rectList) == 0:
            self.finished_ = True

class Select2Activity(Activity):
    def __init__(self, screen):
        Activity.__init__(self, screen)

    def setup_background(self):
        self.background = common.load_image(constants.illustration_016)[0]
        self.instruction_text()

    def instruction_text(self):
        if pygame.font:
            font = pygame.font.SysFont(constants.font_title[0], constants.font_title[1])
            title = unicode("La salud en nuestras playas", 'utf-8')
            text = font.render(title, True, (0, 0, 0))
            textRect = text.get_rect()
            textRect.topleft = (30, 10)
            self.background.blit(text, textRect)

            messages = ["¿Quién está haciendo bien las cosas?",
            "Selecciona las actividades", "correctas en el dibujo."]
            
            y = font.get_linesize()
            font = pygame.font.SysFont(constants.font_default[0], constants.font_default[1])
            font_height = font.get_linesize()

            for message in messages:
                message = unicode(message, 'utf-8')
                text = font.render(message, True, (122, 122, 122))
                textRect = text.get_rect()
                y += font_height 
                textRect.topleft = (30, y)
                self.background.blit(text, textRect)

    def setup(self):
        """Turn off the mouse pointer"""
        pygame.mouse.set_visible( False )
        """change the mouse pointer by a hand"""
        self.button_down = 0
        self.rectList = [ 
                pygame.Rect(236, 235, 71, 39),
                pygame.Rect(238, 326, 84, 162),
                pygame.Rect(410, 273, 88, 77),
                ]
        self.sprites = pygame.sprite.OrderedUpdates()
        self.icons = pygame.sprite.Group()
        self.icons.add([Icons('stop')])
        image_check = image_normal = os.path.join(constants.icons_folder,\
                "check.png")
        self.checkImage, self.checkRect = common.load_image\
          (image_check)
        self.hand = Hand()
        self.sprites.add([self.icons, self.hand])
        pos = pygame.mouse.get_pos()
        self.sprites.draw(self.screen)

    def handle_events(self):
        verify_rect = None
        for event in self.get_event():
            pos = pygame.mouse.get_pos()
            if event.type == QUIT:
                self.quit = True
                return
            elif event.type == MOUSEMOTION:
                    self.hand.update(pos)

            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    self.quit = True
                    return
            elif event.type == MOUSEBUTTONDOWN:
                if pygame.sprite.spritecollideany\
                  (self.hand, self.icons):
                    self.quit = True
                    return
                verify_rect = self.hand.rect.collidelistall(self.rectList)
                if verify_rect:
                    """If the selection is a valid object,
                    delete the object from the list"""
                    objectSelected = self.rectList[verify_rect[0]]
                    del self.rectList[verify_rect[0]]
                    """draw the check image in the center
                    of the rect selected"""
                    self.background.blit(self.checkImage,\
                     (objectSelected.centerx - self.checkRect.centerx\
                     , objectSelected.centery - self.checkRect.centery ))

        self.screen.blit(self.background, (0,0))
        self.sprites.draw(self.screen)
        pygame.display.update()

        if len(self.rectList) == 0:
            self.finished_ = True

class Select3Activity(Activity):
    def __init__(self, screen):
        Activity.__init__(self, screen)

    def setup_background(self):
        self.background = common.load_image(constants.illustration_015)[0]
        self.instruction_text()

    def instruction_text(self):
        if pygame.font:
            font = pygame.font.SysFont(constants.font_title[0], constants.font_title[1])
            title = unicode("Somos diferentes", 'utf-8')
            text = font.render(title, True, (0, 0, 0))
            textRect = text.get_rect()
            textRect.centerx = self.screen.get_rect().centerx
            textRect.centery = 20
            self.background.blit(text, textRect)

            messages = ['En cada uno de las ilustraciones, selecciona según se indica. Ilustración A, el más alto;',
            'ilustración B, la más flaca; ilustración C, el más blanco; ilustración D, el más fuerte.']
            
            y = 252
            font = pygame.font.SysFont(constants.font_default[0], 25)
            font_height = font.get_linesize()

            for message in messages:
                message = unicode(message, 'utf-8')
                text = font.render(message, True, (0, 0, 0))
                textRect = text.get_rect()
                textRect.centerx = self.screen.get_rect().centerx
                y += font_height 
                textRect.centery = y
                self.background.blit(text, textRect)

    def setup(self):
        """Turn off the mouse pointer"""
        pygame.mouse.set_visible( False )
        """change the mouse pointer by a hand"""
        self.button_down = 0
        self.rectList = [ 
                pygame.Rect(160, 62, 70, 195),
                pygame.Rect(595, 59, 49, 154),
                pygame.Rect(141, 339, 59, 199),
                pygame.Rect(472, 317, 69, 257),
                ]
        self.sprites = pygame.sprite.OrderedUpdates()
        self.icons = pygame.sprite.Group()
        self.icons.add([Icons('stop')])
        image_check = image_normal = os.path.join(constants.icons_folder,\
                "check.png")
        self.checkImage, self.checkRect = common.load_image\
          (image_check)
        self.hand = Hand()
        self.sprites.add([self.icons, self.hand])
        pos = pygame.mouse.get_pos()
        self.sprites.draw(self.screen)

    def handle_events(self):
        verify_rect = None
        for event in self.get_event():
            pos = pygame.mouse.get_pos()
            if event.type == QUIT:
                self.quit = True
                return
            elif event.type == MOUSEMOTION:
                    self.hand.update(pos)

            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    self.quit = True
                    return
            elif event.type == MOUSEBUTTONDOWN:
                if pygame.sprite.spritecollideany\
                  (self.hand, self.icons):
                    self.quit = True
                    return
                verify_rect = self.hand.rect.collidelistall(self.rectList)
                if verify_rect:
                    """If the selection is a valid object,
                    delete the object from the list"""
                    objectSelected = self.rectList[verify_rect[0]]
                    del self.rectList[verify_rect[0]]
                    """draw the check image in the center
                    of the rect selected"""
                    self.background.blit(self.checkImage,\
                     (objectSelected.centerx - self.checkRect.centerx,\
                     objectSelected.centery - self.checkRect.centery))

        self.screen.blit(self.background, (0,0))
        self.sprites.draw(self.screen)
        pygame.display.update()

        if len(self.rectList) == 0:
            self.finished_ = True

class Select4Activity(Activity):
    def __init__(self, screen):
        Activity.__init__(self, screen)

    def setup_background(self):
        self.background, self.rect = common.load_image(constants.illustration_026)
        self.instruction_text()

    def instruction_text(self):
        if pygame.font:
            font = pygame.font.SysFont(constants.font_title[0], constants.font_title[1])
            title = unicode("Un desayuno sano", 'utf-8')
            text = font.render(title, True, (0, 0, 0))
            textRect = text.get_rect()
            textRect.centerx = self.screen.get_rect().centerx
            textRect.centery = 20
            self.background.blit(text, textRect)

            messages = ['Haz click en cinco alimentos saludables', 
                'para el desayuno de Ricardo.']
            
            y = 252
            font = pygame.font.SysFont(constants.font_default[0], constants.font_default[1])
            font_height = font.get_linesize()

            for message in messages:
                message = unicode(message, 'utf-8')
                text = font.render(message, True, (0, 0, 0))
                textRect = text.get_rect()
                textRect.centerx = self.screen.get_rect().centerx
                y += font_height 
                textRect.centery = y
                self.background.blit(text, textRect)

    def setup(self):
        """Turn off the mouse pointer"""
        pygame.mouse.set_visible( False )
        """change the mouse pointer by a hand"""
        self.button_down = 0
        self.rectList = [ 
                pygame.Rect(332, 360, 47, 36),
                pygame.Rect(322, 399, 32, 32),
                pygame.Rect(356, 401, 27, 31),
                pygame.Rect(418, 346, 54, 84),
                ]
        self.sprites = pygame.sprite.OrderedUpdates()
        self.icons = pygame.sprite.Group()
        self.icons.add([Icons('stop')])
        self.checked = pygame.sprite.Group()
        self.hand = Hand()
        self.sprites.add([self.icons, self.hand, self.checked])
        pos = pygame.mouse.get_pos()
        self.sprites.draw(self.screen)

    def handle_events(self):
        verify_rect = None
        for event in self.get_event():
            pos = pygame.mouse.get_pos()
            if event.type == QUIT:
                self.quit = True
                return
            elif event.type == MOUSEMOTION:
                    self.hand.update(pos)
            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    self.quit = True
                    return
            elif event.type == MOUSEBUTTONDOWN:
                if pygame.sprite.spritecollideany\
                  (self.hand, self.icons):
                    self.quit = True
                    return
                verify_rect = self.hand.rect.collidelistall(self.rectList)
                if verify_rect:
                    """If the selection is a valid object,
                    delete the object from the list"""
                    objectSelected = self.rectList[verify_rect[0]]
                    del self.rectList[verify_rect[0]]
                    """draw the check image in the center
                    of the rect selected"""
                    self.checked.add(Check(objectSelected.bottomright, 0, (20, 20)))
                    self.sprites.remove(self.checked)
                    self.sprites.add(self.checked)

        self.screen.blit(self.background, (0,0))
        self.sprites.draw(self.screen)
        pygame.display.update()

        if len(self.rectList) == 0:
            self.finished_ = True

