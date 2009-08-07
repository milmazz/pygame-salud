# vim:ts=4:sts=4:et:nowrap:tw=77
# -*- coding: utf-8 -*-

import os
import sys
import pygame
from pygame.sprite import Sprite
from pygame.locals import *

import constants
from activity import Activity
import common
import math
from icons import Icons

class Girl(Sprite):
    def __init__(self, pos, id, name, exit=(0,0)):
        Sprite.__init__(self)
        self.imagen_normal = os.path.join(constants.images_labyrinth, name + '.png')
        self.imagen_check = os.path.join(constants.images_labyrinth, 
                                         name + '_check.png')
        self.image, self.rect = common.load_image(self.imagen_normal)
        self.rect.move_ip(pos)
        self.id = id
        self.img = 0
        self.exit_pos = exit

    def update(self):
            if self.img == 1:
                self.image, rect = common.load_image(self.imagen_check)


class Ball(Sprite):
    def __init__(self, screen):
        Sprite.__init__(self)
        path = os.path.join(constants.images_labyrinth, "ball.png")
        self.image, self.rect = common.load_image(path)
        self.rect.move_ip((50,50))
        self.pos = (0,0)
        self.move_ball = 10
        self.screen = screen
        self.counter = 1

    def verify_color_position(self, pos):
        if pos[0] > 0 and pos[0] < constants.screen_mode[0]\
          and pos[1] > 0 and pos[1] < constants.screen_mode[1]:
            color = self.screen.get_at(pos)
        else:
                return False
        if color[0] >= 220 and color[1] >= 220 and\
          color[2] >= 150 and color[3] >= 250:
            return True
        else:
            return False

    def update(self, pos=(0,0)):
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.pos = pos

    def up_key(self):
        move = 10
        for i in range(1, self.move_ball + 1):
            if (not self.verify_color_position((self.rect.x + 5,
                self.rect.y - i)) or not\
                self.verify_color_position((self.rect.x ,\
                self.rect.y - i)) or not\
                self.verify_color_position((self.rect.x +\
                10, self.rect.y - i))) and move == 10:
                move = i - 1
        self.update((self.rect.x, self.rect.y - move))
    
    def down_key(self):
        move = 10
        for i in range(1, self.move_ball + 1):
            if (not self.verify_color_position((self.rect.x + 5,\
                self.rect.y + 10 + i)) or\
                not self.verify_color_position((self.rect.x,\
                self.rect.y + 10 + i)) or\
                not self.verify_color_position((self.rect.x + 10,\
                self.rect.y + 10 + i))) and move == 10:
                move = i - 1
        self.update((self.rect.x, self.rect.y + move))

    def left_key(self):
        move = 10
        for i in range(1, self.move_ball + 1):
            if (not self.verify_color_position((self.rect.x - i,
                self.rect.y + 5 )) or\
                not self.verify_color_position((self.rect.x -i,
                self.rect.y )) or\
                not self.verify_color_position((self.rect.x -i,
                self.rect.y + 10))) and move == 10:
                move = i - 1
        self.update((self.rect.x - move, self.rect.y))

    def right_key(self):
        move = 10
        for i in range(1, self.move_ball + 1):
            if (not self.verify_color_position((self.rect.x + 10 + i,
                self.rect.y + 5)) or\
                not self.verify_color_position((self.rect.x + 10
                + i, self.rect.y)) or\
                not self.verify_color_position((self.rect.x + 10
                + i, self.rect.y + 10))) and move == 10:
                move = i - 1
        if move < 0:
            move = 0
        self.update((self.rect.x + move, self.rect.y))

 
class Labyrinth(Activity):
    def __init__(self, screen):
        Activity.__init__(self, screen)

    def setup_background(self):
        self.background, rect = common.load_image(constants.illustration_010)

    def setup(self):
        self.ball = Ball(self.screen)
        self.Gball = pygame.sprite.Group()
        self.Gball.add([self.ball])

        self.Girls = pygame.sprite.Group()
        self.Girls.add([Girl((330,85),1,'1',(330, 170)),
                        Girl((280,480),2,'2',(400,473)),
                        Girl((120,318),3,'3',(216, 306)),
                        Girl((495,343),4,'4',(486,387))])

        self.GroupSprite = pygame.sprite.OrderedUpdates()
        self.GroupSprite.add([ self.Gball, self.Girls])
        self.pos = (100,100)
        
        self.screen.blit(self.background, (0,0))
        self.GroupSprite.draw(self.screen)
        pygame.display.update()

        pygame.event.set_blocked(MOUSEMOTION)
        pygame.key.set_repeat(200, 100)

    def handle_events(self):
        exit = False

        while not exit:
            old_pos = self.ball.pos
            for event in [ pygame.event.wait() ] +  pygame.event.get():
                if event.type == QUIT:
                    self.quit = True
                    exit = True
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.quit = True
                        exit = True
                    elif event.key == K_UP:
                        self.ball.up_key()
                    elif event.key == K_DOWN:
                        self.ball.down_key()
                    elif event.key == K_LEFT:
                        self.ball.left_key()
                    elif event.key == K_RIGHT:
                        self.ball.right_key()

                selection = pygame.sprite.spritecollideany(self.ball,
                                self.Girls)
                if selection:
                        if selection.id == self.ball.counter:
                                self.ball.counter += 1
                                selection.img = 1
                                selection.update()
                                self.ball.update(selection.exit_pos)

                self.screen.blit(self.background, (0,0))
                self.GroupSprite.draw(self.screen)
                pygame.display.update()
        
        pygame.event.set_allowed(MOUSEMOTION)
