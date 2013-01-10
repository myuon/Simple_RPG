#! /usr/bin/python
# -*- coding:utf-8 -*-

import pygame
from pygame.locals import *

from functools import wraps

from utility import *
import field_chara

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
        if 0 <= x < self.data_size[1] and 0 <= y < self.data_size[0]:
            tip = self.data[y][x]
        else:
            tip = self.default

        if tip == self.default: return False
        else: return tip not in self.block
    
    def draw_tip(self, screen, col, row):
        f,(x,y) = self.map_to_map[self.data[col][row]]
        screen.blit(self.image[f], (row*self.size.width, col*self.size.height), area=self.size.move(x,y))

    def draw(self, screen):
        for col in range(self.data_size[0]+2):
            for row in range(self.data_size[1]+2):
                self.draw_tip(screen, col-1, row-1)
                
    def block_pos(self,(x,y)):
        return x/self.size.width, y/self.size.height
    
    def lookup_safe(self, pos):
        return [(x,y) for x,y in [(1,0),(-1,0),(0,1),(0,-1)] \
                      if self.is_steppable((pos[0]+x, pos[1]+y))]

class CharaManager(Manager):
    def __init__(self):
        self.objects = []
        self.player = None
        
    def add(self, chara, is_player):
        if is_player: self.player = chara
        else: self.objects.append(chara)

    def move(self, step, lookup, event_map):
        self.player.move_dir(step)
        for i in self.objects:
            if i.movable:
                @event_map.update(i, "get_pos", i.scroll)
                def _move():
                    i.move(lookup(i.pos))

class MapEventManager(Manager):
    def __init__(self, col, row):
        self.data = self.make_2D_array(col, row)
        self.data_size = col, row
        
    def add(self, info, pos): self.data[pos[1]][pos[0]] = info
    def delete(self, pos): self.data[pos[1]][pos[0]] = None
        
    def get(self, pos): return self.data[pos[1]][pos[0]]
    
    def make_2D_array(self, col, row):
        array = []
        for i in range(col):
            array.append([None]*row)
        return array

    def is_steppable(self,(x,y)):
        tip = None
        if 0 <= x < self.data_size[1] and 0 <= y < self.data_size[0]:
            tip = self.data[y][x]

        return tip == None

    def draw(self, screen, offset, scroll):
        for i in range(self.data_size[1]):
            for j in range(self.data_size[0]):
                data = self.data[j][i]
                if data is None: continue
                
                if isinstance(data,field_chara.NPC): data.draw(screen, offset, scroll)
                elif isinstance(data,field_chara.Player): data.draw(screen)

    def update(self, instance, get_pos, scroll, *arg):
        def _update(function):
            pos_old = getattr(instance, get_pos)(*arg)
            function()
            scroll_norm = tuple([self.normalize(-scroll[i]) for i in [0,1]])
            pos_adjust = tuple([pos_old[i] + scroll_norm[i] for i in [0,1]])
            # pos_new = getattr(instance, get_pos)(*arg)

            if UNIT/2 <= abs(scroll[0])+abs(scroll[1]) <= UNIT*3/4 and self.get(pos_old) is instance:
                self.add(self.get(pos_old), pos_adjust)
                self.delete(pos_old)
            
        return _update
    
    def normalize(self, x):
        if x == 0: return 0
        elif x > 0: return 1
        else: return -1

    def reserve(self, pos):
        self.data[pos[1]][pos[0]] = 1
        
class ScrollMap(Map):
    def __init__(self, filename, offset=(-9,-6)):
        super(ScrollMap, self).__init__(filename)
        self.offset = offset
        self.scroll = ScrollMarker(self.size.width, interval=1, step=4, stop=0)
        self.charas = CharaManager()
        self.event_map = MapEventManager(self.data_size[0], self.data_size[1])

    def add_chara(self, chara, is_player=False):
        self.charas.add(chara, is_player)
        if is_player: self.event_map.add(chara, chara.pos_adjust(self.offset))
        else: self.event_map.add(chara, chara.get_pos())

    def draw_tip(self, screen, col, row):
        locate = self.offset[1]+col, self.offset[0]+row
        if 0 <= locate[0] < self.data_size[0] and 0 <= locate[1] < self.data_size[1]:
            tip = self.data[locate[0]][locate[1]]
        else:
            tip = self.default
        f,(x,y) = self.map_to_map[tip]
        px, py = self.scroll()
        screen.blit(self.image[f], (row*self.size.width+px, col*self.size.height+py), area=self.size.move(x,y))

    def is_steppable(self,(x,y)):
        return super(ScrollMap, self).is_steppable((x,y)) and self.event_map.is_steppable((x, y))

    def map_move(self, step):
        if self.scroll.enable:
            if self.scroll.next() == False:
                step_ = dir_step(self.scroll.direction)
                self.offset = self.offset[0]+step_[0], self.offset[1]+step_[1]
        else:
            pos = tuple([self.offset[i] + step[i] + self.charas.player.pos[i] for i in [0,1]])
            if step != (0,0) and self.is_steppable(pos):
                self.scroll.active()
                self.scroll.direction = step_dir(step)

    def draw(self, screen):
        super(ScrollMap, self).draw(screen)
        self.event_map.draw(screen, self.offset, self.scroll())

    def move(self, step):
        @self.event_map.update(self.charas.player, "pos_adjust", self.scroll(), self.offset)
        def _move():
            self.map_move(step)
        self.charas.move(step, self.lookup_safe, self.event_map)
