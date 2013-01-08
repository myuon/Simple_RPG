#! /usr/bin/python
# -*- coding:utf-8 -*-

import pygame
from pygame.locals import *

import os

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

def split_image(image, size, offset):
    images = []
    area = image.get_size()

    for i in range(0, area[0], size[0]):
        surface = pygame.Surface(area)
        surface.blit(image, (0,0), (i+offset[0],offset[1],size[0],size[1]))
        surface.set_colorkey(surface.get_at((0,0)), RLEACCEL)
        surface.convert()
        images.append(surface)
    return images
    
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

class Pos(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        return Pos(self.x + other.x, self.y + other.y)
    
    def __str__(self):
        return "({0}, {1})".format(self.x, self.y)

    def to_tuple(self):
        return (self.x, self.y)

