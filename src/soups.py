# vim:ts=4:sts=4:et:nowrap:tw=77
# -*- coding: utf-8 -*-

import os
import time

import pygame
import random 
from pygame.locals import *
from pygame.sprite import Sprite

import constants
from activity import Activity
import common
from icons import Icons

class Letters(Sprite):
    def __init__(self, pos, letter, id):
        Sprite.__init__(self)
        image_name = os.path.join(constants.data_folder, "soups", \
                letter + "_normal.png")
        self.image_normal, self.rect = common.load_image(image_name)
        image_name = os.path.join(constants.data_folder, "soups", \
                letter + "_color.png")
        self.image_color, self.rect = common.load_image(image_name)
        self.rect.move_ip(pos)
        self.color = 0 #0 normal 1 coloreada 2 terminada
        self.id = id

    def update(self, mover = (0,0)):
        if self.color == 0:
            self.image = self.image_normal
        if self.color == 1:
            self.image = self.image_color


class Lapiz(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        path = os.path.join(constants.data_folder, "cursors",\
                "gartoon", "draw-freehand.png")
        self.image, self.rect = common.load_image(path)

    def update(self, mover):
        self.rect.bottomleft = mover


class Puntalapiz(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        path = os.path.join(constants.data_folder, "soups", \
                "puntalapiz.png")
        self.image, self.rect = common.load_image(path)

    def update(self, mover):
        self.rect.left, self.rect.bottom = mover[0] + 1, mover[1]


class Words(Sprite):
    def __init__(self, x, y, word):
        Sprite.__init__(self)
        self.path_image_normal = os.path.join(constants.data_folder, \
                "soups", word + ".png")
        self.path_image_done = os.path.join(constants.data_folder, \
                "soups", word + "_done.png")
        self.image, self.rect = common.load_image(self.path_image_normal)
        self.rect.move_ip(x, y)
        self.word = word

    def update(self, word = 'vacio'):
        if word == self.word:
            self.image = common.load_image(self.path_image_done)[0]


class SoupActivity(Activity):
    def random_position(self):
        randomSelection = random.randrange(0,5)
        if randomSelection == 0:
            self.lettersM = \
                    'ydvgustojjrihrufimlvistadrywttemoIdotcxtianacmunonotactoolfatoat'
            self.oidoPos = [32,33,34,35]
            self.vistaPos = [19,20,21,22,23]
            self.gustoPos = [3,4,5,6,7]
            self.tactoPos = [51,52,53,54,55]
            self.olfatoPos = [56,57,58,59,60,61]
        if randomSelection == 1:
            self.lettersM = \
                    'gderoyuiufgtIuhjsuyhdtrotgtyojulvistapofzzxnmkgawetactotgustojho'
            self.oidoPos = [4, 12, 20, 28]
            self.vistaPos = [32, 33, 34, 35, 36]
            self.gustoPos = [56, 57, 58, 59, 60]
            self.tactoPos = [50, 51, 52, 53, 54]
            self.olfatoPos = [23, 31, 39, 47, 55, 63]
        if randomSelection == 2:
            self.lettersM = \
                    'gbvpouosudcxswlbswsazxfvttactoaioidxhntsoIdodcotsccbbghanhytgfre'
            self.oidoPos = [40, 41, 42, 43]
            self.vistaPos = [23, 31, 39, 47, 55]
            self.gustoPos = [0, 8, 16, 24, 32]
            self.tactoPos = [25, 26, 27, 28, 29]
            self.olfatoPos = [6, 14, 22, 30, 38, 46]
        if randomSelection == 3:
            self.lettersM = \
                    'vistafjoohnjgrfIlnbvcxxdffvtgbhoagustotgttyuiootoujhgbvttactovtb'
            self.oidoPos = [7, 15, 23, 31]
            self.vistaPos = [0, 1, 2, 3, 4]
            self.gustoPos = [33, 34, 35, 36, 37]
            self.tactoPos = [56, 57, 58, 59, 60]
            self.olfatoPos = [8, 16, 24, 32, 40, 48]
        if randomSelection == 4:
            self.lettersM = \
                    'olfatoctlasasddaolkjmnhcoIdovghtiujhgbbopoivistamgustodtoiujhggd'
            self.oidoPos = [24, 25, 26, 27]
            self.vistaPos = [43, 44, 45, 46, 47]
            self.gustoPos = [49, 50, 51, 52, 53]
            self.tactoPos = [7, 15, 23, 31, 39]
            self.olfatoPos = [0, 1, 2, 3, 4, 5]

    def clean_incorrect_letters(self, list_colored, words):
        #usando los identificadores de las letras
        #verificamos si son las correctas
        #la variable check si es 0 no es correcta la word
        self.check = 1
        self.ordered_list = list()
        #words correctas
        #vista, gusto, tacto, olfato, oido
        self.list_size = len(list_colored)
        #verificamos el tamano de la lista.
        if self.list_size >= 4 and self.list_size <= 6:
            #ordenos la lista por los id
            aux = sorted(list_colored, self.compare)
            for i in range(self.list_size):
                self.ordered_list.append(aux[i].id)
            #oido
            if self.list_size == 4 and self.ordered_list == self.oidoPos:
                self.check = 2
                self.words.update("oido")
            #vista
            elif self.list_size == 5 and self.ordered_list == \
                    self.vistaPos:
                        self.check = 2
                        self.words.update("vista")
            #gusto
            elif self.list_size == 5 and self.ordered_list == \
                    self.gustoPos:
                        self.check = 2
                        self.words.update("gusto")
            #tacto
            elif self.list_size == 5 and self.ordered_list == \
                    self.tactoPos:
                        self.check = 2
                        self.words.update("tacto")
            #olfato
            elif self.list_size == 6 and self.ordered_list == \
                    self.olfatoPos:
                        self.check = 2
                        self.words.update("olfato")
            elif self.check != 2:
                self.check = 0
        else:
            self.check = 0
        if self.check == 2:
            self.count += 1
        #en caso que la word este mal se 
        #borrar las marcadas
        if self.check == 0:
            for item in list_colored:
                item.color = 0

    def compare(self, a, b):
        return cmp(int(a.id), int(b.id))

    def __init__(self, screen):
        Activity.__init__(self, screen)

    def informative_text(self):
        if pygame.font:
            font = pygame.font.SysFont('dejavusans', 26)
            text = font.render("En busca de los cinco sentidos", 1, (0, 0, 0))
            textRect = text.get_rect()
            textRect.centerx = self.screen.get_rect().centerx
            textRect.centery = 20
            self.background.blit(text, textRect)
            font = pygame.font.SysFont("dejavusans", 20)
            instructions = [u"Busca los cinco sentidos en la sopa de",
                            u"letras y marca con el lápiz cada palabra."]
            y = 45
            for line in instructions:
                text = font.render(line, 1,(0, 0, 0))
                self.background.blit(text, (350, y))
                y+=20
        
    def setup_background(self):
        self.background = common.load_image(constants.illustration_003)[0]

    def setup(self):
        self.count = 0
        self.lapiz = Lapiz()
        self.puntalapiz = Puntalapiz()
        #ocultamos el puntero del raton 
        pygame.mouse.set_visible( False )
        #grupos de sprite
        self.sprites = pygame.sprite.OrderedUpdates()
        self.letters = pygame.sprite.Group()
        self.words = pygame.sprite.Group()
        self.icons = pygame.sprite.Group()
        self.icons.add([Icons('stop')])
        ### variables generales ###
        self.mouse_down = 0 
        self.final_pos = (0,0)
        self.pos_x = 320 #posicion inicial de las letras X
        pos_y = 230 #posicion inicial de las letras Y
        tam_x = 45  #tamano de los cuadros ancho
        tam_y = 45  #tamano de los cuadros alto
        self.list = list() #lista de letras que estan coloreadas
        self.informative_text() 
        self.random_position()
        #lettersM = 'ydvgustojjrihrufimlvistadrywttemoIdotcxtianacmunonotactoolfatoat'
        for i in range(8):
            for j in range(8):
                self.letters.add([Letters((self.pos_x + tam_x * j, \
                        pos_y + tam_y * i), self.lettersM[j + i * 8], j + i * 8)])
        self.words.add([Words(110, 370, 'vista'), Words(117, 400, 'gusto'), \
                Words(108, 430, 'tacto'), Words(117, 460, 'oido'), \
                Words(104, 490, 'olfato')])
        self.sprites.add([self.icons, self.letters, self.words, self.lapiz, self.puntalapiz])
        self.final_pos = pygame.mouse.get_pos()
        self.lapiz.update(self.final_pos)
        self.puntalapiz.update(self.final_pos)
        self.sprites.update((0,0))
        self.sprites.draw(self.screen)
        done = False

    def handle_events(self):
        for event in self.get_event():
            if event.type == QUIT:
                self.quit = True
                return
            elif event.type == KEYUP:
               if event.key == K_ESCAPE:
                   self.quit = True
                   return
            elif event.type == MOUSEBUTTONDOWN:
                if pygame.sprite.spritecollideany \
                        (self.puntalapiz, self.icons):
                            self.quit = True
                            return
                self.mouse_down = 1 #se presiono el boton del mouse
            elif event.type == MOUSEMOTION:
                self.final_pos = pygame.mouse.get_pos() #posicion del puntero del mouse
                if self.mouse_down == 1 and self.final_pos[0] > self.pos_x:
                    letter_colored = pygame.sprite.spritecollideany \
                            (self.puntalapiz, self.letters)
                    #si estamos sobre una letra y esta no esta coloreada
                    #la coloreamos
                    if letter_colored and letter_colored.color != 1:
                        letter_colored.color = 1 #la coloreamos
                        letter_colored.update()   #actualizamos la imagen de la letra
                        self.list.append(letter_colored)
                self.lapiz.update(self.final_pos)
                self.puntalapiz.update(self.final_pos)
                self.screen.blit(self.background, (0, 0)) #pintamos el fondo
                self.sprites.draw(self.screen) #dibujar los sprite
            elif event.type == MOUSEBUTTONUP:
                self.mouse_down = 0 #se solto el boton del mouse
                self.clean_incorrect_letters(self.list, self.words)
                #limpiar la lista
                self.list = list()
                self.screen.blit(self.background, (0, 0))
                self.sprites.update(self.final_pos)
                self.sprites.draw(self.screen)
            pygame.display.update() #actualizar la pantalla
            if self.count == 5:
                self.finished_ = True


class SoupActivity2(Activity):
    def random_position(self):
        randomSelection = random.randrange(0,4)
        if randomSelection == 0:
            self.lettersM = \
                    'yplantasairenkefdalsueloouyraiumaguaqeioanimalesqntoaudoaluzatan'
            self.luzPos = [57,58,59]
            self.airePos = [8,9,10,11]
            self.aguaPos = [32,33,34,35]
            self.sueloPos = [19,20,21,22,23]
            self.plantasPos = [1,2,3,4,5,6,7]
            self.animalesPos = [40,41,42,43,44,45,46,47]
        if randomSelection == 1:
            self.lettersM =\
                    'airetocalasasddnoluluzhioIeovghmiulhgbbapoovistlaguatodeplantass'
            self.luzPos = [19, 20, 21]
            self.airePos = [0, 1, 2, 3]
            self.aguaPos = [48, 49, 50, 51]
            self.sueloPos = [10, 18, 26, 34, 42]
            self.plantasPos = [56, 57, 58, 59, 60, 61, 62]
            self.animalesPos = [7, 15, 23, 31, 39, 47, 55, 63]
        if randomSelection == 2:
            self.lettersM = \
                    'aguacfrtsuelodcnplantasimjuhgbfcrbnmkloaanimalesuyvcqafeluzaired'
            self.luzPos = [56, 57, 58]
            self.airePos = [59, 60, 61, 62]
            self.aguaPos = [0, 1, 2, 3]
            self.sueloPos = [8, 9, 10, 11, 12]
            self.plantasPos = [16, 17, 18, 19, 20, 21, 22]
            self.animalesPos = [40, 41, 42, 43, 44, 45, 46, 47]
        if randomSelection == 3:
            self.lettersM = \
                    'aairecpanfrfkdlgikrdfcaumfmvmvnaaorkfgtvlluzfbaceunzasswssuelofx'
            self.luzPos = [41, 42, 43]
            self.airePos = [1, 2, 3, 4]
            self.aguaPos = [7, 15, 23, 31]
            self.sueloPos = [57, 58, 59, 60, 61]
            self.plantasPos = [6, 14, 22, 30, 38, 46, 54]
            self.animalesPos = [0, 8, 16, 24, 32, 40, 48, 56]

    def clean_incorrect_letters(self, list_colored, words):
        #usando los identificadores de las letras
        #verificamos si son las correctas
        #la variable check si es 0 no es correcta la word
        self.check = 1
        self.ordered_list = list()
        #words correctas
        #vista, gusto, tacto, olfato, oido
        self.list_size = len(list_colored)
        #verificamos el tamano de la lista.
        if self.list_size >= 3 and self.list_size <= 8:
            #ordenos la lista por los id
            aux = sorted(list_colored, self.compare)
            for i in range(self.list_size):
                self.ordered_list.append(aux[i].id)
            #luz
            if self.list_size == 3 and self.ordered_list == self.luzPos:
                self.check = 2
                words.update("luz")
            #aire
            elif self.list_size == 4 and self.ordered_list == \
                    self.airePos:
                        self.check = 2
                        words.update("aire")
            #agua
            elif self.list_size == 4 and self.ordered_list == \
                    self.aguaPos:
                        self.check = 2
                        words.update("agua")
            #suelo
            elif self.list_size == 5 and self.ordered_list == \
                    self.sueloPos:
                        self.check = 2
                        words.update("suelo")
            #plantas
            elif self.list_size == 7 and self.ordered_list == \
                    self.plantasPos:
                        self.check = 2
                        words.update("plantas")
            #animales
            elif self.list_size == 8 and self.ordered_list == \
                    self.animalesPos:
                        self.check = 2
                        words.update("animales")
            elif self.check != 2:
                self.check = 0
        else:
            self.check = 0
        if self.check == 2:
            self.count += 1
        if self.check == 0:
            for item in list_colored:
                item.color = 0

    def compare(self, a, b):
        return cmp(int(a.id), int(b.id))

    def __init__(self, screen):
        Activity.__init__(self, screen)

    def informative_text(self):
        if pygame.font:
            font = pygame.font.SysFont('dejavusans', 26)
            text = font.render("Letras escondidas", 1, (0, 0, 0))
            textRect = text.get_rect()
            textRect.centerx = self.screen.get_rect().centerx - 120
            textRect.centery = 20
            self.background.blit(text, textRect)
            font = pygame.font.SysFont("dejavusans", 20)
            instructions = [u"     Encuentra en la sopa de letras las",
                            u"palabras relacionadas con el ambiente",
                            u"que nos rodea. Márcalas con el lápiz."]
            y = 40
            for line in instructions:
                text = font.render(line, 1,(0, 0, 0))
                self.background.blit(text, (20, y))
                y+=20
 
    def setup_background(self):
        self.background = common.load_image(constants.illustration_017)[0]

    def setup(self):
        self.count = 0
        self.lapiz = Lapiz()
        self.puntalapiz = Puntalapiz()
        #turn off the mouse pointer
        pygame.mouse.set_visible( False )
        #sprite groups
        self.sprites = pygame.sprite.OrderedUpdates()
        self.letters = pygame.sprite.Group()
        self.words = pygame.sprite.Group()
        self.icons = pygame.sprite.Group()
        self.icons.add([Icons('stop')])
        ### General variable ###
        self.mouse_down = 0 
        self.final_pos = (0,0)
        self.pos_x = 215 #posicion inicial de las letras X
        pos_y = 220 #posicion inicial de las letras Y
        tam_x = 38  #tamano de los cuadros ancho
        tam_y = 37  #tamano de los cuadros alto
        self.list = list() #lista de letras que estan coloreadas
        #display the informative text in the screen
        self.informative_text()
        #Add the letters to the sprite group
        #generate the random seleccion to the final word position
        self.random_position()
        #lettersM = 'yplantasairenkefdalsueloouyraiumaguaqeioanimalesqntoaudoaluzatan'
        for i in range(8):
            for j in range(8):
                self.letters.add([Letters((self.pos_x + tam_x * j, \
                        pos_y + tam_y * i), self.lettersM[j + i * 8], j + i * 8)])
        self.words.add([Words(550, 200, 'plantas'), Words(550, 250, 'aire'), \
                Words(550, 300, 'agua'), Words(550, 350, 'luz'), \
                Words(550, 400, 'animales'), Words(550, 450, 'suelo')])
        self.sprites.add([self.icons, self.letters, self.words, self.lapiz, self.puntalapiz])
        self.final_pos = pygame.mouse.get_pos()
        self.lapiz.update(self.final_pos)
        self.puntalapiz.update(self.final_pos)
        self.sprites.update((0,0))
        self.sprites.draw(self.screen)
        done = False

    def handle_events(self):
        for event in self.get_event():
            if event.type == QUIT:
                self.quit = True
                return
            elif event.type == KEYUP:
               if event.key == K_ESCAPE:
                   self.quit = True
                   return
            elif event.type == MOUSEBUTTONDOWN:
                if pygame.sprite.spritecollideany \
                        (self.puntalapiz, self.icons):
                            self.quit = True
                            return
                self.mouse_down = 1 #se presiono el boton del mouse
            elif event.type == MOUSEMOTION:
                self.final_pos = pygame.mouse.get_pos() #posicion del puntero del mouse
                if self.mouse_down == 1 and self.final_pos[0] > self.pos_x:
                    letter_colored = pygame.sprite.spritecollideany \
                            (self.puntalapiz, self.letters)
                    #si estamos sobre una letra y esta no esta coloreada
                    #la coloreamos
                    if letter_colored and letter_colored.color != 1:
                        letter_colored.color = 1 #la coloreamos
                        letter_colored.update()   #actualizamos la imagen de la letra
                        self.list.append(letter_colored)
                self.lapiz.update(self.final_pos)
                self.puntalapiz.update(self.final_pos)
                self.screen.blit(self.background, (0, 0)) #pintamos el fondo
                self.sprites.draw(self.screen) #dibujar los sprite
            elif event.type == MOUSEBUTTONUP:
                self.mouse_down = 0 #se solto el boton del mouse
                self.clean_incorrect_letters(self.list, self.words)
                #limpiar la lista
                self.list = list()
                self.screen.blit(self.background, (0, 0))
                self.sprites.update(self.final_pos)
                self.sprites.draw(self.screen)
            pygame.display.update() #actualizar la pantalla
            if self.count == 6:
                self.finished_ = True
