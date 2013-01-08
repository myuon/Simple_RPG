#! /usr/bin/python
# -*- coding:utf-8 -*-

import pygame
from pygame.locals import *

from utility import *

GAME_TITLE = u"GIAPRO"
SCREEN = Rect(0, 0, 640, 480)

maptip = [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
          [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
          [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
          [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
          [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
          [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
          [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
          [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
          [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
          [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
          [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
          [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
          [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
          [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
          [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]

class Map(object):
    def __init__(self):
        self.size = Rect(0,0,32,32)
        self.map_to_map = [(1,(0,0)), (0,(0,0))]
        self.image = map(load_image, ["TileA1.png", "TileA2.png"])
        self.data = maptip
        self.block = [1]
        
    def is_steppable(self,(x,y)):
        return self.data[y][x] not in self.block

    def draw(self, screen):
        for col in range(len(self.data)):
            for i in range(len(self.data[col])):
                (f,(x,y)) = self.map_to_map[self.data[col][i]]
                screen.blit(self.image[f], (i*self.size.width, col*self.size.height), area=self.size.move(x,y))
                
    def block_pos(self,(x,y)):
        return x/self.size.width, y/self.size.height

class Chara(object):
    def __init__(self, path, (x,y)=(0,0)):
        self.pos = Pos(x,y)
        self.image = load_image(path,-1)
        self.size = Rect(0, 0, 384/12, 384/8)
        
    def move(self, (bx,by)):
        self.pos += Pos(bx*self.size.width, by*self.size.height/2)
    
    def move_pos(self, (bx,by)):
        return (self.pos + Pos(bx*self.size.width, by*self.size.height/2)).to_tuple()
    
    def draw(self, screen):
        screen.blit(self.image, self.pos.to_tuple(), area=self.size)

class BookMarker(object):
    def __init__(self, limit, interval=1):
        self.index = 0
        self.max = limit
        self.interval = interval
        
    def next(self):
        self.index = (self.index+1)%(self.interval*self.max)

    def __call__(self):
        return (self.index/self.interval)%self.max

class Player(Chara):
    def __init__(self, path, pos=(0,0), size=(32, 48), offset=(0,0)):
        self.pos = Pos(pos[0], pos[1])
        self.size = Rect(0, 0, size[0], size[1])
        self.index = BookMarker(4, interval=15)

        images = split_image(load_image(path,-1), self.size.size, \
                            offset=(offset[0]*size[0]*3, offset[1]*size[1]*4))
        self.image = [images[1], images[0], images[1], images[2]]
        
    def draw(self, screen):
        screen.blit(self.image[self.index()], self.pos.to_tuple(), area=self.size)
        self.index.next()
        
class Manager(object):
    def __init__(self):
        self.todo = []
    
    def add(self, x):
        self.todo.append(x)
    
    def get(self):
        return self.todo

    def execute(self):
        pass

class System(GameFrame):
    def __init__(self):
        super(System, self).__init__(GAME_TITLE, SCREEN)
        self.player = Player("vx_chara01_a.png", pos=(32,48))
        self.map = Map()
        
    def key_event(self):
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

            step = self.key_event()
            if step != (0, 0) and self.map.is_steppable(self.map.block_pos(self.player.move_pos(step))):
                self.player.move(step)

if __name__ == "__main__":
    game = System()
    game.mainloop()
    game.quit()
