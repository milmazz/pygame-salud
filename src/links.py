# vim:ts=4:sts=4:et:nowrap:tw=77
# -*- coding: utf-8 -*-

import sys
import pygame

import constants
import common
from activity import Activity

# Activity 7
class Shower(Activity):
    def __init__(self, screen):
        Activity.__init__(self, screen)
        self.items_rect = {
                'towel': pygame.Rect(260, 186, 102, 100),
                'shampoo': pygame.Rect(170, 295, 80, 85),
                'brush': pygame.Rect(285, 385, 105, 65),
                'soap': pygame.Rect(195, 498, 90, 65),
                'hair': pygame.Rect(507, 227, 74, 65),
                'body': pygame.Rect(491, 365, 94, 82),
                'mouth': pygame.Rect(500, 510, 73, 42),
                }

        self.selections = []
        # TODO change the mouse
	    pygame.mouse.set_visible(True)

    def setup_background(self):
        self.background = pygame.image.load(constants.illustration_007)

    def setup(self):
        font_title = pygame.font.SysFont("dejavusans", 48)
        font_instructions = pygame.font.SysFont("dejavusans", 24)

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
            
    def handle_events(self):
        selection = [(0, 0), (0, 0)]
        self.startline = None

        while True:
            self.clock.tick(300)

            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                self.quit = True
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.endline = self.startline = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEMOTION \
                    and pygame.mouse.get_pressed()[0]:

                if self.startline == None:
                    self.endline = self.startline = pygame.mouse.get_pos()
                else:
                    self.endline = pygame.mouse.get_pos()

                self.update_screen()
                pygame.draw.aaline(self.screen, (120, 120, 120), 
                                   self.startline, self.endline)
                self.selection = self.startline, self.endline
            
            elif event.type == pygame.MOUSEBUTTONUP:
                self.validate_selection()
            
            pygame.display.flip()

    def update_screen(self):
        self.setup()

        if self.selections:
            for (start, end), color in self.selections:
                pygame.draw.aaline(self.screen, color, start, end, 0)


    def validate_selection(self):
        selection = self.selection
        if self.items_rect['towel'].collidepoint(selection[0]) \
                and self.items_rect['body'].collidepoint(selection[1]) \
                or self.items_rect['towel'].collidepoint(selection[1]) \
                and self.items_rect['body'].collidepoint(selection[0]) \
                or self.items_rect['shampoo'].collidepoint(selection[0]) \
                and self.items_rect['hair'].collidepoint(selection[1]) \
                or self.items_rect['shampoo'].collidepoint(selection[1]) \
                and self.items_rect['hair'].collidepoint(selection[0]) \
                or self.items_rect['brush'].collidepoint(selection[0]) \
                and self.items_rect['mouth'].collidepoint(selection[1]) \
                or self.items_rect['brush'].collidepoint(selection[1]) \
                and self.items_rect['mouth'].collidepoint(selection[0]) \
                or self.items_rect['soap'].collidepoint(selection[0]) \
                and self.items_rect['body'].collidepoint(selection[1]) \
                or self.items_rect['soap'].collidepoint(selection[1]) \
                and self.items_rect['body'].collidepoint(selection[0]):
                    self.selections.append((selection, (100, 150, 255)))
        else:
            self.selections.append((selection, (255, 100, 100)))
