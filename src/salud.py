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
from puzzle import PuzzleActivity, Puzzle2Activity,\
        Puzzle3Activity, Puzzle4Activity
from cooking import Cooking
from healthy import Healthy
from order import OrderActivity, OrderActivity2
from shopping import Shopping
from missing import Missing
from room import Room
from labyrinth import Labyrinth
from riddle import Riddle


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
        MenuItem('missing', Missing, 'dragndrop'), # Act 1
        MenuItem('crazyletter', CrazyLetterActivity, 'dragndrop'),  # Act 2
        MenuItem('fivesenses', SoupActivity, 'soups'), # Act 3
        MenuItem('puzzle1', PuzzleActivity, 'puzzle'), # Act 4-16
        MenuItem('puzzle2', Puzzle2Activity, 'puzzle'), # Act 4-16
        MenuItem('puzzle3', Puzzle3Activity, 'puzzle'), # Act 4-16
        MenuItem('puzzle4', Puzzle4Activity, 'puzzle'), # Act 4-16
        MenuItem('shower', Shower, 'associations'), # Act 5
        MenuItem('healthy', Healthy, 'dragndrop'), # Act 6
        MenuItem('readings2', PoetryActivity, 'readings'), # Act 7
        MenuItem('order1', OrderActivity, 'order'), # Act 8
        MenuItem('health', Labyrinth, 'labyrinth'), # Act 9
        # TODO Act 10
        MenuItem('readings1', PoetryActivity2, 'readings'), # Act 11
        MenuItem('order2', OrderActivity2, 'order'), # Act 12
        # TODO Act 13
        MenuItem('environment', SoupActivity2, 'soups'), # Act 14
        # TODO Act 15
        # TODO Act 16
        MenuItem('room', Room, 'select'), # Act 17
        # TODO Act 18
        # TODO Act 19
        # TODO Act 20
        MenuItem('shopping', Shopping, 'dragndrop'), # Act 21
        # TODO Act 22
        # TODO Act 23
        # TODO Act 24-1
        # TODO Act 24-2
        # TODO Act 24-3
        # TODO Act 24-4
        MenuItem('riddle', Riddle, 'complete'), # Act 25
        MenuItem('cooking', Cooking, 'dragndrop'), # Act 26
        # TODO Act 27
    ]

	MainMenu(screen, items).run()

if __name__ == '__main__': main()
