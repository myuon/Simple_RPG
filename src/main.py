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
        self.player = fc.Player("vx_chara01_a.png")
        self.map = field.ScrollMap("map.txt")

    def key_step(self):
        step = (0, 0)
        if self.key[K_UP]: step = (0, -1)
        elif self.key[K_DOWN]: step = (0, 1)
        elif self.key[K_RIGHT]: step = (1, 0)
        elif self.key[K_LEFT]: step = (-1, 0)
        return step

    def mainloop(self):
        while self._step() != -1:
            self.map.draw(self.screen)
            self.player.draw(self.screen)
            
            step = self.key_step()
            self.map.move(step, self.player.pos.to_tuple())
            self.player.move_pos(step)

if __name__ == "__main__":
    game = System()
    game.mainloop()
    game.quit()
