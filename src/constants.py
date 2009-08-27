# -*- coding: utf-8 -*-

import os

import pygame
from pygame.locals import *

# canaima-salud version
version = "0.1"

# Game folders
data_folder = os.path.join(u"..", "data")
icons_folder = os.path.join(data_folder, u"icons")

# If OS is Linux/Unix
if (os.name == "posix"):
	home_dir = os.path.join(os.getenv('HOME'), u".canaima-salud")
else:
	home_dir = u".."

folder_log = os.path.join(home_dir, u"log")
log_file = os.path.join(folder_log, u"canaima-salud.log")

# cursors
cursor_filename = os.path.join(data_folder, u"cursors", u"pointer.png")

# Fonts
font_title = ("dejavusans", 40)
font_default = ("dejavusans", 20)

# icons and pictures for main menu
background_filename = os.path.join(data_folder, u"backgrounds", u"background-main.jpg")

process_stop_filename = os.path.join(icons_folder, u"gartoon", u"process-stop.png")

# Activities images
readings_filename = os.path.join(icons_folder, "gartoon", "readings_hover.png")
readings_hover_filename = os.path.join(icons_folder, "gartoon", "readings_hover.png")
associations_filename = os.path.join(icons_folder, "gartoon", "associations_hover.png")
associations_hover_filename = os.path.join(icons_folder, "gartoon", "associations_hover.png")

illustration_008 = os.path.join(data_folder, "backgrounds", "illustration_008.jpg")
illustration_012 = os.path.join(data_folder, "backgrounds", "illustration_012.jpg")

# Order1
illustration_009 = os.path.join(data_folder, "backgrounds", "illustration_009.jpg")

# Order2
illustration_013 = os.path.join(data_folder, "backgrounds", "illustration_013.jpg")

# Shower
illustration_007 = os.path.join(data_folder, "backgrounds", "illustration_007.jpg")

# Meals
illustration_023 = os.path.join(data_folder, "backgrounds", "illustration_023.jpg")

# Cooking
illustration_024 = os.path.join(data_folder, "backgrounds", "illustration_024.jpg")

# Healthy
illustration_005 = os.path.join(data_folder, "backgrounds", "illustration_005.jpg")
illustration_006 = os.path.join(data_folder, "backgrounds", "illustration_006.jpg")

# Shopping
illustration_025 = os.path.join(data_folder, "backgrounds", "illustration_025.png")

# Missing
illustration_001 = os.path.join(data_folder, "backgrounds", "illustration_001.jpg")

# Verses
page_21a = os.path.join(data_folder, "backgrounds", "page_21a.png")
page_21b = os.path.join(data_folder, "backgrounds", "page_21b.png")

# Poetries
poetry = os.path.join(data_folder, "poetries", "poetry.txt")
poetry2 = os.path.join(data_folder, "poetries", "poetry2.txt")

# Soups
illustration_003 = os.path.join(data_folder, "backgrounds", "illustration_003.jpg")
illustration_017 = os.path.join(data_folder, "backgrounds", "illustration_017.jpg")

# Crazy letter
illustration_002 = os.path.join(data_folder, "backgrounds", "illustration_002.jpg")

# Puzzle
illustration_puzzle = os.path.join(data_folder, "backgrounds", "illustration_012_b.jpg")
images_puzzle = os.path.join(data_folder,"puzzle")

# Labyrinth
images_labyrinth = os.path.join(data_folder,"labyrinth")
illustration_010 = os.path.join(data_folder, "backgrounds", "illustration_010.png")
illustration_022 = os.path.join(data_folder, "backgrounds", "illustration_022.jpg")

# Select Activity
illustration_011 = os.path.join(data_folder, "backgrounds", "illustration_011.jpg")
illustration_015 = os.path.join(data_folder, "backgrounds", "illustration_015.jpg")
illustration_016 = os.path.join(data_folder, "backgrounds", "illustration_016.jpg")

# Careful
illustration_018 = os.path.join(data_folder, "backgrounds", "illustration_018.jpg")
illustration_019 = os.path.join(data_folder, "backgrounds", "illustration_019.jpg")

# Painting
painting_folder = os.path.join(data_folder, "painting")
bricklayer = os.path.join(painting_folder, "bricklayer.png")
nurse = os.path.join(painting_folder, "nurse.png")
police = os.path.join(painting_folder, "police.png")
streetsweeper = os.path.join(painting_folder, "streetsweeper.png")
barber = os.path.join(painting_folder, "barber.png")
doctor = os.path.join(painting_folder, "doctor.png")
firefighter = os.path.join(painting_folder, "firefighter.png")
teacher = os.path.join(painting_folder, "teacher.png")
mechanic = os.path.join(painting_folder, "mechanic.png")

# sound buffer length
mixer_buffersize = 3 * 1024

# Flags for screen display
screen_flags = FULLSCREEN | NOFRAME
#screen_flags = 0
screen_mode = (800, 600)

# Profiling file
profiling_file = os.path.join(data_folder, "salud.profile")

snd_click = os.path.join(data_folder, "snd", "click.ogg")
snd_congratulation = os.path.join(data_folder, "snd", "congratulation.ogg")
