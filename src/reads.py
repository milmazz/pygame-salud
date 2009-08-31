# vim:ts=4:sts=4:et:nowrap:tw=77
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *

import constants
from activity import Activity
from menu import MenuItem, MenuActivity
from icons import Icons
import common

class Finger(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = common.load_image(constants.cursor_filename)

    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.midtop = pos


# Actividad 7
class PoetryActivity(Activity):
    def __init__(self, screen):
        Activity.__init__(self, screen)
        self.CloseButton = pygame.sprite.RenderUpdates(([Icons('stop')]))
        self.finger = Finger()
        self.Cursor = pygame.sprite.RenderUpdates((self.finger))
        self.pos = None
    
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
        self.text()
        self.Cursor.draw(self.screen)
        self.mprev = self.pos

    def setup_background(self):
        self.background = pygame.image.load(constants.illustration_008)

    def text(self):
        messages = common.load_file(constants.poetry)
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
        self.text()


# Actividad 11
class PoetryActivity2(Activity):
    def __init__(self, screen):
        Activity.__init__(self, screen)
        self.CloseButton = pygame.sprite.RenderUpdates(([Icons('stop')]))
        self.finger = Finger()
        self.Cursor = pygame.sprite.RenderUpdates((self.finger))
        self.pos = None
    
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
        self.text()
        self.Cursor.draw(self.screen)
        self.mprev = self.pos

    def setup_background(self):
        self.background = pygame.image.load(constants.illustration_012)
        
    def text(self):
        messages = common.load_file(constants.poetry2)
        
        # Title
        font = pygame.font.SysFont(constants.font_title[0], constants.font_title[1])
        font_height = font.get_linesize()
        y = 10
        
        title = unicode(messages[0], 'utf-8')
        text = font.render(title, True, (0, 0, 0))
        text_pos = (20, 20)
        self.screen.blit(text, text_pos)

        y = 20 + font_height
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
        self.text()
        self.Cursor.draw(self.screen)

class VerseActivity(Activity):
    def __init__(self, screen):
        Activity.__init__(self, screen)
        self.CloseButton = pygame.sprite.RenderUpdates(([Icons('stop')]))
        self.finger = Finger()
        self.Cursor = pygame.sprite.RenderUpdates((self.finger))
        self.pos = None
    
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
        self.text()
        self.Cursor.draw(self.screen)
        self.mprev = self.pos

    def setup_background(self):
        self.background = pygame.image.load(constants.page_21a)
        
    def info_text(self, messages, pos, size=constants.font_default[1]):
        font = pygame.font.SysFont(constants.font_default[0], size)
        font_height = font.get_linesize()
        for message in messages:
            message = unicode(message, 'utf-8')
            text = font.render(message, True, (102, 102, 102))
            text_pos = pos
            self.screen.blit(text, text_pos)
            pos[1] += font_height
            
    def text(self):
        # Title
        font = pygame.font.SysFont(constants.font_title[0], constants.font_title[1])
        font_height = font.get_linesize()
        y = 10
        
        title = "Versos y estribillos populares" 
        text = font.render(title, True, (0, 0, 0))
        text_pos = (20, 20)
        self.screen.blit(text, text_pos)

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
        
        copyright = ['Extraído de "El Folklore en la Alimentación Venezolana" INN (1996).',]

        self.info_text(messages, [20, y])
        self.info_text(mango, [50, 280])
        self.info_text(guavas, [470, 320])
        self.info_text(copyright, [315, 570], 18)

    def setup(self):
        self.CloseButton.draw(self.screen)
        self.text()
        self.Cursor.draw(self.screen)

class Verse2Activity(Activity):
    def __init__(self, screen):
        Activity.__init__(self, screen)
        self.CloseButton = pygame.sprite.RenderUpdates(([Icons('stop')]))
        self.finger = Finger()
        self.Cursor = pygame.sprite.RenderUpdates((self.finger))
        self.pos = None
    
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
        self.text()
        self.Cursor.draw(self.screen)
        self.mprev = self.pos

    def setup_background(self):
        self.background = pygame.image.load(constants.page_21b)
        
    def info_text(self, messages, pos, size=constants.font_default[1]):
        font = pygame.font.SysFont(constants.font_default[0], size)
        font_height = font.get_linesize()
        for message in messages:
            message = unicode(message, 'utf-8')
            text = font.render(message, True, (102, 102, 102))
            text_pos = pos
            self.screen.blit(text, text_pos)
            pos[1] += font_height
            
    def text(self):
        # Title
        font = pygame.font.SysFont(constants.font_title[0], constants.font_title[1])
        font_height = font.get_linesize()
        y = 10
        
        title = "Versos y estribillos populares" 
        text = font.render(title, True, (0, 0, 0))
        text_pos = (20, 20)
        self.screen.blit(text, text_pos)

        y = 20 + font_height

        messages = ['Alimentarse bien es muy importante para la salud.', \
            'Aquí tienes algunos versos y estribillos populares sobre', \
            'los alimentos. Seguro que tus papás los conocen de cuando', \
            'tenía tu edad.', 'Puedes aprenderlos de memoria.']

        soup = ['No se vaya señor cura', \
            'que ya el sancocho va a está', \
            'tiene ñame, tiene ocumo', \
            'tiene batata morá.']

        breakfast = ['Mi mamá se llama arepa', \
            'y mi taita maíz tostao', \
            'miren las horas que son', \
            'y no me he desayunado.']

        copyright = ['Extraído de "El Folklore en la Alimentación Venezolana" INN (1996).',]

        self.info_text(messages, [20, y])
        self.info_text(soup, [187, 200])
        self.info_text(breakfast, [355, 390])
        self.info_text(copyright, [315, 570], 18)

    def setup(self):
        self.CloseButton.draw(self.screen)
        self.text()
        self.Cursor.draw(self.screen)
