#! /usr/bin/python
# -*- coding:utf-8 -*-

import pygame
from pygame.locals import *

from utility import *

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

class MessageEngine(object):
    def __init__(self, filename, rect):
        self.size = 18
        self.font = self.load(filename)
        self.pages = []
        self.running = False
        self.rect = rect
        self.line_height = 6
        self.page_index = None

    def load(self, filename):
        filename = os.path.join("../data", filename)
        try:
            font = pygame.font.Font(filename, self.size)
        except pygame.error, message:
            print "Cannot load font:", filename
            raise SystemExit, message
        return font
    
    def max_charactors(self, message):
        for i in range(1, len(message)):
            if self.font.size(message[:i])[0] > self.rect.width: return i-1
        return len(message)
    
    def split_by_width(self, message):
        length = self.max_charactors(message)
        if message[length:] == u'': return [message[:length]]
        return [message[:length]] + self.split_by_width(message[length:])
    
    def format(self, message):
        self.pages = []
        for line in message.rstrip().split("[p]"):
            self.pages.append(line.split("[l]"))
        self.pages = [[self.split_by_width(line) for line in page] for page in self.pages]
        self.pages = [flatten(page) for page in self.pages]
        self.page_index = IndexMarker(len(self.pages))
    
    def draw(self, screen, message, pos):
        if self.running == False:
            self.format(message)
            self.running = True
        for i in range(len(self.pages[self.page_index()])):
            screen.blit(self.font.render(self.pages[self.page_index()][i], True, (255, 255, 255)), (pos[0], pos[1]+(self.font.get_height()+self.line_height)*i))

    def next(self):
        self.page_index.next()
        if self.page_index() == 0:
            self.running = False
            return True
        return False

class MessageLayer(Layer):
    def __init__(self, filename, rect, padding={'top':15, 'left':20, 'bottom':15, 'right':20}):
        super(MessageLayer, self).__init__(rect, padding)
        self.mes_engine = MessageEngine(filename, Rect(0, 0, rect.width - padding['left'] - padding['right'], rect.height - padding['bottom'] - padding['top']))

    def draw(self, screen, message):
        super(MessageLayer, self).draw(screen)
        self.mes_engine.draw(screen, message, (self.rect.left + self.padding['left'], self.rect.top + self.padding['top']))

    def next(self): return self.mes_engine.next()
