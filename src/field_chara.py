#! /usr/bin/python
# -*- coding:utf-8 -*-

import pygame
from pygame.locals import *

from utility import *

class Chara(object):
    def __init__(self, path, pos, size, offset):
        self.pos = pos
        self.size = Rect(0, 0, 384/12, 384/8)
        
        self.image = []
        images = split_image(load_image(path,-1), self.size.size, (3,4), offset)
        for seq in images:
            self.image.append((seq[1], seq[0], seq[1], seq[2]))
        
        self.direction = DOWN
        
    def move(self, step):
        self.pos += (step[0]*self.size.width, step[1]*self.size.height/2)

    def move_dir(self, step):
        direction = step_dir(step)
        if direction is not None: self.direction = direction
    
        return (self.pos[0]+step[0]*self.size.width, self.pos[1]+step[1]*self.size.height/2)
    
    def draw(self, screen):
        screen.blit(self.image[self.direction][0], self.pos.to_tuple(), area=self.size)

UNIT = 32

class Player(Chara):
    def __init__(self, path, pos=(SCREEN.width/2/UNIT, SCREEN.height/2/UNIT), size=(32, 48), chara=(0,0)):
        super(Player, self).__init__(path, pos, size, chara)
        self.index = IndexMarker(4, interval=15)
        self.index.active()

    def pixel_pos(self): return self.pos[0]*UNIT, self.pos[1]*UNIT
    def locate(self): return self.pixel_pos()[0], self.pixel_pos()[1]-UNIT/2

    def draw(self, screen):
        screen.blit(self.image[self.direction][self.index()], self.locate(), area=self.size)
        self.index.next()
        
    def move(self): pass
    
class NPC(Player):
    def __init__(self, path, pos=(1,1), size=(32, 48), chara=(0,0)):
        super(NPC, self).__init__(path, pos, size, chara)
        
    def draw(self, screen, offset, scroll):
        screen.blit(self.image[self.direction][self.index()], tuple([self.locate(offset)[i]+scroll[i] for i in [0,1]]), area=self.size)
        self.index.next()

    def pixel_pos(self, offset): return (self.pos[0]-offset[0])*UNIT, (self.pos[1]-offset[1])*UNIT
    def locate(self, offset):
        pos = self.pixel_pos(offset)
        return pos[0], pos[1]-UNIT/2

    def move(self): pass
