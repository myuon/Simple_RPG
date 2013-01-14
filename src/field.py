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
        self.data = self.make_2D_array(col, row)
        self.data_size = col, row
        
    def add(self, info, pos, mode="here"): self.data[pos[1]][pos[0]] = (mode, info)
    def change(self, pos, mode): self.add(self.get(pos)[1], pos, mode=mode)
        
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

        return tip is None
    def draw(self, screen, offset, scroll):
        for i in range(self.data_size[1]):
            for j in range(self.data_size[0]):
                data = self.data[j][i]
                if data is None: continue
                if data[0] != "here": continue
                
                if isinstance(data[1], fc.NPC): data[1].draw(screen, offset, scroll)
                elif isinstance(data[1], fc.Player): data[1].draw(screen)

    def update(self, pos, pos_prev):
#        step = dir_step(self.get(pos)[1].direction)
#        if isinstance(self.get(pos)[1], field_chara.NPC) and self.get(pos)[1].move_step.stop.enable:
#            step = (0,0)

        if pos != pos_prev:
            print pos, pos_prev
            self.add(self.get(pos_prev)[1], pos)
            self.delete(pos_prev)

#        pos_adjust = tuple([pos[i] + step[i] for i in [0,1]])
#        if self.get(pos_adjust) is None or self.get(pos_adjust)[0] == "reserve":
#            self.reserve(pos, pos_adjust)
        
#        if self.get(pos)[0] == "reverse":
#            if self.get(pos_prev)[1] is not self.get(pos)[1]:
#                print self.data
#                print pos, pos_prev
#                raise Exception
#            self.change(pos, "here")
#            self.delete(pos_prev)
            
    def reserve(self, pos, pos_to):
        self.add(self.get(pos)[1], pos_to, mode="reserve")
            
    def normalize(self, x):
        if x == 0: return 0
        elif x > 0: return 1
        else: return -1


class Map(object):
    def __init__(self, filename, map_to_map=[(1,(0,0)), (0,(0,0)), (0, (0,192)), (0, (0,288)), (0, (32,0)), (1,(0,0)), (0,(0,0)), (0, (0,192)), (0, (0,288)), (0, (32,0))], map_files=["TileA1.png", "TileA2.png"], directory="map"):
        self.size = Rect(0,0,32,32)
        self.map_to_map = map_to_map
        self.image = [load_image(map_file, directory="mapchip") for map_file in map_files]
        self.block = []
        self.name = filename

        self.data_size, self.default, self.data = None, None, None
        self.load(filename, directory)

    def insert_path(self, p, string):
        p_ = os.path.splitext(p)
        return "{0}_{1}{2}".format(p_[0], string, p_[1])

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
        with open(get_path(self.insert_path(filename, "setting"), directory=directory), 'r') as f:
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
 
#    def load(self, filename, directory):
#        with open(get_path(filename, directory), 'rb') as f:
#            row = struct.unpack("i", f.read(struct.calcsize("i")))[0]
#            col = struct.unpack("i", f.read(struct.calcsize("i")))[0]
#            default = struct.unpack("B", f.read(struct.calcsize("B")))[0]
#            data = [[default for c in range(col)] for r in range(row)]
#                
#            for r in range(row):
#                for c in range(col):
#                    data[r][c] = struct.unpack("B", f.read(struct.calcsize("B")))[0]
#                    
#        return (row, col), default, data

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

class ScrollMap(Map):
    def __init__(self, filename, offset=(-9,-6), directory="map"):
        super(ScrollMap, self).__init__(filename, directory=directory)
        self.offset = offset
        self.scroll = ScrollMarker(self.size.width, interval=1, step=4, stop=0)
        self.charas = fc.CharaManager()
        self.event_map = MapEventManager(self.data_size[0], self.data_size[1])
        self.player = None

    def add_chara(self, chara, is_player=False):
        self.charas.add(chara, is_player)
        if is_player:
            self.event_map.add(chara, chara.pos_adjust(self.offset))
            self.player = self.charas.player
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
        self.event_map.draw(screen, self.offset, self.scroll())

    def move(self, step):
        self.map_move(step)
        self.charas.move(step, self.offset, self.lookup_safe, self.event_map, self.scroll())
        
    def pos_gazing(self):
        return tuple([self.offset[i] + dir_step(self.player.direction)[i] + self.player.pos[i] for i in [0,1]])

    def check(self):
        return self.event_map.get(self.pos_gazing())[1]

