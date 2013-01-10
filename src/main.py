#! /usr/bin/python
# -*- coding:utf-8 -*-

import pygame
from pygame.locals import *

from utility import *

import field_chara as fc
import field
import layer

GAME_TITLE = u"GIAPRO"

class Scene(object):
    def __init__(self):
        self.scene = [
                      "None",
                      "Load",
                      "Field",
                      "Layer",
                      "Battle"
                      ]
        self.current = "None"
        
    def transition(self, dest):
        if dest not in self.scene:
            print "Undefined scene name:", dest
            raise SystemExit, "Illegal Transition Error"

        self.current = dest

    @property    
    def name(self): return self.current

class GameFrame(object):
    def __init__(self, GAME_TITLE, SCREEN):
        pygame.init()
        pygame.display.set_caption(GAME_TITLE)

        self.screen = pygame.display.set_mode(SCREEN.size)
        self.key = []
        self.clock=pygame.time.Clock()
        self.scene = Scene()
    
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
        self.loaded_events = []
        self.load(filename)
        self.events = {}
        self.index = 0
        
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
                'type' : data_[0],
                'name' : data_[1],
                'position' : (int(data_[2]), int(data_[3])),
                'direction' : int(data_[4]),
                'movable' : bool(data_[5]),
                'message' : data_[6]
                }
        
    def load(self, filename):
        with open(os.path.join("../data", filename), 'r') as f:
            for line in f:
                if line.startswith("#"): continue
                self.loaded_events.append(self.make_data(line.decode('utf-8')))
    
    def run(self, chara_run):
        for event in self.loaded_events:
            if event['type'] == "CHARA":
                chara_run("vx_chara01_a.png", name=event['name'], pos=event['position'], chara=(2,0), movable=event['movable'])
                self.events[event['name']] = {'type':"TALK", 'content':event["message"]}
                
    def check(self, name):
        if self.events.has_key(name):
            return self.events[name]
        else: None

class System(GameFrame):
    def __init__(self):
        super(System, self).__init__(GAME_TITLE, SCREEN)

        self.map = field.ScrollMap("map.txt")
        self.event = EventManager("event.txt")
        
        self.map.add_chara(fc.Player("vx_chara01_a.png", name="player"), is_player=True)
        self.event.run(lambda *args, **kwargs:self.map.add_chara(fc.NPC(*args, **kwargs)))

        self.mes_layer = layer.MessageLayer("ipag.ttf", Rect(140,334,360,140))

        self.scene.transition("Field")

    def key_step(self):
        step = (0, 0)
        if self.key[K_UP]: step = (0, -1)
        elif self.key[K_DOWN]: step = (0, 1)
        elif self.key[K_RIGHT]: step = (1, 0)
        elif self.key[K_LEFT]: step = (-1, 0)
        return step
    
    def key_z(self):
        if self.key[K_z]:
            info = self.map.check()
            if info is None: return None
        
            ev = self.event.check(info.name)
            if ev is None: return None
            
            if ev['type'] == "TALK":
                return ev['content']
                
        return None

    def mainloop(self):
        while self._step() != -1:
            ev = self.key_z()
            if ev is not None:
                self.scene.transition("Layer")

            if self.scene.name == "Field":
                self.map.draw(self.screen)
                self.map.move(self.key_step())
            elif self.scene.name == "Layer":
                self.map.draw(self.screen)
                self.mes_layer.draw(self.screen, ev)
                self.scene.transition("Field")
                
        self._quit()

if __name__ == "__main__":
    game = System()
    game.mainloop()
