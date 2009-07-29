# vim:ts=4:sts=4:et:nowrap:tw=77
# -*- coding: utf-8 -*-
#########################################################################
##    This library is free software; you can redistribute it and/or
##    modify it under the terms of the GNU Library General Public
##    License as published by the Free Software Foundation; either
##    version 2 of the License, or (at your option) any later version.
##
##    This code is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
##    Library General Public License for more details.
##
## Desarrollador: Rafael Leon Zamorano
## Email: leonza99@gmail.com
##        rleon@ula.ve
#########################################################################

import os
import time

import pygame
from pygame.locals import *
from pygame.sprite import Sprite

import constants
from activity import Activity
import common

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
        self.image = pygame.image.load(constants.images_soups+"/lapiz.png")
        self.rect = self.image.get_rect()

    def update(self, mover):
	    if mover[0] - 10 >= 0:
            self.rect.x = mover[0] - 10
        if mover[1] - 45 >= 0:
            self.rect.y = mover[1] - 45


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
        
    def setup_background(self):
        self.background = pygame.image.load(constants.illustration_003).convert_alpha()
        self.background = pygame.transform.scale(self.background, (800,600))

    def setup(self):
        if pygame.font:
            font = pygame.font.Font(None, 40)
            font.set_bold(True)
            text = font.render("En busca de los cinco sentidos", 1, (0, 0, 0))
            self.screen.blit(text, (10, 10))
            
            font = pygame.font.Font(None, 32)
            font.set_bold(False)
            text = font.render("Busca los cinco sentidos en la sopa de letras y", \
            1,(0, 0, 0))
            self.screen.blit(text, (50, 40))

            text = font.render("marca cada palabra", 1,(0, 0, 0))
            self.screen.blit(text, (50, 60))

        self.lapiz = Lapiz()
        self.puntalapiz = Puntalapiz()
        #ocultamos el puntero del raton 
        pygame.mouse.set_visible( True )
        #grupos de sprite
        self.sprites  = pygame.sprite.OrderedUpdates()
        self.letras   = pygame.sprite.Group()
        self.palabras = pygame.sprite.Group()
        ### variables generales ###
        self.mouse_down = 0 
        self.pos_x = 320 #posicion inicial de las letras X
        pos_y = 230 #posicion inicial de las letras Y
        tam_x = 45  #tamano de los cuadros ancho
        tam_y = 45  #tamano de los cuadros alto
        self.lista = list() #lista de letras que estan coloreadas
       
        #agregar las letras sprite al grupo
        letrasM = 'ydvgustojjrihrufimlvistadrywttemoidotcxtianacmunonotactoolfatoat'
        for i in range(8):
            for j in range(8):
                self.letras.add([Letras(self.pos_x + tam_x * j, \
                  pos_y + tam_y * i, letrasM[j + i * 8], j + i * 8)])
           
        self.palabras.add([Palabras(110, 370, 'vista'), Palabras(117, 400, 'gusto'), \
          Palabras(108, 430, 'tacto'), Palabras(117, 460, 'oido'), \
          Palabras(104, 490, 'olfato')])
        
        self.sprites.add([self.letras, self.lapiz, self.puntalapiz, self.palabras])
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
                pygame.display.update() #actualizar la pantalla
