#! /usr/bin/python
# -*- coding:utf-8 -*-

import pygame
from pygame.locals import *

from utility import *

import random

class CharaManager(Manager):
    def __init__(self):
        self.objects = []
        
    def add(self, chara, is_player):
        if is_player: self.player = chara
        else: self.objects.append(chara)

    def move(self, step, player, offset, lookup, event_map):
        player.move(offset)

        player.move_dir(step)
        for i in self.objects:
            if i.movable:
                i.move(lookup(i.pos))
                event_map.update(i.pos, i.pos_prev)

class SimpleEvent(object):
    def __init__(self, event_id=None):
        self.event_id = event_id
        
class Chara(object):
    def __init__(self, path, event_id, pos, size, offset, directory="chara"):
        self.pos = pos
        self.event_id = event_id
        self.size = Rect(0,0,size[0],size[1])
        self.direction = DOWN
        self.split_load(path, offset, directory)
        
    def load(self, path, directory):
        self.image = load_image(path, -1, directory=directory)
        
    def split_load(self, path, offset, directory):
        self.image = []
        images = split_image(load_image(path, -1, directory=directory), self.size.size, (3,4), offset)
        for seq in images:
            self.image.append((seq[1], seq[0], seq[1], seq[2]))
        
    def move(self, step):
        self.pos += (step[0]*self.size.width, step[1]*self.size.height/2)

    def move_dir(self, step):
        direction = step_dir(step)
        if direction is not None: self.direction = direction
    
        return (self.pos[0]+step[0]*self.size.width, self.pos[1]+step[1]*self.size.height/2)
    
    def draw(self, screen):
        screen.blit(self.image[self.direction][0], self.pos, area=self.size)

class Player(Chara):
    def __init__(self, path, name, pos=(SCREEN.width/2/UNIT, SCREEN.height/2/UNIT), size=(32, 48), chara=(0,0), directory="chara"):
        super(Player, self).__init__(path, name, pos, size, chara, directory=directory)
        self.index = IndexMarker(4, interval=15)
        self.index.active()
        self.pos_prev = (1, 1)
        
    def pixel_pos(self): return self.pos[0]*UNIT, self.pos[1]*UNIT
    def locate(self): return self.pixel_pos()[0], self.pixel_pos()[1]-UNIT/2

    def draw(self, screen):
        screen.blit(self.image[self.direction][self.index()], self.locate(), area=self.size)
        self.index.next()
        
    def move(self, offset):
        if self.pos_adjust(offset) != self.pos_prev: self.pos_prev = self.pos_adjust(offset)
    
    def pos_adjust(self, offset): return offset[0]+self.pos[0], offset[1]+self.pos[1]
    
class NPC(Player):
    def __init__(self, path, event_id, pos=(1,1), size=(32, 48), chara=(0,0), movable=False, directory="chara"):
        super(NPC, self).__init__(path, event_id, pos, size, chara, directory=directory)
        self.movable = movable
        self.scroll = (0, 0)
        if self.movable:
            self.neighbors = []
            self.move_step = ScrollMarker(self.size.width, interval=1, step=2, stop=400)
            self.move_step.stop.index = random.randint(0,400)
            self.move_step.active()

    def draw(self, screen, offset, scroll):
        direction = self.direction if self.direction is not None else DOWN
        screen.blit(self.image[direction][self.index()], tuple([self.locate(offset)[i]+scroll[i] for i in [0,1]]), area=self.size)
        self.index.next()

    def pixel_pos(self, offset): return (self.pos[0]-offset[0])*UNIT, (self.pos[1]-offset[1])*UNIT
    def locate(self, offset):
        pos = self.pixel_pos(offset)
        return pos[0]-self.scroll[0], pos[1]-UNIT/2-self.scroll[1]
    
    def move(self, neighbors):
        if self.pos_prev != self.pos: self.pos_prev = self.pos
        if neighbors == []: return None

        if self.move_step.enable:
            if isinstance(self.move_step.direction, list) and self.move_step.is_stack() == False:
                self.direction = step_dir(random.choice(self.move_step.direction))
                self.move_step.direction = self.direction
            if self.move_step.next() == False:
                sx, sy = dir_step(self.direction)
                self.pos = self.pos[0]+sx, self.pos[1]+sy
            self.scroll = self.move_step()
        else:
            self.move_step.active()
            self.move_step.direction = neighbors
            
    def get_pos(self): return self.pos

    def change_dir(self, dir):
        self.direction = dir

