#! /usr/bin/python
# -*- coding:utf-8 -*-

#import pygame
#from pygame.locals import *

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
        prev = self.get(pos_prev)
        if pos != pos_prev and prev is not None:
            self.add(prev[1], pos)
            self.delete(pos_prev)
            
    def reserve(self, pos, pos_to):
        self.add(self.get(pos)[1], pos_to, mode="reserve")
            
    def normalize(self, x):
        if x == 0: return 0
        elif x > 0: return 1
        else: return -1

class MapInfo(object):
    def __init__(self, filename, directory="map"):
        self._info = {}
#        self.load(filename, directory)

    @property
    def chip_size(self): return self._info["chip_size"]
    @property
    def map_size(self): return self._info["size"]
    @property
    def layer(self): return self._info["layer"]
    
    def chip_image(self, n): return self._info["data"][n]["image"]
    def n_block(self, n): return self._info["data"][n]["block"]
    def n_default(self, n): return self._info["data"][n]["default"]
    def n_data(self, n): return self._info["data"][n]["raw"]
    
    def chip(self, n, (x,y)): return self._info["data"][n]["raw"][y][x]

    def map_header(self, data):
        self._info.update({"size":  (int(data[0]), int(data[1])),
                           "chip_size": Rect(0, 0, int(data[2]), int(data[3])),
                           "layer": int(data[4]),
                           "data": []})
    
    def layer_header(self, data):
        image = self.load_mapchip(data[0])
        size = image.get_size()
        self._info["data"].append({"image": image,
                                   "image_chip_size": tuple(size[i]/self._info["chip_size"][i+2] for i in [0,1]),
                                   "block": data[1],
                                   "default": data[2],
                                   "raw": []})

    def load(self, filename, directory):
        self.load_map(filename, directory)

    def load_map(self, filename, directory):
        with open(get_path(filename, directory=directory), 'r') as f:
            info = [int(x) for x in f.readline().rstrip().split(",")]
            self.map_header(info)

            for n in range(self.layer):
                data = []
                filename = f.readline().strip()
                block = [int(c) for c in f.readline().rstrip().split(u",")]
                default = int(f.readline())
                self.layer_header([filename, block, default])

                for i in range(self._info["size"][1]):
                    data.append([int(x) for x in f.readline().rstrip().split(",")])
                self._info["data"][n]["raw"] = data

    def load_mapchip(self, filename, directory="mapchip"):
        return load_image(filename, directory=directory, colorkey=-1)
    
    def chip_number_pos(self, number, layer):
        chip_size = self._info["data"][layer]["image_chip_size"]
        return number%chip_size[0]*self._info["chip_size"].width, int(number/chip_size[1])*self._info["chip_size"].height
#        return tuple([number%chip_size[0], int(number/chip_size[1])][i]*self._info["chip_size"].bottomright[i] for i in [0,1])
    
class Map(object):
    def __init__(self, filename, directory="map"):
        self.map = MapInfo(filename, directory="map")

    def is_steppable(self,(x,y)):
        if not (0 <= x < self.map.map_size[0] and 0 <= y < self.map.map_size[1]):
            return False
        
        for n in range(self.map.layer):
            if self.map.chip(n, (x,y)) in self.map.n_block(n): return False

        return True

    def draw_tip(self, screen, layer, col, row):
        chip = self.get_chip(layer, col, row)
        if layer == 0 or chip != self.n_default:
            screen.blit(self.map.chip_image(layer), (col*self.map.chip_size.width, row*self.map.chip_size.height), area=self.map.chip_size.move(self.map.chip_number_pos(chip, layer)))

    def get_chip(self, layer, col, row):
        if 0 <= col < self.map.map_size[0] and 0 <= row < self.map.map_size[1]:
            chip = self.map.chip(layer, (col, row))
        else:
            chip = self.map.n_default(layer)
        
        return chip

    def draw(self, screen):
        for layer in range(self.map.layer):
            [self.draw_tip(screen, layer, col-1, row-1)
             for col in xrange(self.map.map_size[0]+2)
             for row in xrange(self.map.map_size[1]+2)]
#            for col in range(self.map.map_size[0]+2):
#                for row in range(self.map.map_size[1]+2):
#                    self.draw_tip(screen, layer, col-1, row-1)
    
    def block_pos(self, (x,y)):
        return x/self.size.width, y/self.size.height
    
    def lookup_safe(self, pos):
        return [(x,y) for x,y in [(1,0),(-1,0),(0,1),(0,-1)] \
                      if self.is_steppable((pos[0]+x, pos[1]+y))]

class ScrollMap(Map):
    def __init__(self, filename, offset=(1,1), directory="map"):
        super(ScrollMap, self).__init__(filename, directory=directory)
        self.create(filename, offset, directory)
        self.scroll = ScrollMarker(self.map.chip_size.width, interval=1, step=4, stop=0)
        self.player = None
        
    def create(self, filename, offset, directory="map"):
        self.map.load(filename, directory)
        self.charas = fc.CharaManager()
        self.event_map = MapEventManager(*self.map.map_size)
        self.offset = tuple(offset[i] - SCREEN.size[i]/UNIT/2 for i in [0,1])

    def add_chara(self, chara, is_player=False):
        self.charas.add(chara, is_player)
        if is_player:
            self.player = chara
        else: self.event_map.add(chara, chara.get_pos())
        
    def draw_tip(self, screen, layer, col, row):
        locate = self.offset[0]+col, self.offset[1]+row
        chip = self.get_chip(layer, *locate)
        if layer != 0 and chip == self.map.n_default(layer): return

        px, py = self.scroll.pos
        screen.blit(self.map.chip_image(layer), (col*self.map.chip_size.width+px, row*self.map.chip_size.height+py), area=self.map.chip_size.move(self.map.chip_number_pos(chip, layer)))

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
        self.event_map.draw(screen, self.player, self.offset, self.scroll.pos)

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

