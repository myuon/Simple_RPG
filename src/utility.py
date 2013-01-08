#! /usr/bin/python
# -*- coding:utf-8 -*-

import pygame
from pygame.locals import *

import os

SCREEN = Rect(0, 0, 640, 480)
DOWN, LEFT, RIGHT, UP = 0, 1, 2, 3

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

class Pos(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        return Pos(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Pos(self.x - other.x, self.y - other.y)
    
    def __mul__(self, other):
        return Pos(self.x * other.x, self.y * other.y)
    
    def __div__(self, other):
        return Pos(self.x / other.x, self.y / other.y)
    
    def __str__(self):
        return "({0}, {1})".format(self.x, self.y)

    def to_tuple(self):
        return (self.x, self.y)

    @staticmethod
    def from_tuple((x,y)):
        return Pos(x,y)

class IndexMarker(object):
    def __init__(self, limit, interval=1):
        self.index = 0
        self.max = limit
        self.interval = interval
        self.enable = False
        
    def next(self):
        self.index = (self.index+1)%(self.interval*self.max)
        
    def inactive(self):
        self.enable = False
        
    def active(self):
        self.enable = True

    def __call__(self):
        return (self.index/self.interval)%self.max

class Manager(object):
    def __init__(self):
        self.todo = []
    
    def add(self, x):
        self.todo.append(x)
    
    def get(self):
        return self.todo

    def execute(self):
        pass

