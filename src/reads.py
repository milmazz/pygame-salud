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
        font = pygame.font.SysFont("dejavusans", 32)
        font_height = font.get_linesize()
        y = 20

        title = unicode(messages[0], 'utf-8')
        text = font.render(title, True, (0, 0, 0))
        text_pos = (20, 20)
        self.screen.blit(text, text_pos)

        y = 35 + font_height
        font = pygame.font.SysFont("dejavusans", 28)
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
        font = pygame.font.SysFont("dejavusans", 28)
        font_height = font.get_linesize()
        y = 10
        
        title = unicode(messages[0], 'utf-8')
        text = font.render(title, True, (0, 0, 0))
        text_pos = (20, 20)
        self.screen.blit(text, text_pos)

        y = 20 + font_height
        font = pygame.font.SysFont("dejavusans", 24)
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
