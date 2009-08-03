# vim:ts=4:sts=4:et:nowrap:tw=77
# -*- coding: utf-8 -*-

import os

import pygame
from pygame import *
from pygame.locals import *

import constants
import common
from activity import Activity

class Finger(sprite.Sprite):
    """This class define the mouse sprite"""
    def __init__(self):
        sprite.Sprite.__init__(self) 
        self.image, self.rect = common.load_image(constants.cursor_filename)
        mouse.set_pos(700.0, 550.0)

    def update(self):
        pos = mouse.get_pos()
        self.rect.midtop = pos


class ItemBase(sprite.Sprite):
    def __init__(self, name, pos=(0,0)):
        sprite.Sprite.__init__(self)
        path = os.path.join(constants.data_folder, 'menu', name)
        if os.path.exists(path):
            self.normal, self.rect = common.load_image(path + ".png")
            self.hover, self.rect = common.load_image(path + "_hover.png")
            self.active, self.rect = common.load_image(path + "_hover.png")
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
    def __init__(self, pos, width_item, hight_item, content=[]):
        self.pos = pos
        self.width_item = width_item
        self.hight_item = hight_item
        self.content = sprite.OrderedUpdates()
        for item in content:
            self.add(item)

        return

    def get_content(self):
        return self.content.sprites()
    
    def add(self, item):
        x = self.pos[0]
        y = self.pos[1] + len(self.content) * self.hight_item

        item.place((x, y))
        self.content.add(item)
        return
   
    def draw(self, surface):
        self.content.draw(surface)        
        return


class MenuActivity(Menu):
    def add(self, item):
        sep = 5
        width = item.rect[2]
        hight = item.rect[3]
        if len(self.content) % 2 != 0:
            x = self.pos[0] + width + sep
            y = self.pos[1] + sep + len(self.content)/2 * hight
        else:
            x = self.pos[0]
            y = self.pos[1] + sep + len(self.content)/2 * hight

        item.place((x, y))
        self.content.add(item)
        return

   
class MainMenu(Activity):
    """Main class for elements in the main menu"""
    def __init__(self, screen, items):
        Activity.__init__(self, screen)
        self.screen = screen
        
        # Position of the categories menu
        self.cat_pos = (550, 50)
        
        # Position of the activities menu
        self.act_pos = (50, 50)

        # items holds the categories
        self.menu = Menu(self.cat_pos, 200, 100)

        # submenus holds the different activities separated by category
        self.submenus = {}

        # Wich category is active
        self.active = None

        if items:
            for item in items:
                if not self.submenus.has_key(item.category):
                    submenu = MenuActivity(self.act_pos, 50, 50)
                    self.submenus[item.category] = submenu
                self.submenus[item.category].add(item)

            for item in self.submenus.keys():
                self.menu.add(ItemCategory(item, self.cat_pos))

        self.finger = Finger()
        self.cursor = sprite.RenderPlain((self.finger))
        
        self.pos = None
        return
        
    def handle_events(self):
        event = pygame.event.wait()
        if event.type == QUIT:
            self.quit = True
            return
        elif event.type == KEYUP:
            if event.key == K_F4 and KMOD_ALT & event.mod:
                self.quit = True
                return
        elif event.type == MOUSEBUTTONDOWN:
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
        if self.pos != self.mprev:
            self.changed = True
            
        return

    def on_change(self):
        self.cursor.update()        

        self.menu.draw(self.screen)
        if self.active:
            self.active.draw(self.screen)
        self.cursor.draw(self.screen)
        self.mprev = self.pos
