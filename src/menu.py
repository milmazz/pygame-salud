# vim:ts=4:sts=4:et:nowrap:tw=77
# -*- coding: utf-8 -*-

import os

import pygame
from pygame import *
from pygame.locals import *

import constants
import common
from activity import Activity
from icons import Icons

class Finger(sprite.Sprite):
    """This class define the mouse sprite"""
    def __init__(self):
        sprite.Sprite.__init__(self) 
        self.image, self.rect = common.load_image(constants.cursor_filename)
        pos = constants.screen_mode[0] / 2.0, constants.screen_mode[1] / 2.0
        self.rect.width = 1
        self.rect.height = 1
        mouse.set_pos(pos)

    def update(self):
        pos = mouse.get_pos()
        self.rect.topleft = pos


class ItemBase(sprite.Sprite):
    def __init__(self, name, pos=(0,0)):
        sprite.Sprite.__init__(self)
        path = os.path.join(constants.data_folder, 'menu', name + ".png")
        if os.path.exists(path):
            #self.normal, self.rect = common.load_image(path + ".png")
            self.normal, self.rect = common.load_image(path)
            self.hover = self.normal
            self.active = self.normal
            #self.hover, self.rect = common.load_image(path + "_hover.png")
            #self.active, self.rect = common.load_image(path + "_hover.png")
        else:
            path = os.path.join(constants.data_folder, 'menu', 'noimage.png')
            self.normal, self.rect = common.load_image(path)
            self.hover = self.normal
            self.active = self.normal

        self.active = self.normal
        self.image = self.normal
        self.active = False
        self.name = name
        
        self.place(pos)
        return

    def place(self, pos):
        self.rect.move_ip(pos)
        return

    def activate(self):
        self.image = self.hover
        self.active = True
        return

    def update(self):
        self.rect.midpos = self.rect.midpos

    def run(self):
        pass


class ItemCategory(ItemBase):
    def __init__(self, name, pos):
        ItemBase.__init__(self, name)


class ItemActivity(ItemBase):
    def __init__(self, name, activity, category='uncategorized'):
        ItemBase.__init__(self, name)
        self.activity = activity
        self.category = category

    def activate(self, screen):
        self.image = self.hover
        self.active = True
        self.run(screen)
        return
   
    def run(self, screen):
        self.activity(screen).run() 


MenuItem = ItemActivity


class Menu:
    def __init__(self, pos, content=[]):
        self.pos = pos
        self.content = sprite.OrderedUpdates()
        for item in content:
            self.add(item)

        return

    def get_content(self):
        return self.content.sprites()
    
    def add(self, item):
        #FIXME: Define a mathematical circle function for this 
        if 0 <= len(self.content) <= 1:
            y = 20
            if len(self.content) == 0:
                x = 124
            else:
                x = 559
        elif 2 <= len(self.content) <= 3:
            y = 90
            if len(self.content) == 2:
                x = 62
            else:
                x = 615
        elif 4 <= len(self.content) <= 5:
            y = 160
            if len(self.content) == 4:
                x = 30
            else:
                x = 635
        elif 6 <= len(self.content) <= 7:
            y = 230
            if len(self.content) == 6:
                x = 35
            else:
                x = 630
        elif 8 <= len(self.content) <= 9:
            y = 300
            if len(self.content) == 8:
                x = 55
            else:
                x = 580

        item.place((x, y))
        self.content.add(item)
        return
   
    def draw(self, surface):
        self.content.draw(surface)        
        return


class MenuActivity(Menu):
    def add(self, item):
        sep = 10
        width = item.rect[2]
        hight = item.rect[3]
        if len(self.content) % 2 != 0:
            x = self.pos[0] + width + sep
            y = self.pos[1] + sep + (len(self.content) / 2) * hight
        else:
            x = self.pos[0]
            y = self.pos[1] + sep + (len(self.content) / 2) * hight

        item.place((x, y))
        self.content.add(item)
        return

   
class MainMenu(Activity):
    """Main class for elements in the main menu"""
    def __init__(self, screen, items):
        Activity.__init__(self, screen)
        self.screen = screen
        
        # Position of the categories menu
        self.cat_pos = (675, 60)
        
        # Position of the activities menu
        self.act_pos = (270, 85)

        # items holds the categories
        self.menu = Menu(self.cat_pos)

        # submenus holds the different activities separated by category
        self.submenus = {}

        # Wich category is active
        self.active = None

        if items:
            for item in items:
                if not self.submenus.has_key(item.category):
                    submenu = MenuActivity(self.act_pos)
                    self.submenus[item.category] = submenu
                self.submenus[item.category].add(item)

            for item in self.submenus.keys():
                self.menu.add(ItemCategory(item, self.cat_pos))

        introduction = (u"Este contenido educativo", 
                        u"está diseñado con actividades ", 
                        u"lúdicas para la adquisición de ",
                        u"conceptos y hábitos que contribuyen ",
                        u"a formar niñas y niños saludables.",
                        u" ",
                        u"Esperamos que pases momentos ",
                        u"agradables divertidos ",
                        u"mientras aprendes.")

        font_default = pygame.font.SysFont(constants.font_default[0],
                                           constants.font_default[1])

        isize = font_default.size(introduction[0])[1]

        introduction_pos = (constants.screen_mode[0] / 2.0 + 3, 100)
        
        introduction_ = []
        for i in introduction:
            line = font_default.render(i, True, (102, 102, 102))
            introduction_.append(line)
        self.text = ((introduction_, introduction_pos),)

        self.finger = Finger()
        self.sprites = pygame.sprite.Group()
        self.icons = pygame.sprite.Group()
        self.icons.add([Icons('stop')])
        self.sprites.add((self.finger, self.icons))
        
        self.pos = None
        return
        
    def handle_events(self):
        for event in self.get_event():
            if event.type == QUIT:
                self.quit = True
                return
            elif event.type == KEYUP:
                if event.key == K_F4 and KMOD_ALT & event.mod:
                    self.quit = True
                    return
            elif event.type == MOUSEBUTTONDOWN:
                if pygame.sprite.spritecollideany(self.finger, self.icons):
                    self.quit = True
                    return
                menu_sel = sprite.spritecollideany(self.finger, self.menu.content)
                if menu_sel:
                    menu_sel.activate()
                    self.active = self.submenus[menu_sel.name]

                if self.active:
                    submenu_sel = sprite.spritecollideany(self.finger, 
                                                          self.active.get_content())

                    if submenu_sel:
                        submenu_sel.activate(self.screen)

            self.pos = mouse.get_pos()
            self.changed = True
                
        return

    def setup(self):
        self.draw_text()

    def on_change(self):
        self.sprites.update()        

        self.menu.draw(self.screen)
        if self.active:
            self.active.draw(self.screen)
        else:
            self.draw_text()
        self.sprites.draw(self.screen)
        self.mprev = self.pos

    def draw_text(self):
        x, y = 0, 0
        for i in self.text:
            center = (i[1][0], i[1][1])
            y = center[1]
            surfaces = i[0]
            for surface in surfaces:
                x = center[0] - surface.get_width() / 2.0
                pos = (x, y)
                self.screen.blit(surface, pos)
                y = y + surface.get_height()

