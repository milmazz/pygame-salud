# vim:ts=4:sts=4:et:nowrap:tw=77
# -*- coding: utf-8 -*-

import os
import pygame
from pygame.locals import *

import constants
import common
from activity import Activity
from icons import Icons

class Finger(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        path = os.path.join(u"..", "data", "icons", "gartoon", "draw-brush.png") 
        self.image, self.rect = common.load_image(path)

    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.bottomleft = (pos[0] - 10, pos[1] + 10)

class PaintBase(Activity):
    def __init__(self, screen):
        Activity.__init__(self, screen)
        self.close_button = pygame.sprite.RenderUpdates(([Icons('stop')]))
        self.finger = Finger()
        self.cursor = pygame.sprite.RenderUpdates((self.finger))
        self.pos = None
        self.line_start = (0, 0)
        self.draw_color = (0, 0, 0)
        self.line_width = 3
        self.line_end = None
        self.text()
        self.transparent = pygame.Rect(297, 96, 400, 408)
        # Color palette
        self.palette = {}
        self.mk_palette(constants.rgb_colors)
        # Thickness
        self.thickness = {}
        self.mk_thickness()

    def mk_thickness(self):
        options = (5, 10, 15, 20)
        pos = [0, 215]
        for option in options:
            pos[0] += option + 25
            self.thickness[option] = pygame.draw.circle(self.background, (0, 0, 0), pos, option)
    
    def mk_palette(self, colors):
        pos = (20, 285)
        square = (20, 20)
        count = 0
        for key,color in colors.iteritems():
            x = pos[0] + square[0] * (count % 11)
            y = pos[1] + square[1] * (count / 11)
            self.palette[key] = pygame.draw.rect(self.background, color, ((x, y), square))
            count += 1

    def handle_events(self):
        for event in [pygame.event.wait()] + pygame.event.get():
            if event.type == QUIT:
                self.quit = True
                return
            elif event.type == pygame.MOUSEMOTION:
                self.line_end = pygame.mouse.get_pos()
                if pygame.mouse.get_pressed() == (1, 0, 0) and self.transparent.collidepoint(self.line_end):
                    pygame.draw.line(self.background, self.draw_color, self.line_start, self.line_end, self.line_width)
                self.line_start = self.line_end
            elif event.type == MOUSEBUTTONDOWN:
                if pygame.sprite.spritecollideany(self.finger, self.close_button):
                    self.quit = True
                    return
                else:
                    for key,rect in self.palette.iteritems():
                        if rect.collidepoint(self.line_end):
                            self.draw_color = constants.rgb_colors[key]
                    else:
                        for key,rect in self.thickness.iteritems():
                            if rect.collidepoint(self.line_end):
                                self.line_width = key
            elif event.type == KEYUP:
                self.changed = False
                if event.key == K_ESCAPE:
                    self.quit = True
                    return
        self.pos = pygame.mouse.get_pos()
        if self.pos != self.mprev:
            self.changed = True

    def on_change(self):
        self.cursor.update()
        self.close_button.draw(self.screen)
        self.cursor.draw(self.screen)
        self.mprev = self.pos

    def text(self):
        # Title
        font = pygame.font.SysFont(constants.font_title[0], constants.font_title[1])
        font_height = font.get_linesize()
        x, y = 20, 10

        title = unicode("La salud de nuestra comunidad", 'utf-8')
        text = font.render(title, True, constants.font_title_color, (255, 255, 255))
        text_pos = (x, y)
        self.background.blit(text, text_pos)

        messages = ['Alguna de estas personas', \
            'trabajan para mantener', \
            'la salud de tu comunidad.', \
            'Diviértete coloreándolos.']

        y += 1.5 * font_height
        font = pygame.font.SysFont(constants.font_default[0], constants.font_default[1])
        font_height = font.get_linesize()

        for message in messages:
            message = unicode(message, 'utf-8')
            text = font.render(message, True, constants.font_default_color, (255, 255, 255))
            text_pos = (x, y)
            self.background.blit(text, text_pos)
            y += font_height

        # Tools
        palette_text = unicode("Paleta de colores", 'utf-8')
        text = font.render(palette_text, True, constants.font_default_color, (255, 255, 255))
        text_pos = (x, 250)
        self.background.blit(text, text_pos)

        pincel_text = unicode("Grosor del pincel", 'utf-8')
        text = font.render(pincel_text, True, constants.font_default_color, (255, 255, 255)) 
        text_pos = (x, 170)
        self.background.blit(text, text_pos)


    def setup(self):
        pygame.mouse.set_visible(False)
        self.close_button.draw(self.screen)
        self.cursor.draw(self.screen)

class PaintBrickLayer(PaintBase):
    def __init__(self, screen):
        PaintBase.__init__(self, screen)
        self.transparent = pygame.Rect(356, 156, 400, 410)

    def setup_background(self):
        self.background, rect = common.load_image(constants.bricklayer)

class PaintNurse(PaintBase):
    def __init__(self, screen):
        PaintBase.__init__(self, screen)
        self.transparent = pygame.Rect(356, 156, 400, 423)

    def setup_background(self):
        self.background, rect = common.load_image(constants.nurse)

class PaintPolice(PaintBase):
    def __init__(self, screen):
        PaintBase.__init__(self, screen)
        self.transparent = pygame.Rect(356, 156, 400, 415)

    def setup_background(self):
        self.background, rect = common.load_image(constants.police)

class PaintStreetSweeper(PaintBase):
    def __init__(self, screen):
        PaintBase.__init__(self, screen)
        self.transparent = pygame.Rect(356, 66, 400, 529)

    def setup_background(self):
        self.background, rect = common.load_image(constants.streetsweeper)

class PaintBarber(PaintBase):
    def __init__(self, screen):
        PaintBase.__init__(self, screen)
        self.transparent = pygame.Rect(356, 156, 400, 387)

    def setup_background(self):
        self.background, rect = common.load_image(constants.barber)

class PaintDoctor(PaintBase):
    def __init__(self, screen):
        PaintBase.__init__(self, screen)
        self.transparent = pygame.Rect(356, 156, 400, 404)

    def setup_background(self):
        self.background, rect = common.load_image(constants.doctor)

class PaintFireFighter(PaintBase):
    def __init__(self, screen):
        PaintBase.__init__(self, screen)
        self.transparent = pygame.Rect(356, 156, 400, 389)

    def setup_background(self):
        self.background, rect = common.load_image(constants.firefighter)

class PaintTeacher(PaintBase):
    def __init__(self, screen):
        PaintBase.__init__(self, screen)
        self.transparent = pygame.Rect(356, 156, 400, 408)

    def setup_background(self):
        self.background, rect = common.load_image(constants.teacher)

class PaintMechanic(PaintBase):
    def __init__(self, screen):
        PaintBase.__init__(self, screen)
        self.transparent = pygame.Rect(356, 156, 400, 426)

    def setup_background(self):
        self.background, rect = common.load_image(constants.mechanic)

if __name__ == "__main__":
	pygame.init()

	screen = pygame.display.set_mode(constants.screen_mode, 32)
    paint = PaintMechanic(screen)
	paint.run()
