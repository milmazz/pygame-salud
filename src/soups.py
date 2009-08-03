# -*- coding: utf-8 -*-

import os
import time

import pygame
from pygame.locals import *
from pygame.sprite import Sprite

import constants
from activity import Activity
import common
from icons import Icons

class Letras(Sprite):
    def __init__(self, x, y, letra, id):
        Sprite.__init__(self)
        self.imagen_normal = constants.images_soups+'/'+letra+'_normal.png'
        self.imagen_color  = constants.images_soups+'/'+letra+'_color.png'
        self.image = pygame.image.load(self.imagen_normal)
        self.rect = self.image.get_rect()
        self.rect.move_ip(x, y)
        self.color = 0 #0 normal 1 coloreada 2 terminada
        #self.letra = letra
        self.id = id

    def update(self, mover = (0,0)):
        if self.color == 0:
            self.image = pygame.image.load(self.imagen_normal)
        if self.color == 1:
            self.image = pygame.image.load(self.imagen_color)


class Lapiz(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        #self.image = pygame.image.load(constants.images_soups+"/lapiz.png")
        self.image = pygame.image.load("../data/cursors/gartoon/draw-freehand.png")
        self.rect = self.image.get_rect()

    def update(self, mover):
        if mover[0] - 10 >= 0:
            self.rect.x = mover[0] - 10
        if mover[1] - 45 >= 0:
            self.rect.y = mover[1] - 78


class Puntalapiz(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = pygame.image.load(constants.images_soups+"/puntalapiz.png")
        self.rect = self.image.get_rect()

    def update(self, mover):
        self.rect.x = mover[0]
        self.rect.y = mover[1]


class Palabras(Sprite):
    def __init__(self, x, y, palabra):
        Sprite.__init__(self)
        self.imagen_normal = constants.images_soups+'/'+palabra+'.png'
        self.imagen_raya  = constants.images_soups+'/'+palabra+'_lista.png'
        self.image = pygame.image.load(self.imagen_normal)
        self.rect = self.image.get_rect()
        self.rect.move_ip(x, y)
        self.palabra = palabra

    def update(self, palabra = 'vacio'):
        if palabra == self.palabra:
            self.image = pygame.image.load(self.imagen_raya)


class SoupActivity(Activity):
    def limpiar_letras_incorrectas(self, lista_coloreadas, palabras):
        #usando los identificadores de las letras
        #verificamos si son las correctas
        #la variable check si es 0 no es correcta la palabra
        self.check = 1
        self.lista_ordenada = list()
        #palabras correctas
        #vista, gusto, tacto, olfato, oido
        self.tamano_lista = len(lista_coloreadas)
        #verificamos el tamano de la lista.
        if self.tamano_lista >= 4 and self.tamano_lista <= 6:
            #ordenos la lista por los id
            aux = sorted(lista_coloreadas, self.comparar)
            for i in range(self.tamano_lista):
                self.lista_ordenada.append(aux[i].id)
            #oido
            if self.tamano_lista == 4 and self.lista_ordenada == [32,33,34,35]:
                self.check = 2
                self.palabras.update("oido")
            #vista
            elif self.tamano_lista == 5 and self.lista_ordenada == [19,20,21,22,23]:
                self.check = 2
                self.palabras.update("vista")
            #gusto
            elif self.tamano_lista == 5 and self.lista_ordenada == [3,4,5,6,7]:
                self.check = 2
                self.palabras.update("gusto")
            #tacto
            elif self.tamano_lista == 5 and self.lista_ordenada == [51,52,53,54,55]:
                self.check = 2
                self.palabras.update("tacto")
            #olfato
            elif self.tamano_lista == 6 and self.lista_ordenada == [56,57,58,59,60,61]:
                self.check = 2
                self.palabras.update("olfato")
            elif self.check != 2:
                self.check = 0
        else:
            self.check = 0
        #en caso que la palabra este mal se 
        #borrar las marcadas
        if self.check == 0:
            for item in lista_coloreadas:
                item.color = 0

    def comparar(self, a, b):
        return cmp(int(a.id), int(b.id))

    def __init__(self, screen):
        Activity.__init__(self, screen)

    def informative_text(self):
        if pygame.font:
            font = pygame.font.SysFont('dejavusans', 32)
            font.set_bold(True)
            text = font.render("En busca de los cinco sentidos", 1, (0, 0, 0))
            textRect = text.get_rect()
            textRect.centerx = self.screen.get_rect().centerx
            textRect.centery = 20
            self.screen.blit(text, textRect)


            font = pygame.font.SysFont("dejavusans", 20)
            font.set_bold(False)
            instructions = [u"Busca los cinco sentidos en la sopa de letra y marca con",
                            u"el lápiz cada palabra."]
            y = 40
            for line in instructions:
                text = font.render(line, 1,(0, 0, 0))
                self.screen.blit(text, (20, y))
                y+=20
            
        
    def setup_background(self):
        self.background = pygame.image.load(constants.illustration_003).convert_alpha()

    def setup(self):
        self.lapiz = Lapiz()
        self.puntalapiz = Puntalapiz()
        #ocultamos el puntero del raton 
        pygame.mouse.set_visible( False )
        #grupos de sprite
        self.sprites  = pygame.sprite.OrderedUpdates()
        self.letras   = pygame.sprite.Group()
        self.palabras = pygame.sprite.Group()
        self.icons    = pygame.sprite.Group()
        self.icons.add([Icons('stop')])
        ### variables generales ###
        self.mouse_down = 0 
        self.final_pos = (0,0)
        self.pos_x = 320 #posicion inicial de las letras X
        pos_y = 230 #posicion inicial de las letras Y
        tam_x = 45  #tamano de los cuadros ancho
        tam_y = 45  #tamano de los cuadros alto
        self.lista = list() #lista de letras que estan coloreadas
        self.informative_text() 
        #agregar las letras sprite al grupo
        letrasM = 'ydvgustojjrihrufimlvistadrywttemoIdotcxtianacmunonotactoolfatoat'
        for i in range(8):
            for j in range(8):
                self.letras.add([Letras(self.pos_x + tam_x * j, \
                  pos_y + tam_y * i, letrasM[j + i * 8], j + i * 8)])
           
        self.palabras.add([Palabras(110, 370, 'vista'), Palabras(117, 400, 'gusto'), \
          Palabras(108, 430, 'tacto'), Palabras(117, 460, 'oido'), \
          Palabras(104, 490, 'olfato')])
        
        self.sprites.add([self.icons, self.letras, self.lapiz, self.puntalapiz, self.palabras])
        self.sprites.update((0,0))
        self.sprites.draw(self.screen)

        done = False

    def handle_events(self):
            for event in [ pygame.event.wait() ] + pygame.event.get():
                if event.type == QUIT:
                    self.quit = True
                    return
                elif event.type == KEYUP:
                   if event.key == K_ESCAPE:
                       self.quit = True
                       return
                elif event.type == MOUSEBUTTONDOWN:
                    if pygame.sprite.spritecollideany\
                      (self.puntalapiz, self.icons):
                        self.quit = True
                        return
                    self.mouse_down = 1 #se presiono el boton del mouse
                elif event.type == MOUSEMOTION:
                    self.final_pos = pygame.mouse.get_pos() #posicion del puntero del mouse
                    if self.mouse_down == 1 and self.final_pos[0] > self.pos_x:
                        letra_coloreada = pygame.sprite.spritecollideany \
                          (self.puntalapiz, self.letras)
                        #si estamos sobre una letra y esta no esta coloreada
                        #la coloreamos
                        if letra_coloreada and letra_coloreada.color != 1:
                            letra_coloreada.color = 1 #la coloreamos
                            letra_coloreada.update()   #actualizamos la imagen de la letra
                            self.lista.append(letra_coloreada)
                    self.lapiz.update(self.final_pos)
                    self.puntalapiz.update(self.final_pos)
                    self.screen.blit(self.background, (0, 0)) #pintamos el fondo
                    self.sprites.draw(self.screen) #dibujar los sprite
                elif event.type == MOUSEBUTTONUP:
                    self.mouse_down = 0 #se solto el boton del mouse
                    self.limpiar_letras_incorrectas(self.lista, self.palabras)
                    #limpiar la lista
                    self.lista = list()
                    self.screen.blit(self.background, (0, 0))
                    self.sprites.update(self.final_pos)
                    self.sprites.draw(self.screen)
                self.informative_text()
                pygame.display.update() #actualizar la pantalla


class SoupActivity2(Activity):
    def limpiar_letras_incorrectas(self, lista_coloreadas, palabras):
        #usando los identificadores de las letras
        #verificamos si son las correctas
        #la variable check si es 0 no es correcta la palabra
        self.check = 1
        self.lista_ordenada = list()
        #palabras correctas
        #vista, gusto, tacto, olfato, oido
        self.tamano_lista = len(lista_coloreadas)
        #verificamos el tamano de la lista.
        if self.tamano_lista >= 3 and self.tamano_lista <= 8:
            #ordenos la lista por los id
            aux = sorted(lista_coloreadas, self.comparar)
            for i in range(self.tamano_lista):
                self.lista_ordenada.append(aux[i].id)
            #luz
            if self.tamano_lista == 3 and self.lista_ordenada == [57,58,59]:
                self.check = 2
                palabras.update("luz")
            #aire
            elif self.tamano_lista == 4 and self.lista_ordenada == [8,9,10,11]:
                self.check = 2
                palabras.update("aire")
            #agua
            elif self.tamano_lista == 4 and self.lista_ordenada == [32,33,34,35]:
                self.check = 2
                palabras.update("agua")
            #suelo
            elif self.tamano_lista == 5 and self.lista_ordenada == [19,20,21,22,23]:
                self.check = 2
                palabras.update("suelo")
            #plantas
            elif self.tamano_lista == 7 and self.lista_ordenada == [1,2,3,4,5,6,7]:
                self.check = 2
                palabras.update("plantas")
            #animales
            elif self.tamano_lista == 8 and self.lista_ordenada == [40,41,42,43,44,45,46,47]:
                self.check = 2
                palabras.update("animales")
            elif self.check != 2:
                self.check = 0
        else:
            self.check = 0
        if self.check == 0:
            for item in lista_coloreadas:
                item.color = 0

    def comparar(self, a, b):
        return cmp(int(a.id), int(b.id))

    def __init__(self, screen):
        Activity.__init__(self, screen)

    def informative_text(self):
        if pygame.font:
            font = pygame.font.SysFont('dejavusans', 32)
            font.set_bold(True)
            text = font.render("Letras escondidas", 1, (0, 0, 0))
            textRect = text.get_rect()
            textRect.centerx = self.screen.get_rect().centerx
            textRect.centery = 20
            self.screen.blit(text, textRect)


            font = pygame.font.SysFont("dejavusans", 20)
            font.set_bold(False)
            instructions = [u"     Encuentra en la sopa de letras las palabras relacionadas",
                            u"con el ambiente que nos rodea. Márcalas con el lápiz."]
            y = 40
            for line in instructions:
                text = font.render(line, 1,(0, 0, 0))
                self.screen.blit(text, (20, y))
                y+=20
 
    def setup_background(self):
        self.background = pygame.image.load(constants.illustration_017).convert_alpha()

    def setup(self):
        self.lapiz = Lapiz()
        self.puntalapiz = Puntalapiz()
        #turn off the mouse pointer
        pygame.mouse.set_visible( False )
        #sprite groups
        self.sprites  = pygame.sprite.OrderedUpdates()
        self.letras   = pygame.sprite.Group()
        self.palabras = pygame.sprite.Group()
        self.icons    = pygame.sprite.Group()
        self.icons.add([Icons('stop')])
        ### General variable ###
        self.mouse_down = 0 
        self.final_pos = (0,0)
        self.pos_x = 215 #posicion inicial de las letras X
        pos_y = 220 #posicion inicial de las letras Y
        tam_x = 38  #tamano de los cuadros ancho
        tam_y = 37  #tamano de los cuadros alto
        self.lista = list() #lista de letras que estan coloreadas
        #display the informative text in the screen
        self.informative_text()
        #Add the letters to the sprite group
        letrasM = 'yplantasairenkefdalsueloouyraiumaguaqeioanimalesqntoaudoaluzatan'
        for i in range(8):
            for j in range(8):
                self.letras.add([Letras(self.pos_x + tam_x * j, \
                  pos_y + tam_y * i, letrasM[j + i * 8], j + i * 8)])
           
        self.palabras.add([Palabras(550, 200, 'plantas'), Palabras(550, 250, 'aire'), \
          Palabras(550, 300, 'agua'), Palabras(550, 350, 'luz'), \
          Palabras(550, 400, 'animales'), Palabras(550, 450, 'suelo')])
        
        self.sprites.add([self.icons, self.letras, self.lapiz, self.puntalapiz, self.palabras])
        self.sprites.update((0,0))
        self.sprites.draw(self.screen)

        done = False

    def handle_events(self):
            for event in [ pygame.event.wait() ] + pygame.event.get():
                if event.type == QUIT:
                    self.quit = True
                    return
                elif event.type == KEYUP:
                   if event.key == K_ESCAPE:
                       self.quit = True
                       return
                elif event.type == MOUSEBUTTONDOWN:
                    if pygame.sprite.spritecollideany\
                      (self.puntalapiz, self.icons):
                        self.quit = True
                        return
                    self.mouse_down = 1 #se presiono el boton del mouse
                elif event.type == MOUSEMOTION:
                    self.final_pos = pygame.mouse.get_pos() #posicion del puntero del mouse
                    if self.mouse_down == 1 and self.final_pos[0] > self.pos_x:
                        letra_coloreada = pygame.sprite.spritecollideany \
                          (self.puntalapiz, self.letras)
                        #si estamos sobre una letra y esta no esta coloreada
                        #la coloreamos
                        if letra_coloreada and letra_coloreada.color != 1:
                            letra_coloreada.color = 1 #la coloreamos
                            letra_coloreada.update()   #actualizamos la imagen de la letra
                            self.lista.append(letra_coloreada)
                    self.lapiz.update(self.final_pos)
                    self.puntalapiz.update(self.final_pos)
                    self.screen.blit(self.background, (0, 0)) #pintamos el fondo
                    self.sprites.draw(self.screen) #dibujar los sprite
                elif event.type == MOUSEBUTTONUP:
                    self.mouse_down = 0 #se solto el boton del mouse
                    self.limpiar_letras_incorrectas(self.lista, self.palabras)
                    #limpiar la lista
                    self.lista = list()
                    self.screen.blit(self.background, (0, 0))
                    self.sprites.update(self.final_pos)
                    self.sprites.draw(self.screen)
                self.informative_text()
                pygame.display.update() #actualizar la pantalla
