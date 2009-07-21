# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

import os.path
import math

import pygame
from pygame.locals import *

import constants
import common
from menu import MenuItem, MenuActivity
from reads import PoetryActivity, PoetryActivity2

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
        MenuItem(constants.readings_filename , PoetryActivity), 
        MenuItem(constants.associations_filename, PoetryActivity2), 
    ]

	MenuActivity(screen, items).run()

if __name__ == '__main__': main()
