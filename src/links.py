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
from icons import *

class Item(sprite.Sprite):
        def __init__(self, name, position):
            sprite.Sprite.__init__(self)
            self.name = name
            self.image_name = os.path.join(constants.data_folder, 
                                           "links", name)
            self.normal, self.rect = common.load_image(self.image_name + ".png")
            self.over = common.load_image(self.image_name + "_hover.png")[0]
            self.image = self.normal
            self.rect.move_ip(position)
            self.active = False

        def update(self):
            if self.active:
                self.deactivate()
            else:
                self.activate()

        def activate(self):
            self.active = True
            self.image = self.over

        select = activate

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
        self.rect.topleft = pos


class Arrow:
    def __init__(self, surface, start=(0, 0), end=(0, 0), color=(0,0,0),
                 width=1):
        self.surface = surface
        self.start = start
        self.end = end
        self.color = color
        self.width = width

        self.update()

        return

    def update(self, start=None, end=None):
        if start:
            self.start = start
        if end:
            self.end = end

        pygame.draw.line(self.surface, self.color, self.start, self.end,
                         self.width)

        rotate = math.atan2(self.end[1] - self.start[1], 
                               self.end[0] - self.start[0])
        rotate = math.degrees(rotate)
        h = 20
        angle1 = math.radians(30 + rotate)
        angle2 = math.radians(30 - rotate)

        x1 = self.end[0] - math.cos(angle1) * h
        y1 = self.end[1] - math.sin(angle1) * h
        x2 = self.end[0] - math.cos(angle2) * h
        y2 = self.end[1] + math.sin(angle2) * h
        points = [(x1, y1), (x2, y2), (self.end)]
        pygame.draw.polygon(self.surface, self.color, points) 
        return


# Activity 7
class Links(Activity):
    def __init__(self, screen, pos):
        Activity.__init__(self, screen)

 
        self.couple = set()
        self.couples = []

        self.sprites0 = pygame.sprite.OrderedUpdates()
        self.sprites1 = pygame.sprite.OrderedUpdates()
        self.pointer_ = pygame.sprite.OrderedUpdates()
        self.items = pygame.sprite.Group()
        self.icons = pygame.sprite.Group()

        self.icons.add([Icons('stop')])

        self.sprites0.add(self.icons)

        for i in pos.keys():
            item = Item(i, pos[i])
            self.sprites0.add(item)
            self.items.add(item)

        self.pointer = Pointer()
        self.pointer_.add(self.pointer)

        self.arrows = []
        self.arrow = None

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
        instructions_pos = [10, title_pos[1] + tsize]

        self.info_text(title, title_pos, size=constants.font_title[1], bg=self.background)
        self.info_text(instructions, instructions_pos, bg=self.background)

    def setup(self):
        self.informative_text(self.title, self.instructions)
        pygame.display.update()
        
    def handle_events(self):
        for event in self.get_event():
            if event.type == QUIT:
                self.quit = True
                return
            elif event.type == KEYUP:
                self.changed = False
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
                    selected.activate()
                    self.couple.add(selected)

                    if len(self.couple) == 1:
                        start = selected.rect.center
                        self.arrow = Arrow(surface=self.screen, start=start,
                                           end=start, width=3)
                    elif len(self.couple) == 2:
                        if self.are_couple(self.couple):
                        # TODO some feeback? message? sound?
                            if not (self.couple in self.couples):
                                self.couples.append(self.couple.copy())
                                end = self.couple.pop().rect.center
                                start = self.couple.pop().rect.center
                                self.arrow.update(start=start, end=end)
                                self.arrows.append(self.arrow)
                                pos = ((start[0] + end[0]) / 2.0, 
                                             (start[1] + end[1]) / 2.0)
                                self.sprites1.add(Check(pos, 0, (36, 35)))
                        else:
                            for i in self.couple:
                                i.deactivate()

                        for i, j in self.couples:
                            i.activate()
                            j.activate()
                       
                        self.arrow = None
                        self.couple.clear()

            if event.type == MOUSEMOTION:
                if self.arrow:
                    end = pygame.mouse.get_pos()
                    self.arrow.update(end=end)

            if len(self.couples) == 4:
                self.finished_ = True

            self.screen.blit(self.background, (0,0))
            self.sprites0.draw(self.screen)
            if self.arrow:
                self.arrow.update()
            for i in self.arrows:
                i.update()

            self.sprites1.draw(self.screen)
            self.pointer_.draw(self.screen)
            pygame.display.flip()


# Activity 7
class Shower(Links):
    def __init__(self, screen):
        self.title = ("¡A la ducha!",)
        self.instructions = ("Une con una flecha lo que necesitas para",
                             "asear cada parte de tu cuerpo.")
        pos = {
                'towel': (150, 126),
                'shampoo': (70, 255),
                'brush': (125, 365),
                'soap': (155, 470),
                'hair': (500, 180),
                'body': (510, 295),
                'mouth': (500, 450),
                }
        Links.__init__(self, screen, pos)
        return 

    def setup_background(self):
        self.background = common.load_image(constants.illustration_007)[0]

    def are_couple(self, couple):
        b, a = couple
        if a.active and b.active:
            if a.name == 'towel' and b.name == 'body':
                return True
            if a.name == 'body' and b.name == 'towel':
                return True
            if a.name == 'shampoo' and b.name == 'hair':
                return True
            if a.name == 'hair' and b.name == 'shampoo':
                return True
            if a.name == 'brush' and b.name == 'mouth':
                return True
            if a.name == 'mouth' and b.name == 'brush':
                return True
            if a.name == 'soap' and b.name == 'body':
                return True
            if a.name == 'body' and b.name == 'soap':
                return True
        return False 


# Activity 23
class Meals(Links):
    def __init__(self, screen):
        self.title = ("Cada oveja con su pareja",)
        self.instructions = ("Une con una línea el dibujo con la palabra",
                             "que le corresponde.",)
        pos = {
                'breakfast': (491, 476),
                'lunch': (399, 75),
                'dinner': (330, 341),
                'snack': (512, 201),
                'tlunch': (40, 115),
                'tsnack': (70, 205),
                'tdinner': (92, 347),
                'tbreakfast': (20, 459),
                }
        Links.__init__(self, screen, pos)

    def setup_background(self):
        self.background = common.load_image(constants.illustration_023)[0]

    def are_couple(self, couple):
        b, a = couple
        couple = False
        if a.active and b.active:
            if a.name == 'tbreakfast' and b.name == 'breakfast':
                return True        
            elif a.name == 'tlunch' and b.name == 'lunch':
                return True        
            elif a.name == 'tsnack' and b.name == 'snack':
                return True        
            elif a.name == 'tdinner' and b.name == 'dinner':
                return True        
            elif a.name == 'breakfast' and b.name == 'tbreakfast':
                return True        
            elif a.name == 'lunch' and b.name == 'tlunch':
                return True        
            elif a.name == 'snack' and b.name == 'tsnack':
                return True        
            elif a.name == 'dinner' and b.name == 'tdinner':
                return True
        return False


if __name__ == "__main__":
	pygame.init()

	screen = pygame.display.set_mode(constants.screen_mode, 32)
    meals = Meals(screen)
    meals.run()
