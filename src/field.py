#! /usr/bin/python
# -*- coding:utf-8 -*-

import pygame
from pygame.locals import *

from utility import *

class Map(object):
    def __init__(self, filename):
        self.size = Rect(0,0,32,32)
        self.map_to_map = [(1,(0,0)), (0,(0,0)), (0, (0,192)), (0, (0,288)), (0, (32,0))]
        self.image = map(load_image, ["TileA1.png", "TileA2.png"])
        self.block = [1,2,3,4]
        self.data_size, self.default, self.data = self.load(filename)
        
    def load(self, filename):
        data = []
        with open(os.path.join("../data", filename), 'r') as f:
            size = map(int, f.readline().split())
            default = int(f.readline())
            for line in f:
                data.append(map(int, line.rstrip()))
        return size, default, data

    def is_steppable(self,(x,y)):
        return self.data[y][x] not in self.block
    
    def draw_tip(self, screen, col, row):
        f,(x,y) = self.map_to_map[self.data[col][row]]
        screen.blit(self.image[f], (row*self.size.width, col*self.size.height), area=self.size.move(x,y))

    def draw(self, screen):
        for col in range(self.data_size[0]+2):
            for row in range(self.data_size[1]+2):
                self.draw_tip(screen, col-1, row-1)
                
    def block_pos(self,(x,y)):
        return x/self.size.width, y/self.size.height
    
class ScrollMarker(IndexMarker):
    def __init__(self, limit, interval=1, step=1):
        super(ScrollMarker, self).__init__(limit, interval)
        self.direction = None
        self.step = step
    
    def __call__(self):
        idx = super(ScrollMarker, self).__call__()
        sx, sy = dir_step(self.direction)
        return (-sx)*idx, (-sy)*idx
    
    def next(self):
        self.index = (self.index+self.step)%(self.interval*self.max)
        if self.index == 0: self.inactive()
        return self.enable

class ScrollMap(Map):
    def __init__(self, filename, offset=(-9,-6)):
        super(ScrollMap, self).__init__(filename)
        self.offset = offset
        self.pixels = ScrollMarker(self.size.width, interval=1, step=4)

    def draw_tip(self, screen, col, row):
        locate = self.offset[1]+col, self.offset[0]+row
        if 0 <= locate[0] < self.data_size[0] and 0 <= locate[1] < self.data_size[1]:
            tip = self.data[locate[0]][locate[1]]
        else:
            tip = self.default
        f,(x,y) = self.map_to_map[tip]
        px, py = self.pixels()
        screen.blit(self.image[f], (row*self.size.width+px, col*self.size.height+py), area=self.size.move(x,y))

    def is_steppable(self,(x,y)):
        if 0 <= x < self.data_size[1] and 0 <= y < self.data_size[0]:
            tip = self.data[y][x]
        else:
            tip = self.default

        if tip == self.default: return False
        else: return tip not in self.block
    
    def move(self, step, pos):
        if self.pixels.enable:
            if self.pixels.next() == False:
                step_ = dir_step(self.pixels.direction)
                self.offset = self.offset[0]+step_[0], self.offset[1]+step_[1]
        else:
            pos_ = (Pos.from_tuple(self.offset) + Pos.from_tuple(step) + Pos.from_tuple(pos)/Pos.from_tuple(self.size.size)).to_tuple()
            if step != (0,0) and self.is_steppable(pos_):
                self.pixels.active()
                self.pixels.direction = step_dir(step)

