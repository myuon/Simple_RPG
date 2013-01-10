#! /usr/bin/python
# -*- coding:utf-8 -*-

import pygame
from pygame.locals import *

from utility import *

import field_chara as fc
import field

GAME_TITLE = u"GIAPRO"

class GameFrame(object):
    def __init__(self, GAME_TITLE, SCREEN):
        pygame.init()
        pygame.display.set_caption(GAME_TITLE)

        self.screen = pygame.display.set_mode(SCREEN.size)
        self.key = []
        self.clock=pygame.time.Clock()
    
    def _event(self):
        for event in pygame.event.get():
            if event.type==QUIT: return -1
        if self.key[K_ESCAPE]: return -1
        
    def _step(self):
        pygame.display.update()

        self.key = pygame.key.get_pressed()
        self.clock.tick(60)
        
        if self._event() == -1: return -1

        self.screen.fill((0,0,60))
        return 0
        
    def mainloop(self):
        while self._step() != -1:
            pass
        self._quit()

    def _quit(self):
        pygame.display.quit()
        pygame.quit()

class EventManager(Manager):
    def __init__(self, filename):
        self.events = []
        self.load(filename)
        
    def make_data(self, data):
        data_ = data.split(",", 7)
        
        if data_[0] not in ["CHARA"]:
            print "received undefined type:{0}".format(data_[0])
            raise SystemExit, "Undefined Type Error"
        if data_[2].isdigit() != True or \
           data_[3].isdigit() != True:
            print "position x(or y) must be an integer, not:{0}({1})".format(data_[2], data_[3])
            raise SystemExit, "Type Check Error"
        if data_[4].isdigit() != True or \
           int(data_[4]) not in [0, 1, 2, 3]:
            print "direction must be an integer ranged 0-3, not:{0}".format(data_[4])
            raise SystemExit, "Type/Range Check Error"
        if data_[5].isdigit() != True or \
           int(data_[5]) not in [0, 1]:
            print "direction must be an integer ranged 0-1, not:{0}".format(data_[5])
            raise SystemExit, "Type/Range Check Error"
        
        return {
                "type" : data_[0],
                "name" : data_[1],
                "position" : (int(data_[2]), int(data_[3])),
                "direction" : int(data_[4]),
                "movable" : bool(data_[5]),
                "message" : data_[6]
                }
        
    def load(self, filename):
        with open(os.path.join("../data", filename), 'r') as f:
            for line in f:
                if line.startswith("#"): continue
                self.events.append(self.make_data(line))
    
    def run(self, chara_run):
        for event in self.events:
            if event["type"] == "CHARA":
                chara_run("vx_chara01_a.png", pos=event["position"], chara=(2,0), movable=event["movable"])

class System(GameFrame):
    def __init__(self):
        super(System, self).__init__(GAME_TITLE, SCREEN)
        self.map = field.ScrollMap("map.txt")
        self.event = EventManager("event.txt")
        
        self.map.add_chara(fc.Player("vx_chara01_a.png"), is_player=True)
        self.event.run(lambda *args, **kwargs:self.map.add_chara(fc.NPC(*args, **kwargs)))
#        self.map.add_chara(fc.NPC("vx_chara01_a.png", pos=(4,3), chara=(2,0), movable=True))
#        self.map.add_chara(fc.NPC("vx_chara01_a.png", pos=(2,1), chara=(1,1), movable=True))
#        self.map.add_chara(fc.NPC("vx_chara01_a.png", pos=(6,3), chara=(3,1)))

    def key_step(self):
        step = (0, 0)
        if self.key[K_UP]: step = (0, -1)
        elif self.key[K_DOWN]: step = (0, 1)
        elif self.key[K_RIGHT]: step = (1, 0)
        elif self.key[K_LEFT]: step = (-1, 0)
        return step

    def mainloop(self):
        while self._step() != -1:
            self.map.draw(self.screen)
            self.map.move(self.key_step())
        self._quit()

if __name__ == "__main__":
    game = System()
    game.mainloop()
