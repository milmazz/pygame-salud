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
from icons import *

class Word(Sprite):
    def __init__(self, name, pos=(0,0)):
        Sprite.__init__(self)
        image_name = os.path.join(constants.data_folder, "words",
                                  name  + ".png")
        self.normal, self.rect = common.load_image(image_name, True)
        self.size = self.normal.get_size()
        self.origin = pos
        self.name = name
        self.zoom = pygame.transform.scale(self.normal, (self.size[0] * 1.3, 
                                                        self.size[1] * 1.3))
        self.image = self.normal
        self.update(pos)
        return

    def change_size(self):
        if self.image is self.normal:
            self.image = self.zoom
        else:
	        self.image = self.normal
        return
	
    def update(self, pos):
        self.rect.topleft = pos

    def reset(self):
        self.rect.topleft = self.origin


class Hand(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        path = os.path.join(constants.data_folder, "cursors", "hand")
        self.open, self.rect = common.load_image(path + "-open.png")
        self.close, self.rect = common.load_image(path + "-close.png")
        self.image = self.open
        return

    def change_hand(self):
        if self.image is self.open:
            self.image = self.close
        else:
            self.image = self.open
        return

    def update(self, pos=(0, 0)):
        self.rect.topleft = pos
        return

class Bag:
    def __init__(self, name, rect, sheet, sep=19):
        self.sep = sep
        self.rect = Rect(rect)
        self.sheet = sheet
        self.next = [sheet[0], sheet[1]]
        self.name = name
        self.content = []
        return
        
    def draw(self, screen):
        sheet = Rect(self.sheet)
        pygame.draw.rect(screen, (0,255,0), self.sheet)
        pygame.draw.rect(screen, (0,2,0), self.rect)
        return

    def add(self, item):
        pos = self.next[:]
        self.next[1] += self.sep
        item.update(pos)
        self.content.append(item)
        return self.next
    
    def contains(self, rect):
        return self.rect.contains(rect)


class Words(Activity):
    def __init__(self, screen):
        Activity.__init__(self, screen)
        self.background = common.load_image(constants.illustration_019)[0]
        words = {
                'saludable': (114, 236),
                'risa': (41, 264),
                'alimentos': (143, 283),
                'agua': (41, 307),
                'descanso': (101, 346),
                'amor': (89, 375),
                'limpieza': (26, 407),
                'deporte': (149, 445),
                'sol': (59, 463),
                'aire': (109, 490),
                'aseo': (55, 514),
                'banarse': (193, 542),
                }

        self.title = ("¡Palabras largas, palabras cortas!",)
        self.instructions = ("Estas palabras están relacionadas con la salud.",
                        "  ",
                        "Arrastra hacia la bolsa roja",
                        "las palabras que tienen",
                        "menos de 5 letras y hacia la",
                        "bolsa azul las que tienen",
                        "más de 5 letras.")
        self.informative_text(self.title, self.instructions)
        self.hand = Hand()
        self.icons = pygame.sprite.Group()
        self.icons.add([Icons('stop')])
        self.words = pygame.sprite.Group()
        self.sprites = pygame.sprite.OrderedUpdates()
        for word, pos in words.items():
            word_ = Word(word, pos)
            self.sprites.add(word_)
            self.words.add(word_)
        self.sprites.add([self.icons, self.hand])
        self.sprites.draw(self.screen)
        self.selected = None
        self.bags = (Bag('cortas', (430, 150, 170, 150), (475, 175, 100, 120)), 
                     Bag('largas', (430, 375, 170, 160), (480, 395, 105, 130)))
                
        return

    def info_text(self, messages, pos, size=constants.font_default[1], bg=None):
        font = pygame.font.SysFont(constants.font_default[0], size)
        font_height = font.get_linesize()

        for message in messages:
            message = unicode(message, 'utf-8')
            text = font.render(message, True, constants.font_default_color)
            text_pos = pos
            bg.blit(text, text_pos)
            pos[1] += font_height
 
    def informative_text(self, title, instructions):
        font_title = pygame.font.SysFont(constants.font_title[0],
                                         constants.font_title[1])

        tsize = font_title.size(title[0])

        title_pos = [(constants.screen_mode[0] - tsize[0]) / 2.0, 0]
       
        tsize = font_title.get_linesize()
        instructions_pos = [10, title_pos[1] + 1.5 * tsize]

        self.info_text(title, title_pos, size=constants.font_title[1], bg=self.background)
        self.info_text(instructions, instructions_pos, bg=self.background)

    def setup(self):
        pygame.event.clear()
        self.sprites.draw(self.screen)
        pygame.display.update()

    def handle_events(self):
        for event in self.get_event():
            pos = pygame.mouse.get_pos()
            if event.type == QUIT:
                self.quit = True
                return
            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    self.quit = True
                    return
            if event.type == MOUSEMOTION:
                self.hand.update(pos)
                if self.selected:
                    self.selected.update(pos)
            if event.type == MOUSEBUTTONDOWN:
                if pygame.sprite.spritecollideany(self.hand, self.icons):
                    self.quit = True
                    return
                self.hand.change_hand()
                self.selected = pygame.sprite.spritecollideany(self.hand, 
                                                               self.words)
                if self.selected:
                    self.selected.change_size()
            elif event.type == MOUSEBUTTONUP:
                self.hand.change_hand()
                if self.selected:
                    added = False
                    for bag in self.bags:
                        if bag.contains(self.selected.rect) and \
                                self.correct(self.selected, bag):
                            check_pos = bag.add(self.selected)
                            self.words.remove(self.selected)
                            self.sprites.add(Check(check_pos, 0, (26, 25)))
                            added = True
                    if not added:
                        self.selected.reset()
                    
                    self.selected.change_size()
                    self.selected = None

            if not self.words:
                self.finished_ = True

            self.screen.blit(self.background, (0,0))
            self.sprites.draw(self.screen)
            pygame.display.update()

    def correct(self, word, bag):
        if len(word.name) <= 5 and bag.name == 'cortas':
            return True
        elif len(word.name) > 5 and bag.name == 'largas':
            return True
        else:
            return False


if __name__ == "__main__":
	pygame.init()

	screen = pygame.display.set_mode(constants.screen_mode, 32)
    words = Words(screen)
    words.run()
