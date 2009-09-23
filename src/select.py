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


class SelectBase(Activity):
    def __init__(self, screen):
        Activity.__init__(self, screen)
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
        self.tex_info = {
            'title': ["Una boca bien sana", None],
            'instructions' : [["Selecciona aquellos objetos", \
                            "que son necesarios para mantener tu boca sana"], None]
        }

    def setup_background(self):
        self.background, self.rect = common.load_image(constants.illustration_011)

    def instruction_text(self, info):
        if pygame.font:
            title = info['title'][0]
            title_pos = info['title'][1]
            messages = info['instructions'][0]
            font = pygame.font.SysFont(constants.font_title[0], constants.font_title[1])
            text = font.render(title, True, constants.font_title_color)
            # Centering the text
            if title_pos == None:
                title_pos = text.get_rect()
                title_pos.centerx = self.screen.get_rect().centerx
                title_pos.centery = 20
            self.background.blit(text, title_pos)
            
            if info['instructions'][1] == None:
                y = font.get_linesize()
            else:
                y = info['instructions'][1]

            font = pygame.font.SysFont(constants.font_default[0], constants.font_default[1])
            font_height = font.get_linesize()

            for message in messages:
                y += font_height
                message = unicode(message, 'utf-8')
                text = font.render(message, True, constants.font_default_color)
                message_pos = text.get_rect()
                # Centering text instructions
                if info['title'][1] == None:
                    message_pos.centerx = self.screen.get_rect().centerx
                    message_pos.centery = y
                else:
                    message_pos.topleft = (info['title'][1][0], y)
                self.background.blit(text, message_pos)

    def setup(self):
        """Turn off the mouse pointer"""
        pygame.mouse.set_visible( False )
        self.instruction_text(self.tex_info)
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

class SelectActivity(SelectBase):
    def __init__(self, screen):
        SelectBase.__init__(self, screen)


class Select2Activity(SelectBase):
    def __init__(self, screen):
        SelectBase.__init__(self, screen)
        self.rectList = [
                pygame.Rect(236, 235, 71, 39),
                pygame.Rect(238, 326, 84, 162),
                pygame.Rect(410, 273, 88, 77),
                ]
        self.tex_info = {
            'title': ["La salud en nuestras playas", (30, 10)],
            'instructions' : [["¿Quién está haciendo bien las cosas?", \
                            "Selecciona las actividades",
                            "correctas en el dibujo."], None]
        }

    def setup_background(self):
        self.background, self.rect = common.load_image(constants.illustration_016) 


class Select3Activity(SelectBase):
    def __init__(self, screen):
        SelectBase.__init__(self, screen)
        self.rectList = [ 
                pygame.Rect(160, 62, 70, 195),
                pygame.Rect(595, 59, 49, 154),
                pygame.Rect(141, 339, 59, 199),
                pygame.Rect(472, 317, 69, 257),
                ]
        self.tex_info = {
            'title': ["Somos diferentes", None],
            'instructions' : [["En cada uno de las ilustraciones, " + \
                    "selecciona según se indica. Ilustración A, el más alto;",
                    "ilustración B, la más flaca; ilustración C, el" + \
                    "más blanco; ilustración D, el más fuerte."], 252]
        }

    def setup_background(self):
        self.background, self.rect = common.load_image(constants.illustration_015)


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
            text = font.render(title, True, constants.font_title_color)
            textRect = text.get_rect()
            textRect.centerx = self.screen.get_rect().centerx + 145
            textRect.centery = 40
            self.background.blit(text, textRect)

            messages = ['Haz clic en cinco alimentos', 
                'saludables para el desayuno',  
                'de Ricardo.']
            
            y = 500
            font = pygame.font.SysFont(constants.font_default[0], constants.font_default[1])
            font_height = font.get_linesize()

            for message in messages:
                message = unicode(message, 'utf-8')
                text = font.render(message, True, constants.font_default_color)
                textRect = text.get_rect()
                textRect.topleft = (10, y)
                y += font_height 
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
                pygame.Rect(534, 478, 176, 113),
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
