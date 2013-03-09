#! /usr/bin/python
# -*- coding:utf-8 -*-

import pygame
from pygame.locals import *

import os
import itertools

SCREEN = Rect(0, 0, 640, 480)
DOWN, LEFT, RIGHT, UP = 0, 1, 2, 3
UNIT = 32

def get_path(filename, directory):
    return os.path.join("../data/{0}".format(directory), filename)

def load_image(filename, colorkey=None, alpha=False, directory=None):
    filename = get_path(filename, directory)
    try:
        image = pygame.image.load(filename)
    except pygame.error, message:
        print "Cannot load image:", filename
        raise SystemExit, message

    if alpha: image = image.convert_alpha()
    else: image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image

def split_image(image, size=(UNIT, UNIT), times=(1,1), offset=(0,0)):
    images = []
    area = image.get_size()
    if times == -1:
        times = area[0]/size[0], area[1]/size[1]

    offset = (offset[0]*size[0]*3, offset[1]*size[1]*4)
    for col in range(times[1]):
        colimages = []
        for row in range(times[0]):
            surface = pygame.Surface(area)
            surface.blit(image, (0,0), (row*size[0]+offset[0],col*size[1]+offset[1],size[0],size[1]))
            surface.set_colorkey(surface.get_at((0,0)), RLEACCEL)
            surface.convert()
            colimages.append(surface)
        images.append(colimages)
    return images

def insert_path(p, string):
    p_ = os.path.splitext(p)
    return "{0}_{1}{2}".format(p_[0], string, p_[1])

def step_dir(step):
    direction = None
    if step == (1, 0): direction = RIGHT
    elif step == (-1, 0): direction = LEFT
    elif step == (0, -1): direction = UP
    elif step == (0, 1): direction = DOWN
    
    return direction

def dir_step(direction):
    step = (0, 0)
    if direction == RIGHT: step = (1, 0)
    elif direction == LEFT: step = (-1, 0)
    elif direction == UP: step = (0, -1)
    elif direction == DOWN: step = (0, 1)
    
    return step

def flatten(nested_list):
    return list(itertools.chain(*nested_list))

def slice_by(seq, n):
    new_list = []
    for i in range(len(seq)/n+1):
        new_list.append(seq[i*n:(i+1)*n])
    return new_list

def wise_slice(seq, n, fill=None):
    l = len(seq)
    if l >= n: return seq[:n]
    else: return seq + [fill]*(n-l)

class Bounded(object):
    def __init__(self, limit, is_infinite=False):
        self._index = 0
        self.limit = limit
        self.is_infinite = is_infinite
    
    def next(self):
        self._index += 1
        if self._index+1 >= self.limit:
            if self.is_infinite: self._index = 0
            else: self._index = self.limit-1
            
    def back(self):
        self._index -= 1
        if self._index < 0:
            if self.is_infinite: self._index = self.limit-1
            else: self._index = 0

    def getter(self): return self._index

    def setter(self, n):
        if 0 <= n <= self.limit:
            self._index = n
        else:
            print "accessed self._index["+str(n)+"]"
            raise SystemExit, "Out of range Error"
        
    index = property(getter, setter)

class IndexMarker(object):
    def __init__(self, limit, interval=1):
        self.index = 0
        self.limit = limit
        self.interval = interval
        self.enable = False
        
    def reset(self):
        self.index = 0
    
    def next(self):
        self.index = (self.index+1)%(self.interval*self.limit)
        
    def inactive(self):
        self.enable = False
        
    def active(self):
        self.enable = True
    
    def is_next_end(self):
        return self.index+1 == self.interval*self.limit

    @property
    def pos(self): return (int(self.index/self.interval))%self.limit

class DummyMarker(IndexMarker):
    def __init__(self):
        self.enable = False
        self.index = 0
        
    def reset(self): pass
    def next(self): pass

    @property
    def pos(self): return 1

class ScrollMarker(IndexMarker):
    def __init__(self, limit, interval=1, step=1, stop=100):
        super(ScrollMarker, self).__init__(limit, interval)
        self.direction = DOWN
        self.step = step
        self.stop = IndexMarker(stop) if stop>0 else DummyMarker()
    
    @property
    def pos(self):
        idx = super(ScrollMarker, self).pos
        sx, sy = dir_step(self.direction)
        return (-sx)*idx, (-sy)*idx
    
    def next(self):
        if self.stop.enable:
            self.stop.next()
            if self.stop.index == 0: self.stop.inactive()

        if not self.stop.enable or isinstance(self.stop, DummyMarker):
            self.index = (self.index+self.step)%(self.interval*self.limit)
            if self.index == 0:
                self.inactive()
                self.stop.active()
        return self.enable
    
    def is_stack(self): return self.stop.enable

class Manager(object):
    def __init__(self):
        self.tickets = []
    
    def add(self, x):
        self.tickets.append(x)
    
    def get(self):
        return self.tickets

    def run(self):
        pass

