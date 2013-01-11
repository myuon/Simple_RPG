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
    FONT_SIZE = 18
    LINE_HEIGHT = 6

    def __init__(self, filename, rect):
        self.size = self.FONT_SIZE
        self.font = self.load(filename)
        self.messages = []
        self.rect = rect
        self.line_height = self.LINE_HEIGHT
        self.index = { 'page': None, 'line': None, 'letter': None }
        self.waiting = False
        self.running = False
        
    def new_index(self, keys):
        for key in keys:
            if self.index.has_key(key) == False:
                print "Illegal key:", key
                raise SystemExit, "Key Error"
    
            if key == 'page': self.index['page'] = IndexMarker(len(self.messages)+1)
            if key == 'line': self.index['line'] = IndexMarker(len(self.messages[self.index['page']()])+1)
            if key == 'letter': self.index['letter'] = IndexMarker(len(self.messages[self.index['page']()][self.index['line']()])+1, interval=3)

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
        self.messages = []
        for line in message.rstrip().split("[p]"):
            self.messages.append(line.split("[l]"))
        self.messages = [[self.split_by_width(line) for line in page] for page in self.messages]
        self.messages = [flatten(page) for page in self.messages]

    def indexes_areas(self):
        areas = []
        for i in range(len(self.messages[self.index['page']()])):
            if i < self.index['line']():
                areas.append(Rect(0, 0, self.rect.width, self.font.get_height()))
            elif i == self.index['line']():
                areas.append(Rect((0, 0), self.font.size(self.messages[self.index['page']()][i][:self.index['letter']()])))
            else:
                areas.append(Rect(0, 0, 0, 0))
        return areas
    
    def init(self, message):
        self.format(message)
        self.running = True
        self.new_index(['page', 'line', 'letter'])
    
    def draw(self, screen, message, pos):
        if self.running == False: self.init(message)
        areas = self.indexes_areas()
        for i in range(len(self.messages[self.index['page']()])):
            screen.blit(self.font.render(self.messages[self.index['page']()][i], True, (255, 255, 255)), (pos[0], pos[1]+(self.font.get_height()+self.line_height)*i), area=areas[i])

        if self.waiting:
            screen.blit(self.font.render(u"▽", True, (255, 255, 255)), (pos[0]+self.rect.width/2-self.font.size("▽")[0]/2, pos[1]+self.rect.height-self.font.get_height()))
        else:
            self.count()

    def count(self):
        self.index['letter'].next()
        if self.index['letter'].is_next_end():
            self.index['line'].next()
            if self.index['line'].is_next_end():
                self.waiting = True
            else:
                self.new_index(['letter'])

    def next(self):
        self.waiting = False
        self.index['page'].next()
        if self.index['page'].is_next_end():
            self.running = False
            return True
        self.new_index(['line', 'letter'])
        return False

class MessageLayer(Layer):
    def __init__(self, filename, rect, padding={'top':15, 'left':20, 'bottom':15, 'right':20}):
        super(MessageLayer, self).__init__(rect, padding)
        self.mes_engine = MessageEngine(filename, Rect(0, 0, rect.width - padding['left'] - padding['right'], rect.height - padding['bottom'] - padding['top']))

    def draw(self, screen, message):
        super(MessageLayer, self).draw(screen)
        self.mes_engine.draw(screen, message, (self.rect.left + self.padding['left'], self.rect.top + self.padding['top']))

    def next(self): return self.mes_engine.next()
