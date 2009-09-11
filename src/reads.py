# vim:ts=4:sts=4:et:nowrap:tw=77
# -*- coding: utf-8 -*-

import os
import pygame
from pygame.locals import *

import constants
from activity import Activity
from menu import MenuItem, MenuActivity
from icons import Icons, Navigation
import common

class Finger(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = common.load_image(constants.cursor_filename)

    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.midtop = pos


class PoetryBase(Activity):
    def __init__(self, screen):
        Activity.__init__(self, screen)
        self.CloseButton = pygame.sprite.RenderUpdates(([Icons('stop')]))
        self.finger = Finger()
        self.Cursor = pygame.sprite.RenderUpdates((self.finger))
        self.pos = None
        self.messages_filename = constants.poetry
    
    def handle_events(self):
        for event in [pygame.event.wait()] + pygame.event.get():
            if event.type == QUIT:
                self.quit = True
                return
            elif event.type == KEYUP:
                self.changed = False
                if event.key == K_ESCAPE:
                    self.quit = True
                    return
            elif event.type == MOUSEBUTTONDOWN:
                if pygame.sprite.spritecollideany(self.finger, \
                        self.CloseButton):
                    self.quit = True
                    return
        self.pos = pygame.mouse.get_pos()
        if self.pos != self.mprev:
            self.changed = True

    def on_change(self):
        self.Cursor.update()
        self.CloseButton.draw(self.screen)
        self.text(self.messages_filename)
        self.Cursor.draw(self.screen)
        self.mprev = self.pos

    def setup_background(self):
        self.background = pygame.image.load(constants.illustration_008)

    def text(self, info):
        messages = common.load_file(info)
        # Title
        font = pygame.font.SysFont(constants.font_title[0], constants.font_title[1])
        font_height = font.get_linesize()
        y = 20

        title = unicode(messages[0], 'utf-8')
        text = font.render(title, True, (0, 0, 0))
        text_pos = (20, 20)
        self.screen.blit(text, text_pos)

        y = 35 + font_height
        font = pygame.font.SysFont(constants.font_default[0], constants.font_default[1])
        font_height = font.get_linesize()

        for message in messages[1:]:
            message = unicode(message, 'utf-8')
            text = font.render(message, True, (102, 102, 102))
            text_pos = (20, y)
            y += font_height
            self.screen.blit(text, text_pos)

    def setup(self):
        self.CloseButton.draw(self.screen)
        self.Cursor.draw(self.screen)
        self.text(self.messages_filename)


class PoetryActivity(PoetryBase):
    def __init__(self, screen):
        PoetryBase.__init__(self, screen)


class PoetryActivity2(PoetryBase):
    def __init__(self, screen):
        PoetryBase.__init__(self, screen)
        self.messages_filename = constants.poetry2

    def setup_background(self):
        self.background = pygame.image.load(constants.illustration_012)
        

class VerseActivity(Activity):
    def __init__(self, screen):
        Activity.__init__(self, screen)
        self.CloseButton = pygame.sprite.RenderUpdates(([Icons('stop')]))
        self.finger = Finger()
        self.Cursor = pygame.sprite.RenderUpdates((self.finger))
        self.change = pygame.sprite.Group([Navigation()]) #load next and prev buttons
        self.pos = None
        self.sprites = pygame.sprite.OrderedUpdates()
        self.sprites.add([self.CloseButton, self.change, self.Cursor])
    
    def handle_events(self):
        for event in [pygame.event.wait()] + pygame.event.get():
            if event.type == QUIT:
                self.quit = True
                return
            elif event.type == KEYUP:
                self.changed = False
                if event.key == K_ESCAPE:
                    self.quit = True
                    return
            elif event.type == MOUSEBUTTONDOWN:
                if pygame.sprite.spritecollideany(self.finger, \
                        self.CloseButton):
                    self.quit = True
                    return
                if pygame.sprite.spritecollideany(self.finger, self.change):
                    self.sprites.remove([self.change, self.finger])
                    self.update_background()
                    self.change.update()
                    self.sprites.add([self.change, self.finger])
                    self.sprites.draw(self.screen)
                    self.screen.blit(self.background, (0, 0))
                    pygame.display.flip()

        self.pos = pygame.mouse.get_pos()

        if self.pos != self.mprev:
            self.changed = True

    def on_change(self):
        self.Cursor.update()
        self.sprites.draw(self.screen)
        self.mprev = self.pos

    def setup_background(self):
        self.bg1 = pygame.image.load(constants.page_21a)
        self.bg2 = pygame.image.load(constants.page_21b)
        self.background = self.bg1

    def update_background(self):
        if self.background == self.bg1:
            self.background = self.bg2
        else:
            self.background = self.bg1
        
    def info_text(self, messages, pos, size=constants.font_default[1], bg=None):
        font = pygame.font.SysFont(constants.font_default[0], size)
        font_height = font.get_linesize()

        for message in messages:
            message = unicode(message, 'utf-8')
            text = font.render(message, True, (0, 0, 0))
            text_pos = pos
            bg.blit(text, text_pos)
            pos[1] += font_height
            
    def text(self):
        # Title
        font = pygame.font.SysFont(constants.font_title[0], constants.font_title[1])
        font_height = font.get_linesize()
        y = 10
        
        title = "Versos y estribillos populares" 
        text = font.render(title, True, (0, 0, 0))
        text_pos = (20, 20)
        self.bg1.blit(text, text_pos)
        self.bg2.blit(text, text_pos)

        y = 20 + font_height

        messages = ['Alimentarse bien es muy importante para la salud.', \
            'Aquí tienes algunos versos y estribillos populares sobre', \
            'los alimentos. Seguro que tus papás los conocen de cuando', \
            'tenía tu edad.', 'Puedes aprenderlos de memoria.']

        mango = ['El manguito de hilacha', \
            'el manguito de bocao', \
            'se le quita la concha', \
            'y se  come pelao.']

        guavas = ['Una guayaba madura', \
            'le dijo a la que era verde', \
            'el que siembra en tierra ajena', \
            'hasta la semilla pierde.']
        
        soup = ['No se vaya señor cura', \
            'que ya el sancocho va a está', \
            'tiene ñame, tiene ocumo', \
            'tiene batata morá.']

        breakfast = ['Mi mamá se llama arepa', \
            'y mi taita maíz tostao', \
            'miren las horas que son', \
            'y no me he desayunado.']

        copyright = ['Extraído de "El Folklore en la Alimentación Venezolana" INN (1996).',]

        self.info_text(messages, [20, y], bg=self.bg1)
        self.info_text(mango, [50, 280], bg=self.bg1)
        self.info_text(guavas, [470, 320], bg=self.bg1)
        self.info_text(copyright, [10, 570], size=18, bg=self.bg1)
        # Background 2
        self.info_text(messages, [20, y], bg=self.bg2)
        self.info_text(soup, [187, 200], bg=self.bg2)
        self.info_text(breakfast, [355, 390], bg=self.bg2)
        self.info_text(copyright, [315, 570], size=18, bg=self.bg2)

    def setup(self):
        self.text()
        self.sprites.draw(self.screen)
