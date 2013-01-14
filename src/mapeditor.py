#! /usr/bin/python
# -*- coding:utf-8 -*-

import pygame
from pygame.locals import *

from utility import *
import layer
import field
import field_chara as fc
import main

GAME_TITLE = u"GIAPRO"
DIRECTORY = "mapeditor"

class MapEditor(field.ScrollMap):
    def __init__(self, filename, offset=(-9,-6), size=(15,20), default=0, map_to_map=[(0,(0,0)), (1,(0,0))], map_files=["none.png", "mapchip.png"]):
        self.size = Rect(0,0,32,32)
        self.map_to_map = map_to_map
        self.image = [load_image(map_file, directory="mapchip") for map_file in map_files]
        self.block = []
        self.data_size, self.default, self.data = size, default, [[1]*size[1] for i in range(size[0])]
        self.name = filename

        self.offset = offset
        self.scroll = ScrollMarker(self.size.width, interval=1, step=4, stop=0)
        self.charas = field.CharaManager()
        self.event_map = field.MapEventManager(self.data_size[0], self.data_size[1])
        
        self.init()

    def init(self):
        self.layer = layer.SimpleMessageEngine("ipag.ttf", rect=Rect(0,0,200,100))
        self.pointing = load_image("pointing.png", alpha=True, directory=DIRECTORY)
        
    def draw(self, screen):
        screen.blit(self.pointing, (SCREEN.width/2, SCREEN.height/2-UNIT/2))
        self.layer.draw(screen, u"{0} {1}".format(*self.player.pos_adjust(self.offset)), (0,0))
        
class System(main.GameFrame):
    def __init__(self):
        super(System, self).__init__(title=GAME_TITLE, size=SCREEN.size)

        self.map = MapEditor("field.map")
        self.map.add_chara(fc.Player("pointing.png", name="player", directory=DIRECTORY), is_player=True)
        
    def key_step(self):
        step = (0, 0)
        if self.key[K_UP]: step = (0, -1)
        elif self.key[K_DOWN]: step = (0, 1)
        elif self.key[K_RIGHT]: step = (1, 0)
        elif self.key[K_LEFT]: step = (-1, 0)
        return step
    
    def mainloop(self):
        while self._step() != -1:
            super(field.ScrollMap, self.map).draw(self.screen)
            self.map.draw(self.screen)
            self.map.move(self.key_step())
        self._quit()

if __name__ == "__main__":
    game = System()
    game.mainloop()
