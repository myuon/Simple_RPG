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
    def __init__(self, title=GAME_TITLE, size=SCREEN.size):
        pygame.init()
        pygame.display.set_caption(title)

        self.screen = pygame.display.set_mode(size)
        self.key = [0]*323
        self.clock=pygame.time.Clock()
        self.scene = Scene()
    
    def _event(self):
        for event in pygame.event.get():
            if event.type==QUIT: return -1
        if self.key[K_ESCAPE]: return -1
        
    def _key(self):
        key = pygame.key.get_pressed()
        for i in range(len(key)):
            if key[i]: self.key[i] += key[i]
            else: self.key[i] = 0
        
    def _step(self):
        pygame.display.update()
        self._key()
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
    def __init__(self, filename, directory="map"):
        self.loaded_events = []
        self.load(filename, directory)
        self.a_events = {}
        self.p_events = {}
        self.index = 0
        self.message = u""
        
    def make_data(self, data):
        data_ = data.split(",", 7)
        
        if data_[0] not in ["CHARA", "MOVE"]:
            print "received undefined type:{0}".format(data_[0])
            raise SystemExit, "Undefined Type Error"

        if data_[0] == "CHARA":
            return {
                    'type' : data_[0],
                    'chara' : (int(data_[1]), int(data_[2])),
                    'position' : (int(data_[3]), int(data_[4])),
                    'direction' : int(data_[5]),
                    'movable' : bool(data_[6]),
                    'message' : data_[7]
                    }
        elif data_[0] == "MOVE":
            return {
                    'type' : data_[0],
                    'position' : (int(data_[1]), int(data_[2])),
                    'map' : data_[3],
                    'to_position' : (int(data_[4]), int(data_[5]))
                    }
        
    def load(self, filename, directory):
        with open(get_path(insert_path(filename, "event"), directory=directory), 'r') as f:
            for line in f:
                if line.startswith("#"): continue
                self.loaded_events.append(self.make_data(line.decode('utf-8')))
    
    def register(self, chara_register, move_register):
        for event in self.loaded_events:
            if event['type'] == "CHARA":
                event_id = "{0}_{1}".format(*event['position'])
                chara_register("vx_chara01_a.png", event_id=event_id, pos=event['position'], chara=event['chara'], movable=event['movable'])
                self.a_events[event_id] = {'type':"TALK", 'content':event["message"]}
            elif event['type'] == "MOVE":
                event_id = "{0}_{1}".format(*event['position'])
                move_register(event['position'], event_id=event_id)
                self.p_events[event_id] = {'type':"MOVE", 'map':event['map'], 'to_position':event['to_position']}

    def a_check(self, event_id, key):
        if key[K_z] == 1:
            if self.a_events.has_key(event_id):
                return self.a_events[event_id]
        
    def p_check(self, event_id, key):
        if self.p_events.has_key(event_id):
            return self.p_events[event_id]
            
    def pull_event(self, map_check, event_check, key):
        info = map_check()
        if info is None: return None, None
        
        event = event_check(info.event_id, key)
        if event is None: return None, None
        
        return info, event
            
    def run(self, scene, scmap, key):
        info, event = self.pull_event(scmap.check_gazing, self.a_check, key)
        if (info, event) != (None, None):
            if event['type'] == "TALK":
                info.change_dir(step_dir(tuple([scmap.player.pos_adjust(scmap.offset)[i] - info.pos[i] for i in [0,1]])))
                self.message = event['content']
                scene.transition("Layer")
            
        info, event = self.pull_event(scmap.check_pos, self.p_check, key)
        if (info, event) != (None, None):
            if event['type'] == "MOVE":
                scmap.create(event['map'], event['to_position'])
                return event['map']

class System(GameFrame):
    def __init__(self):
        super(System, self).__init__(title=GAME_TITLE, size=SCREEN.size)

        self.map = field.ScrollMap("field1.txt")
        self.map.add_chara(fc.Player("vx_chara01_a.png", name="player"), is_player=True)
        self.event = EventManager("field1.txt")
        
        self.create()
        
        self.mes_layer = layer.MessageLayer("ipag.ttf", Rect(140,334,360,140))
        self.scene.transition("Field")
    
    def create(self):
        self.event.register(lambda *args, **kwargs:self.map.add_chara(fc.NPC(*args, **kwargs)),
                            lambda pos, *args, **kwargs:self.map.event_map.add(fc.SimpleEvent(*args, **kwargs), pos))


    def key_step(self):
        step = (0, 0)
        if self.key[K_UP]: step = (0, -1)
        elif self.key[K_DOWN]: step = (0, 1)
        elif self.key[K_RIGHT]: step = (1, 0)
        elif self.key[K_LEFT]: step = (-1, 0)
        return step
    
    def mainloop(self):
        while self._step() != -1:
            if self.scene.name == "Field":
                self.map.draw(self.screen)
                self.map.move(self.key_step())
                if self.map.scroll.enable == False:
                    info = self.event.run(self.scene, self.map, self.key)
                    if info is not None:
                        self.event.__init__(info)
                        self.create()

            elif self.scene.name == "Layer":
                self.map.draw(self.screen)
                self.mes_layer.draw(self.screen, self.event.message)
                if self.key[K_z] == 1:
                    is_quit = self.mes_layer.next()
                    if is_quit: self.scene.transition("Field")
        self._quit()

if __name__ == "__main__":
    game = System()
    game.mainloop()
