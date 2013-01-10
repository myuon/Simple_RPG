#! /usr/bin/python
# -*- coding:utf-8 -*-

import pygame
from pygame.locals import *

import os

SCREEN = Rect(0, 0, 640, 480)
DOWN, LEFT, RIGHT, UP = 0, 1, 2, 3
UNIT = 32

def load_image(filename, colorkey=None):
    filename = os.path.join("../data", filename)
    try:
        image = pygame.image.load(filename)
    except pygame.error, message:
        print "Cannot load image:", filename
        raise SystemExit, message

    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image

def split_image(image, size, times, offset):
    images = []
    area = image.get_size()

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

class IndexMarker(object):
    def __init__(self, limit, interval=1):
        self.index = 0
        self.max = limit
        self.interval = interval
        self.enable = False
        
    def reset(self):
        self.index = 0
    
    def next(self):
        self.index = (self.index+1)%(self.interval*self.max)
        
    def inactive(self):
        self.enable = False
        
    def active(self):
        self.enable = True

    def __call__(self):
        return (self.index/self.interval)%self.max

class DummyMarker(IndexMarker):
    def __init__(self):
        self.enable = False
        self.index = 0
        
    def reset(self): pass
    def next(self): pass
    def __call__(self): return 0

class ScrollMarker(IndexMarker):
    def __init__(self, limit, interval=1, step=1, stop=100):
        super(ScrollMarker, self).__init__(limit, interval)
        self.direction = None
        self.step = step
        self.stop = IndexMarker(stop) if stop>0 else DummyMarker()
    
    def __call__(self):
        idx = super(ScrollMarker, self).__call__()
        sx, sy = dir_step(self.direction)
        return (-sx)*idx, (-sy)*idx
    
    def next(self):
        if self.stop.enable:
            self.stop.next()
            if self.stop.index == 0: self.stop.inactive()

        if not self.stop.enable or isinstance(self.stop, DummyMarker):
            self.index = (self.index+self.step)%(self.interval*self.max)
            if self.index == 0:
                self.inactive()
                self.stop.active()
        return self.enable
    
    def is_stack(self): return self.stop.enable

class Manager(object):
    def __init__(self):
        self.objects = []
    
    def add(self, x):
        self.objects.append(x)
    
    def get(self):
        return self.objects

    def run(self):
        pass

