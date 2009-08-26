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
        # Colors
        self.color_red = pygame.draw.rect(self.background, (255, 0, 0), (100, 100, 20, 20))
        self.color_green = pygame.draw.rect(self.background, (0, 255, 0), (130, 100, 20, 20))
        self.color_white = pygame.draw.rect(self.background, (255, 255, 255), (100, 130, 20, 20))
        self.color_blue = pygame.draw.rect(self.background, (0, 0, 255), (130, 130, 20, 20))
        self.color_black = pygame.draw.rect(self.background, (0, 0, 0), (100, 160, 20, 20))
        #
        self.pincel1 = pygame.draw.circle(self.background, (0, 0, 0), (100, 200), 5)
        self.pincel2 = pygame.draw.circle(self.background, (0, 0, 0), (120, 200), 10)
        self.pincel3 = pygame.draw.circle(self.background, (0, 0, 0), (155, 200), 15)
        self.pincel3 = pygame.draw.circle(self.background, (0, 0, 0), (195, 200), 20)
    
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
                elif self.color_red.collidepoint(self.line_end):
                    # Red
                    self.draw_color = (255, 0, 0)
                elif self.color_green.collidepoint(self.line_end):
                    # Green
                    self.draw_color = (0, 255, 0)
                elif self.color_white.collidepoint(self.line_end):
                    # White
                    self.draw_color = (255, 255, 255)
                elif self.color_blue.collidepoint(self.line_end):
                    # Blue
                    self.draw_color = (0, 0, 255)
                elif self.color_black.collidepoint(self.line_end):
                    # Black
                    self.draw_color = (0, 0, 0)
                elif self.pincel1.collidepoint(self.line_end):
                    self.line_width = 3
                elif self.pincel2.collidepoint(self.line_end):
                    self.line_width = 10
                elif self.pincel3.collidepoint(self.line_end):
                    self.line_width = 20
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
        #self.text()
        self.cursor.draw(self.screen)
        self.mprev = self.pos

    def text(self):
        # Title
        font = pygame.font.SysFont("dejavusans", 32)
        font_height = font.get_linesize()
        x, y = 20, 20

        title = unicode("La salud de nuestra comunidad", 'utf-8')
        text = font.render(title, True, (0, 0, 0))
        text_pos = (x, y)
        self.screen.blit(text, text_pos)

        messages = ['Alguna de estas personas', \
            'trabajan para mantener', \
            'la salud de tu comunidad.', \
            'Diviértete coloreándolos.']

        y += font_height
        font = pygame.font.SysFont("dejavusans", 20)
        font_height = font.get_linesize()

        for message in messages:
            message = unicode(message, 'utf-8')
            text = font.render(message, True, (122, 122, 122))
            text_pos = (x, y)
            self.background.blit(text, text_pos)
            y += font_height

    def setup(self):
        pygame.mouse.set_visible(False)
        self.close_button.draw(self.screen)
        self.cursor.draw(self.screen)
        #self.text()

class PaintActivity(PaintBase):
    def setup_background(self):
        self.background, rect = common.load_image(constants.teacher)
    
class Paint2Activity(PaintBase):
    def setup_background(self):
        self.background, rect = common.load_image(constants.mechanic)
    
if __name__ == "__main__":
	pygame.init()

	screen = pygame.display.set_mode(constants.screen_mode, 32)
    paint = Paint2Activity(screen)
	paint.run()
