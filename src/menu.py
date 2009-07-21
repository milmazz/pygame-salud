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
        pygame.mouse.set_pos(100.0, 100.0)

    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.midtop = pos

class MenuActivity(Activity):
    """Main class for elements in the main menu"""
    def __init__(self, screen, items):
        Activity.__init__(self, screen)
        
        self.activities = pygame.sprite.RenderPlain()
        
        x = self.screen.get_width() / 2.0
        #y_center = self.screen.get_height() / 2.0
        # Positions of the activities in the main menu 
        if items:
            y = 100
            for i in range(len(items)):
                items[i].place(x, y)
                self.activities.add(items[i])
                y += 120
            
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
        self.pos = pygame.mouse.get_pos()
        if self.pos != self.mprev:
            self.changed = True
            
    def on_change(self):
        self.Cursor.update()        

        for x in pygame.sprite.spritecollide(self.finger, self.activities, False):
            x.run(self.screen)
            pygame.mouse.set_pos(100.0, 100.0)
            break
        self.activities.draw(self.screen)
        self.Cursor.draw(self.screen)
    
        self.mprev = self.pos
