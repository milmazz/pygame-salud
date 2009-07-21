# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *

def load_image(path, colorkey=None):
	"""Load image resources"""
	try:
		image = pygame.image.load(path)
	except pygame.error, message:
		print "Cannot load image: ", path
		raise SystemExit, message

	image = image.convert_alpha()

	return image, image.get_rect()

def load_sound(path):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer:
        return NoneSound()
    try:
        sound = pygame.mixer.Sound(path)
    except pygame.error, message:
        print 'Cannot load sound:', path
        raise SystemExit, message
    return sound
