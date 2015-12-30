# vim:et:ts=4:sts=4:nowrap:tw=77
# -*- coding: utf-8 -*-
import os
import random

import pygame
from pygame.locals import *

import common
import constants

MAXFPS = 20


class Activity:
    def __init__(self, screen):
        self.screen = screen

        self.setup_background()
        self.center = self.background.get_rect().center

        self.clock = pygame.time.Clock()
        self.quit = False
        self.changed = False
        self.mprev = None
        click = common.load_sound(constants.snd_click)
        complete = None  # common.load_sound(constants.snd_complete)
        self.sounds = {'click': click, 'complete': complete}
        random.seed(None)
        self.finished_ = False
        texts = [u"¡Excelente!", u"¡Eres muy inteligente!", u"¡Muy bien!",
                 u"¡Lo lograste!", u"¡Sigue adelante!"]

        self.finished_text = random.choice(texts)
        self.snd_congratulation = common.load_sound(constants.snd_congratulation)
        self.done = False

    def setup_background(self):
        self.background = pygame.image.load(constants.background_filename).convert()

    def load_image(self, name, colorkey=None):
        return common.load_image(name, colorkey)

    def load_sound(self, name):
        return common.load_sound(name)

    def get_event(self):
        events = pygame.event.get()
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                self.sounds['click'].play()
            if event.type == QUIT:
                self.quit = True
        return events

    def run(self):
        self.screen.blit(self.background, (0, 0))
        self.setup()
        pygame.display.flip()
        while True:
            self.clock.tick(MAXFPS)

            if self.finished_:
                self.finished()
            else:
                # self.handle_events()
                pass
            self.handle_events()

            if self.quit:
                break
            if self.changed:
                self.screen.blit(self.background, (0, 0))
                self.on_change()
                pygame.display.flip()
            self.changed = False

    def setup(self):
        pass

    def handle_events(self):
        pass

    def on_change(self):
        pass

    def finished(self):
        font = pygame.font.SysFont("dejavusans", 64)
        size = font.size(self.finished_text)
        pos = self.center[0] - size[0] / 2.0, self.center[1] - size[1] / 2.0
        # text = font.render(self.finished_text, True, (102, 10, 12))
        # rect = self.screen.blit(text, pos)
        # pygame.display.update(rect)

        if not self.done:
            self.snd_congratulation.play()
        self.done = True
        return

    def wrong(self):
        pass

    def good(self):
        pass
