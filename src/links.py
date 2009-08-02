# vim:ts=4:sts=4:et:nowrap:tw=77
# -*- coding: utf-8 -*-

import sys
import os
import math

import pygame
from pygame import *
from pygame.locals import *

import constants
import common
from activity import Activity
from icons import Icons


# Activity 7
class Shower(Activity):
    def __init__(self, screen):
        Activity.__init__(self, screen)

        pos = {
                'towel': (150, 126),
                'shampoo': (70, 255),
                'brush': (125, 365),
                'soap': (155, 470),
                'hair': (500, 180),
                'body': (510, 295),
                'mouth': (500, 450),
                }
#         self.items = {
#                 'towel': pygame.Rect(260, 186, 102, 100),
#                 'shampoo': pygame.Rect(170, 295, 80, 85),
#                 'brush': pygame.Rect(285, 385, 105, 65),
#                 'soap': pygame.Rect(195, 498, 90, 65),
#                 'hair': pygame.Rect(507, 227, 74, 65),
#                 'body': pygame.Rect(491, 365, 94, 82),
#                 'mouth': pygame.Rect(500, 510, 73, 42),
#                 }
  
        self.selections = []
        self.actual_selection = []
        self.couple = set()
        self.couples = []

        self.sprites = pygame.sprite.OrderedUpdates()
        self.items = pygame.sprite.Group()
        self.icons = pygame.sprite.Group()

        self.icons.add([Icons('stop')])

        self.sprites.add(self.icons)

        for i in pos.keys():
            item = Item(i, pos[i])
            self.sprites.add(item)
            self.items.add(item)


        self.pointer = Pointer()
        self.sprites.add(self.pointer)

        self.arrows = []

    def setup_background(self):
        self.background = common.load_image(constants.illustration_007)[0]

    def setup(self):
        font_title = pygame.font.SysFont("dejavusans", 40)
        font_instructions = pygame.font.SysFont("dejavusans", 20)

        title = u"¡A la ducha!"
        title_width, title_height = font_title.size(title)

        instructions = [u"Une con una flecha lo que necesitas para", 
                        u"asear cada parte de tu cuerpo."]

        y = title_height / 2

        text = font_title.render(title, True, (102, 102, 102))
        text_pos = (constants.screen_mode[0]/2.0 - title_width/2.0, y)

        self.screen.blit(self.background, (0,0))
        self.screen.blit(text, text_pos)

        y += title_height
        line_width, line_height = font_instructions.size(instructions[0])
        for line in instructions:
            text = font_instructions.render(line, True, (102, 102, 102))
            y += line_height
            text_pos = (50, y)
            self.screen.blit(text, text_pos)
            
        self.sprites.draw(self.screen)
        
    def handle_events(self):
        for event in [pygame.event.wait()] + pygame.event.get():
            if event.type == QUIT:
                self.quit = True
                return
            elif event.type == KEYUP:
                self.changed = True
                if event.key == K_ESCAPE:
                    self.quit = True                        
                    return
            elif event.type == MOUSEMOTION:
                pointer_pos = pygame.mouse.get_pos()
                self.pointer.update(pointer_pos)
            elif event.type == MOUSEBUTTONDOWN:
                    """Test if the mouse pointer is over the 
                       close button"""
                    if pygame.sprite.spritecollideany(self.pointer, self.icons):
                        self.quit = True
                        return
                    selected = sprite.spritecollideany(self.pointer, 
                                                       self.items)
                    if selected:
                        selected.update()
                        if selected.active:
                            self.couple.add(selected)
                        elif selected in self.couple:
                                self.couple.remove(selected)

                    if len(self.couple) == 2:
                        # TODO some feeback? message? sound?
                        if self.are_couple(self.couple):
                            for i in self.couple:
                                i.deactivate()

                            if not (self.couple in self.couples):
                                self.couples.append(self.couple.copy())
                                a = self.couple.pop().rect.center
                                b = self.couple.pop().rect.center
                                self.sprites.add(Arrow(start=b, end=a))
                        
                        for i in self.couple:
                            i.deactivate()
                            
                        self.couple.clear()

            self.setup()
            pygame.display.flip()

    def are_couple(self, couple):
        b, a = couple
        if a.active and b.active:
            if a.name == 'towel' and b.name == 'body':
                return True
#            if a.name == 'body' and b.name == 'towel':
#                return True
            if a.name == 'shampoo' and b.name == 'hair':
                return True
#            if a.name == 'hair' and b.name == 'shampoo':
#                return True
            if a.name == 'brush' and b.name == 'mouth':
                return True
#            if a.name == 'mouth' and b.name == 'brush':
#                return True
            if a.name == 'soap' and b.name == 'body':
                return True
#            if a.name == 'body' and b.name == 'soap':
#                return True
                
        return False 


class Item(sprite.Sprite):
        def __init__(self, name, position):
            sprite.Sprite.__init__(self)
            self.name = name
            self.image_name = os.path.join(constants.data_folder, 
                                           "links", name)
            self.normal, self.rect = common.load_image(self.image_name + ".png")
            self.over = common.load_image(self.image_name + "_over.png")[0]
            self.image = self.normal
            self.rect.move_ip(position)
            self.active = False

            self.rect.inflate_ip(-self.rect[2]*0.3, -self.rect[3]*0.3)

        def update(self):
            if self.active:
                self.deactivate()
            else:
                self.activate()

        def activate(self):
            self.active = True
            self.image = self.over

        def deactivate(self):
            self.active = False
            self.image = self.normal


class Pointer(sprite.Sprite):
    def __init__(self):
        sprite.Sprite.__init__(self) 
        self.image, self.rect = common.load_image(constants.cursor_filename)

        self.rect[2] = 10
        self.rect[3] = 10

        pos = (constants.screen_mode[0]/2.0, constants.screen_mode[1]/2.0)
        pygame.mouse.set_pos(pos)
        self.update(pos)

    def update(self, pos):
        self.rect.midtop = pos


class Arrow(sprite.Sprite):
    def __init__(self, start=(0, 0), end=(0, 0)):
        sprite.Sprite.__init__(self)
        self.start = start
        self.end = end
        self.points = []
        self.image, self.rect = common.load_image(constants.arrow)
        self.update()

    def update(self, start = None, end = None):
        if start:
            self.start = start
        if end:
            self.end = end

        width = math.hypot(self.start[0] - self.end[0],
                           self.start[1] - self.end[1])
        height = self.rect[3]
        rotate = -1*math.atan2(self.end[1] - self.start[1], 
                            self.end[0] - self.start[0])
        rotate = math.degrees(rotate) 

        if rotate > 0:
            self.start = (self.start[0], self.start[1] - self.rect[2])

        self.image = pygame.transform.scale(self.image, (width, height))
        self.image = pygame.transform.rotate(self.image, rotate)
        self.rect.move_ip(self.start)

 
