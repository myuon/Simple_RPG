#! /usr/bin/python
# -*- coding:utf-8 -*-

import pygame
from pygame.locals import *

from utility import *

class MessageEngine(object):
    def __init__(self, filename):
        self.font = self.load(filename)

    def load(self, filename):
        filename = os.path.join("../data", filename)
        try:
            font = pygame.font.Font(filename, 18)
        except pygame.error, message:
            print "Cannot load font:", filename
            raise SystemExit, message
        return font
    
    def draw(self, screen, message, pos):
        screen.blit(self.font.render(message, True, (255, 255, 255)), pos)

class Layer(object):
    EDGE_WIDTH = 4

    def __init__(self, rect, padding={'top':5, 'left':10, 'bottom':5, 'right':10}):
        self.rect = rect
        self.inner_rect = self.rect.inflate(-self.EDGE_WIDTH*2, -self.EDGE_WIDTH*2)
        self.is_visible = True
        self.padding = padding
        self.pos={'x':self.rect.left+self.padding['left'], 'y':self.rect.top+self.padding['top']}

    def draw(self, screen):
        if self.is_visible == False: return
        pygame.draw.rect(screen, (255,255,255), self.rect, 0)
        pygame.draw.rect(screen, (0,0,0), self.inner_rect, 0)

    def active(self): self.is_visible = True
    def inactive(self): self.is_visible = False

class MessageLayer(Layer):
    def __init__(self, filename, rect, padding={'top':5, 'left':10, 'bottom':5, 'right':10}):
        super(MessageLayer, self).__init__(rect, padding)
        self.mes_engine = MessageEngine(filename)

    def draw(self, screen, message):
        super(MessageLayer, self).draw(screen)
        self.mes_engine.draw(screen, message, (self.rect.left + self.padding['left'], self.rect.top + self.padding['top']))
