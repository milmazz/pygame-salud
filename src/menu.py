# vim:ts=4:sts=4:et:nowrap:tw=77
# -*- coding: utf-8 -*-

import math

import pygame
from pygame.locals import *

import constants
import common
from activity import Activity

class MenuItem(pygame.sprite.Sprite):
    """Base class for the items in the main menu"""
    def __init__(self, image, activity):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = common.load_image(image)
        self.activity = activity
        self.pos = (-self.rect.width, -self.rect.height)

    def run(self, screen):
        self.activity(screen).run()

    def place(self, x, y):
        self.pos = (x, y)
        self.rect.center = self.pos

class Finger(pygame.sprite.Sprite):
    """This class define the mouse sprite"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) 
        self.image, self.rect = common.load_image(constants.cursor_filename)
        pygame.mouse.set_pos(700.0, 550.0)

    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.midtop = pos

class MenuActivity(Activity):
    """Main class for elements in the main menu"""
    def __init__(self, screen, items):
        Activity.__init__(self, screen)
        
        self.activities = pygame.sprite.RenderPlain()
        
        # Positions of the activities in the main menu 
        if items:
            y = 0
            for i in range(len(items)):
                if i % 2 == 0:
                    x = self.screen.get_width() / 2.0 - 130
                    y += 120
                else:
                    x = self.screen.get_width() / 2.0 + 130
                items[i].place(x, y)
                self.activities.add(items[i])
            
        self.finger = Finger()
        self.Cursor = pygame.sprite.RenderPlain((self.finger))
        
        self.pos = None
        
    #def setup_background(self):
    #    self.background = pygame.image.load(constants.background_filename)
        
    def handle_events(self):
        event = pygame.event.wait()
        if event.type == QUIT:
            self.quit = True
            return
        elif event.type == KEYUP:
            if event.key == K_F4 and KMOD_ALT & event.mod:
                self.quit = True
                return
        elif event.type == MOUSEBUTTONUP:
            for x in pygame.sprite.spritecollide(self.finger, self.activities, False):
                x.run(self.screen)
                pygame.mouse.set_pos(100.0, 100.0)
                break

        self.pos = pygame.mouse.get_pos()
        if self.pos != self.mprev:
            self.changed = True
            
    def on_change(self):
        self.Cursor.update()        

        #for x in pygame.sprite.spritecollide(self.finger, self.activities, False):
        #    x.run(self.screen)
        #    pygame.mouse.set_pos(100.0, 100.0)
        #    break
        self.activities.draw(self.screen)
        self.Cursor.draw(self.screen)
    
        self.mprev = self.pos
