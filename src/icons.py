import pygame
from pygame.locals import *
from pygame.sprite import Sprite
import constants

class Icons(Sprite):
   def __init__(self, id):
       Sprite.__init__(self)
       self.image = pygame.image.load(constants.icons_folder+'/gartoon/process-stop.png')
       self.rect = self.image.get_rect()
       x = constants.screen_mode[0] - self.image.get_width()
       y = 0
       self.rect.topleft = [x,y]
       self.id = id

