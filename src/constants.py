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
draw_freehand = os.path.join(constants.data_folder, "cursors", \
    "gartoon", "draw-freehand.png")

# Fonts
font_title = ("dejavusans", 40)
font_default = ("dejavusans", 30)

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
illustration_026 = os.path.join(data_folder, "backgrounds", "illustration_026.jpg")

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

# Riddle
illustration_029a = os.path.join(data_folder, "backgrounds", 'illustration_029a.png')
illustration_029b = os.path.join(data_folder, "backgrounds", 'illustration_029b.png')
illustration_030a = os.path.join(data_folder, "backgrounds", 'illustration_030a.png')
illustration_030b = os.path.join(data_folder, "backgrounds", 'illustration_030b.png')
illustration_031a = os.path.join(data_folder, "backgrounds", 'illustration_031a.png')
illustration_031b = os.path.join(data_folder, "backgrounds", 'illustration_031b.png')

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

# Colors
rgb_colors = { "aliceblue": (240, 248, 255),
    "antiquewhite": (250, 235, 215),
    "aqua": (0, 255, 255),
    "aquamarine": (127, 255, 212),
    "azure": (240, 255, 255),
    "beige": (245, 245, 220),
    "bisque": (255, 228, 196),
    "black": (0, 0, 0),
    "blanchedalmond": (255, 235, 205),
    "blue": (0, 0, 255),
    "blueviolet": (138, 43, 226),
    "brown": (165, 42, 42),
    "burlywood": (222, 184, 135),
    "cadetblue": (95, 158, 160),
    "chartreuse": (127, 255, 0),
    "chocolate": (210, 105, 30),
    "coral": (255, 127, 80),
    "cornflowerblue": (100, 149, 237),
    "cornsilk": (255, 248, 220),
    "crimson": (220, 20, 60),
    "cyan": (0, 255, 255),
    "darkblue": (0, 0, 139),
    "darkcyan": (0, 139, 139),
    "darkgoldenrod": (184, 134, 11),
    "darkgray": (169, 169, 169),
    "darkgreen": (0, 100, 0),
    "darkgrey": (169, 169, 169),
    "darkkhaki": (189, 183, 107),
    "darkmagenta": (139, 0, 139),
    "darkolivegreen": (85, 107, 47),
    "darkorange": (255, 140, 0),
    "darkorchid": (153, 50, 204),
    "darkred": (139, 0, 0),
    "darksalmon": (233, 150, 122),
    "darkseagreen": (143, 188, 143),
    "darkslateblue": (72, 61, 139),
    "darkslategray": (47, 79, 79),
    "darkslategrey": (47, 79, 79),
    "darkturquoise": (0, 206, 209),
    "darkviolet": (148, 0, 211),
    "deeppink": (255, 20, 147),
    "deepskyblue": (0, 191, 255),
    "dimgray": (105, 105, 105),
    "dimgrey": (105, 105, 105),
    "dodgerblue": (30, 144, 255),
    "firebrick": (178, 34, 34),
    "floralwhite": (255, 250, 240),
    "forestgreen": (34, 139, 34),
    "fuchsia": (255, 0, 255),
    "gainsboro": (220, 220, 220),
    "ghostwhite": (248, 248, 255),
    "gold": (255, 215, 0),
    "goldenrod": (218, 165, 32),
    "gray": (128, 128, 128),
    "grey": (128, 128, 128),
    "green": (0, 128, 0),
    "greenyellow": (173, 255, 47),
    "honeydew": (240, 255, 240),
    "hotpink": (255, 105, 180),
    "indianred": (205, 92, 92),
    "indigo": (75, 0, 130),
    "ivory": (255, 255, 240),
    "khaki": (240, 230, 140),
    "lavender": (230, 230, 250),
    "lavenderblush": (255, 240, 245),
    "lawngreen": (124, 252, 0),
    "lemonchiffon": (255, 250, 205),
    "lightblue": (173, 216, 230),
    "lightcoral": (240, 128, 128),
    "lightcyan": (224, 255, 255),
    "lightgoldenrodyellow": (250, 250, 210),
    "lightgray": (211, 211, 211),
    "lightgreen": (144, 238, 144),
    "lightgrey": (211, 211, 211),
    "lightpink": (255, 182, 193),
    "lightsalmon": (255, 160, 122),
    "lightseagreen": (32, 178, 170),
    "lightskyblue": (135, 206, 250),
    "lightslategray": (119, 136, 153),
    "lightslategrey": (119, 136, 153),
    "lightsteelblue": (176, 196, 222),
    "lightyellow": (255, 255, 224),
    "lime": (0, 255, 0),
    "limegreen": (50, 205, 50),
    "linen": (250, 240, 230),
    "magenta": (255, 0, 255),
    "maroon": (128, 0, 0),
    "mediumaquamarine": (102, 205, 170),
    "mediumblue": (0, 0, 205),
    "mediumorchid": (186, 85, 211),
    "mediumpurple": (147, 112, 219),
    "mediumseagreen": (60, 179, 113),
    "mediumslateblue": (123, 104, 238),
    "mediumspringgreen": (0, 250, 154),
    "mediumturquoise": (72, 209, 204),
    "mediumvioletred": (199, 21, 133),
    "midnightblue": (25, 25, 112),
    "mintcream": (245, 255, 250),
    "mistyrose": (255, 228, 225),
    "moccasin": (255, 228, 181),
    "navajowhite": (255, 222, 173),
    "navy": (0, 0, 128),
    "oldlace": (253, 245, 230),
    "olive": (128, 128, 0),
    "olivedrab": (107, 142, 35),
    "orange": (255, 165, 0),
    "orangered": (255, 69, 0),
    "orchid": (218, 112, 214),
    "palegoldenrod": (238, 232, 170),
    "palegreen": (152, 251, 152),
    "paleturquoise": (175, 238, 238),
    "palevioletred": (219, 112, 147),
    "papayawhip": (255, 239, 213),
    "peachpuff": (255, 218, 185),
    "peru": (205, 133, 63),
    "pink": (255, 192, 203),
    "plum": (221, 160, 221),
    "powderblue": (176, 224, 230),
    "purple": (128, 0, 128),
    "red": (255, 0, 0),
    "rosybrown": (188, 143, 143),
    "royalblue": (65, 105, 225),
    "saddlebrown": (139, 69, 19),
    "salmon": (250, 128, 114),
    "sandybrown": (244, 164, 96),
    "seagreen": (46, 139, 87),
    "seashell": (255, 245, 238),
    "sienna": (160, 82, 45),
    "silver": (192, 192, 192),
    "skyblue": (135, 206, 235),
    "slateblue": (106, 90, 205),
    "slategray": (112, 128, 144),
    "slategrey": (112, 128, 144),
    "snow": (255, 250, 250),
    "springgreen": (0, 255, 127),
    "steelblue": (70, 130, 180),
    "tan": (210, 180, 140),
    "teal": (0, 128, 128),
    "thistle": (216, 191, 216),
    "tomato": (255, 99, 71),
    "turquoise": (64, 224, 208),
    "violet": (238, 130, 238),
    "wheat": (245, 222, 179),
    "white": (255, 255, 255),
    "whitesmoke": (245, 245, 245),
    "yellow": (255, 255, 0),
    "yellowgreen": (154, 205, 50)
    }
