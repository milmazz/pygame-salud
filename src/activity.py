import os, sys
import pygame

import common
import constants

class Activity:
    def __init__(self, screen):        
        self.screen = screen
        
        #self.background = pygame.Surface(self.screen.get_size())
        #self.background = self.background.convert()
        #self.setup_background()
        self.background = pygame.image.load(constants.background_filename)
        
        self.center = self.background.get_rect().center
        
        self.clock = pygame.time.Clock()
        self.quit = False
        self.changed = False
        self.mprev = None
        
    def setup_background(self):
        pass
        
    def load_image(self, name, colorkey=None):
        return common.load_image(name, colorkey)
        
    def load_sound(self, name):
        return common.load_sound(name)
    
    def run(self):
        self.screen.blit(self.background, (0,0))
        self.setup()
        pygame.display.flip()
        while True:
            self.handle_events()
            if self.quit:
                break
            if self.changed:
                self.screen.blit(self.background, (0, 0))
                self.on_change()
                pygame.display.flip()
            self.changed = False
    
    def setup(self):
        pass 
        
    def handle_events(self):
        pass 
        
    def on_change(self):
        pass 
