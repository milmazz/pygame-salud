# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

import os.path
import math

import pygame
from pygame.locals import *
import cProfile as profile

import constants
import common
from menu import MenuItem, MainMenu
from reads import PoetryActivity, PoetryActivity2
from links import Shower
from soups import SoupActivity, SoupActivity2
from crazyletter import CrazyLetterActivity
from puzzle import PuzzleActivity
from cooking import Cooking

def main():
	# Mixer pre init
	pygame.mixer.pre_init(44100, -16, 2, constants.mixer_buffersize)

	pygame.init()

	# Bigger dimensions for the screen, fullscreen mode
	#screen_mode = pygame.display.list_modes(0, constants.screen_flags)[0]
	screen = pygame.display.set_mode(constants.screen_mode, constants.screen_flags, 32)

	pygame.display.set_caption('Salud')

	# TODO: Compile our own transparent cursor because this implementation is slow.
	pygame.mouse.set_visible(False)

	items = [
        MenuItem('cletter', CrazyLetterActivity, 'dragndrop'), 
        MenuItem('soup1', SoupActivity, 'soups'), 
        MenuItem('puzzle', PuzzleActivity, 'puzzle'), 
        MenuItem('shower', Shower, 'associations'), 
        MenuItem('poetry1', PoetryActivity, 'readings'), 
        MenuItem('poetry2', PoetryActivity2, 'readings'), 
        MenuItem('soup2', SoupActivity2, 'soups'), 
        MenuItem('cooking', Cooking, 'dragndrop'), 
    ]

	MainMenu(screen, items).run()

if __name__ == '__main__': main()
