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

class ImagePuzzle(Sprite):
    def __init__(self, pos, id, numimage):

        Sprite.__init__(self)
        self.image_path = os.path.join(constants.data_folder, "order",
                                  numimage  + ".png")
        self.image, self.rect = common.load_image(self.image_path)
        self.rect.topleft = pos
        self.id = id #id to compare between images
        self.fix = 0 #fix if the correct image is in the correct position
        self.orig = pos

    def update(self, pos=(0,0)):
        self.rect.topleft = pos


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
        self.rect.x = mover[0] - self.image.get_width() / 2
        self.rect.y = mover[1] - self.image.get_height() / 2
        if self.color == 0:
            self.image = self.normal
        if self.color == 1:
            self.image = self.close


class OrderActivity(Activity):
    def __init__(self, screen):
        Activity.__init__(self, screen)
        self.correct = set()

    def setup_background(self):
        self.background = common.load_image(constants.illustration_009)[0]
        self.instruction_text()

    def instruction_text(self):
        if pygame.font:
            font = pygame.font.SysFont(constants.font_title[0], constants.font_title[1])
            title = unicode("¿Qué va primero?", 'utf-8')
            text = font.render(title, True, constants.font_title_color)
            textRect = text.get_rect()
            textRect.centerx = self.screen.get_rect().centerx
            textRect.centery = 20
            self.background.blit(text, textRect)

            messages = ["Ordena los dibujos y numéralos (1, 2, 3, 4 y 5)", \
                "en cada cuadro siguiendo la secuencia."]
            
            y = font.get_linesize()
            font = pygame.font.SysFont(constants.font_default[0], constants.font_default[1])
            font_height = font.get_linesize()

            for message in messages:
                message = unicode(message, 'utf-8')
                text = font.render(message, True, constants.font_default_color)
                y += font_height 
                textRect.midtop = (300, y) 
                self.background.blit(text, textRect)

    def setup(self):
        """Turn off the mouse pointer"""
        pygame.mouse.set_visible( False )
        """change the mouse pointer by a hand"""
        self.button_down = 0
        self.selection = 0
        self.hand = Hand()
        self.sprites = pygame.sprite.OrderedUpdates()
        self.pictures = pygame.sprite.Group() #picture that can be move
        self.transparent= pygame.sprite.Group() #picture that cann't be move
        self.icons = pygame.sprite.Group()
        self.icons.add([Icons('stop')])
        self.transparent.add([\
          ImagePuzzle((188,522),1,"6"),\
          ImagePuzzle((432,409),2,"6"),\
          ImagePuzzle((694,520),3,"6"),\
          ImagePuzzle((688,312),4,"6"),\
          ImagePuzzle((194,299),5,"6")])
        """add the 4 pictures to the sprite groups"""
        self.pictures.add([\
          ImagePuzzle((310,550),1,"1"),\
          ImagePuzzle((355,550),2,"2"),\
          ImagePuzzle((400,550),3,"3"),\
          ImagePuzzle((445,550),4,"4"),\
          ImagePuzzle((490,550),5,"5")])
        self.sprites.add([self.transparent, self.pictures, self.icons, self.hand])
        pos = pygame.mouse.get_pos()
        self.hand.update(pos)
        self.sprites.draw(self.screen)

    def handle_events(self):
        for event in self.get_event():
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
                    self.sprites.add([self.selection, self.hand])
                self.hand.change_hand() #change de open hand by the close hand
            elif event.type == MOUSEBUTTONUP and self.button_down == 1:
                if self.selection:
                    verify_correct = pygame.sprite.spritecollideany\
                      (self.selection, self.transparent)
                    if verify_correct and verify_correct.id == self.selection.id:
                        self.selection.fix = 1
                        self.selection.rect = verify_correct.rect
                        self.correct.add(self.selection)
                        check = self.selection.rect.center
                        self.sprites.add(Check(check, 0, (20, 20)))
                        self.hand.kill()
                        self.sprites.add([self.hand])
                    else:
                        self.selection.update(self.selection.orig)
                self.button_down = 0
                self.selection = 0
                self.hand.change_hand() #change the close hand by the open hand
            elif event.type == MOUSEMOTION:
                if self.selection and self.selection.fix == 0\
                  and self.button_down == 1:   
                    self.selection.update(pos)
            self.hand.update(pos)
            self.screen.blit(self.background, (0,0))
            self.sprites.draw(self.screen)
            """update all the screen"""
            pygame.display.update()

            if len(self.correct) == 5:
                self.finished_ = True


class OrderActivity2(Activity):
    def __init__(self, screen):
        Activity.__init__(self, screen)
        self.correct = set()

    def setup_background(self):
        self.background = common.load_image(constants.illustration_013)[0]
        self.instruction_text()

    def instruction_text(self):
        if pygame.font:
            font = pygame.font.SysFont(constants.font_title[0], constants.font_title[1])
            title = unicode("Nuestro cuerpo cambia cuando crecemos", 'utf-8')
            text = font.render(title, True, constants.font_title_color)
            textRect = text.get_rect()
            textRect.centerx = self.screen.get_rect().centerx
            textRect.centery = 20
            self.background.blit(text, textRect)

            messages = ["Cuando eras un bebé, tomabas tetero y usabas pañal.",
            "Eras chiquito, cada año creces un poco y te vas",
            "haciendo más alto. Ordena del más",
            "pequeño al más grande, arrastra",
            "el número (1, 2, 3 y 4) al", "círculo correspondiente."]
            
            y = font.get_linesize()
            font = pygame.font.SysFont(constants.font_default[0], constants.font_default[1])
            font_height = font.get_linesize()

            for message in messages:
                message = unicode(message, 'utf-8')
                text = font.render(message, True, constants.font_default_color)
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
        self.selection = 0
        self.hand = Hand()
        self.sprites = pygame.sprite.OrderedUpdates()
        self.pictures = pygame.sprite.Group() #picture that can be move
        self.transparent= pygame.sprite.Group() #picture that cann't be move
        self.icons = pygame.sprite.Group()
        self.icons.add([Icons('stop')])
        self.transparent.add([\
          ImagePuzzle((690,547),1,"7"),\
          ImagePuzzle((204,285),2,"7"),\
          ImagePuzzle((613,284),3,"7"),\
          ImagePuzzle((385,542),4,"7")])
        """add the 4 pictures to the sprite groups"""
        self.pictures.add([\
          ImagePuzzle((100,500),1,"1"),\
          ImagePuzzle((145,500),2,"2"),\
          ImagePuzzle((100,540),3,"3"),\
          ImagePuzzle((145,540),4,"4")])
        self.sprites.add([self.transparent, self.pictures, self.icons, self.hand])
        pos = pygame.mouse.get_pos()
        self.hand.update(pos)
        self.sprites.draw(self.screen)

    def handle_events(self):
            for event in self.get_event():
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
                        self.sprites.add([self.selection, self.hand])
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
                            self.correct.add(self.selection)
                            check = self.selection.rect.center
                            self.sprites.add(Check(check, 0, (20, 20)))
                            self.hand.kill()
                            self.sprites.add([self.hand])
                        else:
                            self.selection.update(self.selection.orig)
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

            if len(self.correct) == 4:
                self.finished_ = True
