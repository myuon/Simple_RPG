#! /usr/bin/python
# -*- coding:utf-8 -*-

import pygame
from pygame.locals import *

from functools import wraps
import struct
import os

from utility import *
import field_chara as fc

class MapEventManager(Manager):
    def __init__(self, col, row):
        # data :: {(Int, Int):(String, <Charactor object>)}
        self.data = {}
        self.data_size = col, row
        
    def add(self, info, pos, mode="here"): self.data[pos] = (mode, info)
    def change(self, pos, mode): self.data[pos] = (mode, self.data[pos])

    def delete(self, pos): del self.data[pos]        
    def get(self, pos):
        if self.data.has_key(pos): return self.data[pos]
        else: return None
    
    def is_steppable(self, pos):
        info = None
        if 0 <= pos[0] < self.data_size[1] and 0 <= pos[1] < self.data_size[0]:
            if self.data.has_key(pos):
                info = self.data[pos][1]

        return info is None or isinstance(info, fc.SimpleEvent)

    def draw(self, screen, player, offset, scroll):
        for pos, (mode, chara) in sorted(self.data.items()+[(player.pos_adjust(offset), ("here", player))]):
            if mode != "here": continue
            
            if isinstance(chara, fc.NPC): chara.draw(screen, offset, scroll)
            elif isinstance(chara, fc.Player): chara.draw(screen)

    def update(self, pos, pos_prev):
        if pos != pos_prev:
            self.add(self.get(pos_prev)[1], pos)
            self.delete(pos_prev)
            
    def reserve(self, pos, pos_to):
        self.add(self.get(pos)[1], pos_to, mode="reserve")
            
    def normalize(self, x):
        if x == 0: return 0
        elif x > 0: return 1
        else: return -1


class Map(object):
    def __init__(self, filename, directory="map"):
        self.size = Rect(0,0,32,32)
        self.map_to_map = []
        self.image = []
        self.block = []
        self.name = filename

        self.data_size, self.default, self.data = None, None, None
        self.load(filename, directory)

    def load(self, filename, directory):
        self.data_size, self.default, self.data = self.load_map(filename, directory)
        chip_files, block = self.load_setting(filename, directory)
        self.image, self.map_to_map = self.make_number_mapping(chip_files, directory)
        self.block += block

    def load_map(self, filename, directory):
        data = []
        with open(get_path(filename, directory=directory), 'r') as f:
            info = [int(x) for x in f.readline().rstrip().split(",")]
            size = info[1], info[0]
            default = int(f.readline())
            for line in f:
                data.append([int(x) for x in line.rstrip().split(",")])
        return size, default, data
    
    def load_setting(self, filename, directory):
        data = []
        block = []
        with open(get_path(insert_path(filename, "setting"), directory=directory), 'r') as f:
            line = f.readline()
            for line in f:
                if line.startswith(u"#"): continue
                if line.startswith(u":"):
                    block.append([int(c) for c in line[1:].rstrip().split(u",")])
                else: data.append(line.rstrip())
        return data, flatten(block)
    
    def make_number_mapping(self, fs, directory):
        data = []
        mapping = []
        for f in range(len(fs)):
            image = load_image(fs[f], directory="mapchip")
            size = image.get_size()
            mapping.append([(f, (x*UNIT, y*UNIT)) for y in range(size[1]/UNIT) for x in range(size[0]/UNIT)])
            data.append(image)

        return data, flatten(mapping)

    def is_steppable(self,(x,y)):
        if not (0 <= x < self.data_size[1] and 0 <= y < self.data_size[0]):
            return False

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
    
    def lookup_safe(self, pos):
        return [(x,y) for x,y in [(1,0),(-1,0),(0,1),(0,-1)] \
                      if self.is_steppable((pos[0]+x, pos[1]+y))]

class ScrollMap(Map):
    def __init__(self, filename, offset=(-9,-6), directory="map"):
        super(ScrollMap, self).__init__(filename, directory=directory)
        self.scroll = ScrollMarker(self.size.width, interval=1, step=4, stop=0)
        self.player = None

        self.charas = fc.CharaManager()
        self.event_map = MapEventManager(self.data_size[0], self.data_size[1])
        self.offset = offset
        
    def create(self, filename, offset, directory="map"):
        self.data_size, self.default, self.data = None, None, None
        self.load(filename, directory)

        self.charas = fc.CharaManager()
        self.event_map = MapEventManager(self.data_size[0], self.data_size[1])
        self.offset = tuple(offset[i] - SCREEN.size[i]/UNIT/2 for i in [0,1])

    def add_chara(self, chara, is_player=False):
        self.charas.add(chara, is_player)
        if is_player:
            self.player = chara
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
            pos = tuple([self.offset[i] + step[i] + self.player.pos[i] for i in [0,1]])
            if step != (0,0) and self.is_steppable(pos):
                self.scroll.active()
                self.scroll.direction = step_dir(step)

    def draw(self, screen):
        super(ScrollMap, self).draw(screen)
        self.event_map.draw(screen, self.player, self.offset, self.scroll())

    def move(self, step):
        self.map_move(step)
        self.charas.move(step, self.player, self.offset, self.lookup_safe, self.event_map)
        
    def pos_gazing(self):
        return tuple([self.offset[i] + dir_step(self.player.direction)[i] + self.player.pos[i] for i in [0,1]])

    def check_gazing(self):
        return self.get_event(self.pos_gazing())[1] if self.get_event(self.pos_gazing()) is not None else None
    
    def check_pos(self):
        return self.get_event(self.player.pos_adjust(self.offset))[1] if self.get_event(self.player.pos_adjust(self.offset)) is not None else None

    def get_event(self, pos):
        return self.event_map.get(pos)

