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

# icons and pictures for main menu
background_filename = os.path.join(data_folder, u"backgrounds", u"background-main.jpg")

process_stop_filename = os.path.join(icons_folder, u"gartoon", u"process-stop.png")

# Activities images
readings_filename = os.path.join(icons_folder, "gartoon", "readings.png")
readings_hover_filename = os.path.join(icons_folder, "gartoon", "readings_hover.png")
associations_filename = os.path.join(icons_folder, "gartoon", "associations.png")
associations_hover_filename = os.path.join(icons_folder, "gartoon", "associations_hover.png")

illustration_008 = os.path.join(data_folder, "backgrounds", "illustration_008.jpg")
illustration_012 = os.path.join(data_folder, "backgrounds", "illustration_012.jpg")

# Shower
illustration_007 = os.path.join(data_folder, "backgrounds", "illustration_007.jpg")

poetry = os.path.join(data_folder, "poetries", "poetry.txt")
poetry2 = os.path.join(data_folder, "poetries", "poetry2.txt")

# soups
illustration_003 = os.path.join(data_folder, "backgrounds", "illustration_003.jpg")
images_soups = os.path.join(data_folder,"soups")
# sound buffer length
mixer_buffersize = 3 * 1024

# Flags for screen display
#screen_flags = FULLSCREEN | NOFRAME
screen_flags = 0
screen_mode = (800, 600)

# Profiling file
profiling_file = os.path.join(data_folder, "salud.profile")
