# -*- coding: utf-8 -*-

import string

import pygame
from pygame.locals import *

def load_image(path, colorkey=None):
    """Load image resources"""
    try:
        image = pygame.image.load(path)
    except pygame.error, message:
        print "Cannot load image: ", path
        raise SystemExit, message

    if image.get_alpha() is None:
        image = image.convert()
    else:
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
        print 'Cannot load sound: ', path
        raise SystemExit, message

    return sound

def load_file(path):
    try:
        file = open(path, 'r')
        lines = []
        for line in file:
            lines.append(string.rstrip(line))

    except IOError, message:
        print 'Cannot load file: ', path
        raise SystemExit, message

    return lines
