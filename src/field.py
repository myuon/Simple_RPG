#! /usr/bin/python
# -*- coding:utf-8 -*-

import pygame
from pygame.locals import *

from utility import *

class Map(object):
    def __init__(self, filename):
        self.size = Rect(0,0,32,32)
        self.map_to_map = [(1,(0,0)), (0,(0,0))]
        self.image = map(load_image, ["TileA1.png", "TileA2.png"])
        self.block = [1]
        self.data_size, self.data = self.load(filename)
        
    def load(self, filename):
        data = []
        with open(os.path.join("../data", filename), 'r') as f:
            size = map(int, f.readline().split())
            for line in f:
                data.append(map(int, line.rstrip()))
        return size, data

    def is_steppable(self,(x,y)):
        return self.data[y][x] not in self.block

    def draw(self, screen):
        for col in range(self.data_size[0]):
            for row in range(self.data_size[1]):
                (f,(x,y)) = self.map_to_map[self.data[col][row]]
                screen.blit(self.image[f], (row*self.size.width, col*self.size.height), area=self.size.move(x,y))
                
    def block_pos(self,(x,y)):
        return x/self.size.width, y/self.size.height

