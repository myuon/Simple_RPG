#! /usr/bin/python
# -*- coding:utf-8 -*-

import pygame
from pygame.locals import *

from utility import *

import field_chara as fc
import field

GAME_TITLE = u"GIAPRO"

class GameFrame(object):
    def __init__(self, GAME_TITLE, SCREEN):
        pygame.init()
        pygame.display.set_caption(GAME_TITLE)

        self.screen = pygame.display.set_mode(SCREEN.size)
        self.key = []
        self.clock=pygame.time.Clock()
    
    def event(self):
        for event in pygame.event.get():
            if event.type==QUIT: return -1
        if self.key[K_ESCAPE]: return -1
        
    def _step(self):
        pygame.display.update()

        self.key = pygame.key.get_pressed()
        self.clock.tick(60)
        
        if self.event() == -1: return -1

        self.screen.fill((0,0,60))
        return 0
        
    def mainloop(self):
        while self._step() != -1:
            pass

    def quit(self):
        pygame.display.quit()
        pygame.quit()

class System(GameFrame):
    def __init__(self):
        super(System, self).__init__(GAME_TITLE, SCREEN)
        self.map = field.ScrollMap("map.txt")
        
        self.map.add_chara(fc.Player("vx_chara01_a.png"), is_player=True)
        self.map.add_chara(fc.NPC("vx_chara01_a.png", pos=(4,3), chara=(2,0), movable=True))
        self.map.add_chara(fc.NPC("vx_chara01_a.png", pos=(5,3), chara=(1,1)))
        self.map.add_chara(fc.NPC("vx_chara01_a.png", pos=(6,3), chara=(3,1)))

    def key_step(self):
        step = (0, 0)
        if self.key[K_UP]: step = (0, -1)
        elif self.key[K_DOWN]: step = (0, 1)
        elif self.key[K_RIGHT]: step = (1, 0)
        elif self.key[K_LEFT]: step = (-1, 0)
        return step

    def mainloop(self):
        while self._step() != -1:
            self.map.run(self.screen)
            self.map.move(self.key_step())

if __name__ == "__main__":
    game = System()
    game.mainloop()
    game.quit()
