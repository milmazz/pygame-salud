# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *

import constants
from activity import Activity
from menu import MenuItem, MenuActivity
import common

# Actividad 7
class PoetryActivity(Activity):
    def __init__(self, screen):
        Activity.__init__(self, screen)
    
    def handle_events(self):
        event = pygame.event.wait()
        if event.type == QUIT:
            self.quit = True
            return
        elif event.type == KEYUP:
            self.changed = False
            if event.key == K_ESCAPE:
                self.quit = True
                return
    def setup_background(self):
        self.background = pygame.image.load(constants.illustration_008)

    def setup(self):
        font = pygame.font.SysFont("dejavusans", 32)
        font_height = font.get_linesize()
        messages = common.load_file(constants.poetry)
        y = font_height

        for message in messages:
            message = unicode(message, 'utf-8')
            text = font.render(message, True, (102, 102, 102))
            text_pos = (50, y)
            y += font_height
            self.screen.blit(text, text_pos)

# Actividad 11
class PoetryActivity2(Activity):
    def __init__(self, screen):
        Activity.__init__(self, screen)
    
    def handle_events(self):
        event = pygame.event.wait()
        if event.type == QUIT:
            self.quit = True
            return
        elif event.type == KEYUP:
            self.changed = False
            if event.key == K_ESCAPE:
                self.quit = True
                return
 
    def setup_background(self):
        self.background = pygame.image.load(constants.illustration_012)
        
    def setup(self):
        font = pygame.font.SysFont("dejavusans", 24)
        font_height = font.get_linesize()
        messages = common.load_file(constants.poetry2)
        y = font_height

        for message in messages:
            message = unicode(message, 'utf-8')
            text = font.render(message, True, (102, 102, 102))
            text_pos = (50, y)
            y += font_height
            self.screen.blit(text, text_pos)
