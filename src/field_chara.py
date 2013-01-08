#! /usr/bin/python
# -*- coding:utf-8 -*-

import pygame
from pygame.locals import *

from utility import *

DOWN, LEFT, RIGHT, UP = 0, 1, 2, 3

class Chara(object):
    def __init__(self, path, pos=(0,0), size=(32, 48)):
        self.pos = Pos(pos[0], pos[1])
        self.image = load_image(path,-1)
        self.size = Rect(0, 0, 384/12, 384/8)
        
        self.direction = DOWN
        
    def move(self, step):
        self.pos += Pos(step[0]*self.size.width, step[1]*self.size.height/2)

    def move_pos(self, step):
        if step == (1, 0): self.direction = RIGHT
        elif step == (-1, 0): self.direction = LEFT
        elif step == (0, -1): self.direction = UP
        elif step == (0, 1): self.direction = DOWN
    
        return (self.pos + Pos(step[0]*self.size.width, step[1]*self.size.height/2)).to_tuple()
    
    def draw(self, screen):
        screen.blit(self.image, self.pos.to_tuple(), area=self.size)

class Player(Chara):
    def __init__(self, path, pos=(0,0), size=(32, 48), offset=(0,0)):
        self.pos = Pos(pos[0], pos[1])
        self.size = Rect(0, 0, size[0], size[1])
        self.index = BookMarker(4, interval=15)

        self.image = []
        images = split_image(load_image(path,-1), self.size.size, (3,4), offset)
        for seq in images:
            self.image.append((seq[1], seq[0], seq[1], seq[2]))
        
        self.direction = DOWN

    def draw(self, screen):
        screen.blit(self.image[self.direction][self.index()], (self.pos - Pos(0, 32)).to_tuple(), area=self.size)
        self.index.next()
        
