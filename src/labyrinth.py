
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


class Hand(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image_normal = os.path.join(constants.data_folder,\
          'cursors', "hand-open.png")
        self.image_close = os.path.join(constants.data_folder,\
          'cursors', "hand-close.png")
        self.normal, self.rect = common.load_image(self.image_normal)
        self.close, self.rect = common.load_image(self.image_close)
        self.image = self.normal 
        self.color = 0

    def change_hand(self):
        if self.color == 0:
            self.color = 1
        else:
            self.color = 0

    def update(self, mover=(0,0)):
        self.rect.x = mover[0] 
        self.rect.y = mover[1] 
        if self.color == 0:
            self.image = pygame.image.load(self.image_normal)
        if self.color == 1:
            self.image = pygame.image.load(self.image_close)


class Ball(Sprite):
    def __init__(self, screen, pos):
        Sprite.__init__(self)
        path = os.path.join(constants.images_labyrinth, "ball.png")
        self.image, self.rect = common.load_image(path)
        self.rect.move_ip(pos)
        self.pos = (0,0)
        self.move_ball = 5
        self.screen = screen

    def verify_color_position(self, pos):
        if pos[0] > 0 and pos[0] < constants.screen_mode[0]\
          and pos[1] > 0 and pos[1] < constants.screen_mode[1]:
            color = self.screen.get_at(pos)
        else:
                return False
        if color[0] >= 210 and color[1] >= 144 and\
          color[2] >= 210 and color[3] >= 250:
            return True
        else:
            return False

    def update(self, pos=(0,0)):
        self.rect.x, self.rect.y = pos[0], pos[1]
        self.pos = pos

    def up_key(self):
        move = self.move_ball
        for i in range(1, self.move_ball + 1):
            if (not self.verify_color_position((self.rect.x + 5,
                self.rect.y - i)) or not\
                self.verify_color_position((self.rect.x ,\
                self.rect.y - i)) or not\
                self.verify_color_position((self.rect.x +\
                10, self.rect.y - i))) and move == self.move_ball:
                move = i - 1
        self.update((self.rect.x, self.rect.y - move))
    
    def down_key(self):
        move = self.move_ball
        for i in range(1, self.move_ball + 1):
            if (not self.verify_color_position((self.rect.x + 5,\
                self.rect.y + 10 + i)) or\
                not self.verify_color_position((self.rect.x,\
                self.rect.y + 10 + i)) or\
                not self.verify_color_position((self.rect.x + 10,\
                self.rect.y + 10 + i))) and move == self.move_ball:
                move = i - 1
        self.update((self.rect.x, self.rect.y + move))

    def left_key(self):
        move = self.move_ball
        for i in range(1, self.move_ball + 1):
            if (not self.verify_color_position((self.rect.x - i,
                self.rect.y + 5 )) or\
                not self.verify_color_position((self.rect.x -i,
                self.rect.y )) or\
                not self.verify_color_position((self.rect.x -i,
                self.rect.y + 10))) and move == self.move_ball:
                move = i - 1
        self.update((self.rect.x - move, self.rect.y))

    def right_key(self):
        move = self.move_ball
        for i in range(1, self.move_ball + 1):
            if (not self.verify_color_position((self.rect.x + 10 + i,
                self.rect.y + 5)) or\
                not self.verify_color_position((self.rect.x + 10
                + i, self.rect.y)) or\
                not self.verify_color_position((self.rect.x + 10
                + i, self.rect.y + 10))) and move == self.move_ball:
                move = i - 1
        self.update((self.rect.x + move, self.rect.y))

 
class Labyrinth(Activity):
    def __init__(self, screen):
        Activity.__init__(self, screen)
        self.correct = set()

    def setup_background(self):
        self.background = pygame.image.load(constants.illustration_010)

    def setup(self):
        self.ball = Ball(self.screen)
        self.Gball = pygame.sprite.Group()
        self.Gball.add([self.ball])

    def informative_text(self):
        if pygame.font:
            font = pygame.font.SysFont("dejavusans", 32)
            text = font.render("El laberinto de la salud", 1, (0, 0, 0))
            textRect = text.get_rect()
            textRect.centerx = self.screen.get_rect().centerx
            textRect.centery = 20
            self.screen.blit(text, textRect)

            font = pygame.font.SysFont("dejavusans", 20)
            instructions = \
                    [u"  Ayuda a Nina a realizar",
                    u"las tareas diarias a través",
                    u"del laberinto. Utiliza las",
                    u"teclas de desplazamiento."]
            y = 490
            for line in instructions:
                text = font.render(line, 1,(0, 0, 0))
                self.screen.blit(text, (20, y))
                y+=20

    def setup(self):
        pygame.mouse.set_visible( False )
        path = os.path.join(constants.images_labyrinth, "correct.png")
        self.checkImage, self.checkImageRect = common.load_image(path)
        self.counter = 0
        self.rectangleListEnter = [
                pygame.Rect(345, 90, 10, 15),
                pygame.Rect(340, 480, 10, 15),
                pygame.Rect(300, 390, 10, 15),
                pygame.Rect(493, 325, 10, 15),
                pygame.Rect(362, 299, 10, 15)
                ]
        self.pointList = [
                (350, 123),
                (400, 460),
                (277, 279),
                (451, 365)
                ]
        self.checkList = [
                (390, 80),
                (360, 520),
                (260, 340),
                (494, 358),
                (407, 304),
                ]
        self.icons = pygame.sprite.Group()
        self.icons.add([Icons('stop')])
        self.hand = Hand()
        self.ball = Ball(self.screen, (200,80))
        self.Gball = pygame.sprite.Group()
        self.Gball.add([self.ball])
        self.GroupSprite = pygame.sprite.OrderedUpdates()
        self.GroupSprite.add([ self.icons, self.Gball, self.hand])
        self.pos = (100,200)
        self.screen.blit(self.background, (0,0))
        self.informative_text()
        self.GroupSprite.draw(self.screen)
        pygame.display.update()
        pygame.key.set_repeat(50, 50)

    def handle_events(self): 
        for event in [ pygame.event.wait() ] + pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == QUIT:
                self.quit = True
                return
            elif event.type == MOUSEMOTION:
                self.hand.update(pos)
            elif event.type == MOUSEBUTTONDOWN:
              if pygame.sprite.spritecollideany(self.hand,\
                    self.icons):
                  self.quit = True
                  return
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.quit = True
                    return
                elif event.key == K_UP:
                    self.ball.up_key()
                elif event.key == K_DOWN:
                    self.ball.down_key()
                elif event.key == K_LEFT:
                    self.ball.left_key()
                elif event.key == K_RIGHT:
                    self.ball.right_key()
                self.hand.update((0,0))

                if self.counter <= 4 and self.ball.rect.colliderect(self.\
                  rectangleListEnter[self.counter]):
                    if self.counter < 4:
                        self.ball.update(self.pointList[self.counter])
                    self.background.blit(self.checkImage,\
                      self.checkList[self.counter])
                    self.counter += 1
        if self.counter == 5:
            self.finished_ = True

        self.screen.blit(self.background, (0,0))
        self.GroupSprite.draw(self.screen)
        self.informative_text()
        pygame.display.update()

class Labyrinth2Activity(Activity):
    def __init__(self, screen):
        Activity.__init__(self, screen)
        self.correct = set()

    def setup_background(self):
        self.background = pygame.image.load(constants.illustration_022)

    def setup(self):
        self.ball = Ball(self.screen)
        self.Gball = pygame.sprite.Group()
        self.Gball.add([self.ball])

    def informative_text(self):
        if pygame.font:
            font = pygame.font.SysFont("dejavusans", 32)
            text = font.render(u"Día de limpieza", 1, (0, 0, 0))
            textRect = text.get_rect()
            textRect.centerx = self.screen.get_rect().centerx
            textRect.centery = 20
            self.screen.blit(text, textRect)

            font = pygame.font.SysFont("dejavusans", 20)
            instructions = \
                    [u"Recorre el laberinto y une",
                    u"los objetos con las palabras"]
            y = 60
            for line in instructions:
                text = font.render(line, 1,(0, 0, 0))
                self.screen.blit(text, (20, y))
                y+=20

    def setup(self):
        pygame.mouse.set_visible( False )
        path = os.path.join(constants.images_labyrinth, "correct.png")
        self.checkImage, self.checkImageRect = common.load_image(path)
        self.counter = 0
        self.rectangleListEnter = [
                pygame.Rect(212, 342, 50, 25),
                pygame.Rect(354, 407, 3, 20),
                pygame.Rect(251, 506, 1, 25),
                pygame.Rect(600, 320, 12, 6),
                pygame.Rect(470, 522, 7, 17)
                ]
        self.pointList = [
                (130, 390),
                (130, 564),
                (534, 201),
                (642, 489)
                ]
        self.checkList = [
                (250, 305),
                (400, 391),
                (290, 535),
                (607, 279),
                (521, 540),
                ]
        self.icons = pygame.sprite.Group()
        self.icons.add([Icons('stop')])
        self.hand = Hand()
        self.ball = Ball(self.screen, (400,250))
        self.Gball = pygame.sprite.Group()
        self.Gball.add([self.ball])
        self.GroupSprite = pygame.sprite.OrderedUpdates()
        self.GroupSprite.add([ self.icons, self.Gball, self.hand])
        self.pos = (100,200)
        self.screen.blit(self.background, (0,0))
        self.informative_text()
        self.GroupSprite.draw(self.screen)
        pygame.display.update()
        pygame.key.set_repeat(50, 50)

    def handle_events(self): 
        for event in [ pygame.event.wait() ] + pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == QUIT:
                self.quit = True
                return
            elif event.type == MOUSEMOTION:
                self.hand.update(pos)
            elif event.type == MOUSEBUTTONDOWN:
              if pygame.sprite.spritecollideany(self.hand,\
                    self.icons):
                  self.quit = True
                  return
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.quit = True
                    return
                elif event.key == K_UP:
                    self.ball.up_key()
                elif event.key == K_DOWN:
                    self.ball.down_key()
                elif event.key == K_LEFT:
                    self.ball.left_key()
                elif event.key == K_RIGHT:
                    self.ball.right_key()
                self.hand.update((0,0))

                if self.counter <= 4 and self.ball.rect.colliderect(self.\
                  rectangleListEnter[self.counter]):
                    if self.counter < 4:
                        self.ball.update(self.pointList[self.counter])
                    self.background.blit(self.checkImage,\
                      self.checkList[self.counter])
                    self.counter += 1
        if self.counter == 5:
            self.finished_ = True

        self.screen.blit(self.background, (0,0))
        self.GroupSprite.draw(self.screen)
        self.informative_text()
        pygame.display.update()
