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
from reads import PoetryActivity, PoetryActivity2, VerseActivity, Verse2Activity
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
from labyrinth import Labyrinth, Labyrinth2Activity
from riddle import Riddle1, Riddle2, Riddle3, Riddle4, Riddle5, Riddle6
from select import SelectActivity, Select2Activity,\
        Select3Activity
from careful import CarefulActivity
from painting import PaintActivity, Paint2Activity

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
        MenuItem('readings1', PuzzleActivity, 'puzzle'), # Act 4-16
        MenuItem('beach', Puzzle2Activity, 'puzzle'), # Act 4-16
        MenuItem('shower', Puzzle3Activity, 'puzzle'), # Act 4-16
        MenuItem('cleaning', Puzzle4Activity, 'puzzle'), # Act 4-16
        MenuItem('shower', Shower, 'associations'), # Act 5
        MenuItem('healthy', Healthy, 'dragndrop'), # Act 6
        MenuItem('readings2', PoetryActivity, 'readings'), # Act 7
        MenuItem('order1', OrderActivity, 'order'), # Act 8
        MenuItem('health', Labyrinth, 'labyrinth'), # Act 9
        MenuItem('mouth', SelectActivity, 'select'), # Act 10
        MenuItem('readings1', PoetryActivity2, 'readings'), # Act 11
        MenuItem('order2', OrderActivity2, 'order'), # Act 12
        MenuItem('diff', Select3Activity, 'select'), # Act 13
        MenuItem('environment', SoupActivity2, 'soups'), # Act 14
        # TODO Act 15
        MenuItem('verses', VerseActivity, 'readings'), # Act 16
        MenuItem('verses', Verse2Activity, 'readings'), # Act 16
        MenuItem('room', Room, 'select'), # Act 17
        MenuItem('beach', Select2Activity, 'select'), # Act 18
        MenuItem('warning', CarefulActivity, 'dragndrop'), # Act 19
        # TODO Act 20
        MenuItem('shopping', Shopping, 'dragndrop'), # Act 21
        MenuItem('cleaning', Labyrinth2Activity, 'labyrinth'), #  Act 22
        MenuItem('painting', PaintActivity, 'paint'), #  Act 23
        MenuItem('painting', Paint2Activity, 'paint'), #  Act 23
        MenuItem('riddle', Riddle1, 'complete'), # Act 24-1
        MenuItem('riddle', Riddle2, 'complete'), # Act 24-2
        MenuItem('riddle', Riddle3, 'complete'), # Act 24-3
        MenuItem('riddle', Riddle4, 'complete'), # Act 24-4
        MenuItem('riddle', Riddle5, 'complete'), # Act 24-5
        MenuItem('riddle', Riddle6, 'complete'), # Act 25
        MenuItem('cooking', Cooking, 'dragndrop'), # Act 26
        # TODO Act 27
    ]

	MainMenu(screen, items).run()

if __name__ == '__main__': main()
