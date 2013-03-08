#! /usr/bin/python
# -*- coding:utf-8 -*-

import pygame
from pygame.locals import *

from utility import *

class Event(object):
    def __init__(self):
        self._info = {}
        
    def _update(self, sequence):
        self._info.update(sequence)
    
    def register(self):
        pass

    @property
    def info(self): return self._info

class NPCTalkEvent(Event):
    def __init__(self, data):
        super(NPCTalkEvent, self).__init__()
        self._update({
                     'type': data[0],
                     'chara': (int(data[1]), int(data[2])),
                     'position': (int(data[3]), int(data[4])),
                     'direction': int(data[5]),
                     'movable': bool(data[6]),
                     'message': data[7],
                     })
    
    def register(self, fun):
        event_id = "{0}_{1}".format(*self._info['position'])
        fun("vx_chara01_a.png", event_id=event_id, pos=self._info['position'], chara=self._info['chara'], movable=self._info['movable'])
        return "a_events", event_id, {'type':"TALK", 'content':self._info["message"]}
    
class MoveEvent(Event):
    def __init__(self, data):
        super(MoveEvent, self).__init__()
        self._update({
                     'type': data[0],
                     'position': (int(data[1]), int(data[2])),
                     'map': data[3],
                     'to_position': (int(data[4]), int(data[5])),
                     })

    def register(self, fun):
        event_id = "{0}_{1}".format(*self._info['position'])
        fun(self._info['position'], event_id=event_id)
        return "p_events", event_id, {'type':"MOVE", 'map':self._info['map'], 'to_position':self._info['to_position']}

class ItemEvent(Event):
    def __init__(self, data):
        super(ItemEvent, self).__init__()
        self._update({
                     'type': data[0],
                     'position': (int(data[1]), int(data[2])),
                     'index': data[3],
                     'maptip': (int(data[4]), int(data[5])),
                     })

class EventManager(Manager):
    def __init__(self, filename, directory="map"):
        self.kind = ["CHARA", "MOVE"]
        self.create(filename, directory)
        
    def create(self, filename, directory="map"):
        self.loaded_events = []
        self.load(filename, directory)
        self.a_events = {}
        self.p_events = {}
        
    def make_data(self, data):
        data_ = data.split(",", 7)
        pair = dict(zip(self.kind, [NPCTalkEvent, MoveEvent]))
        
        if data_[0] not in self.kind:
            print "received undefined type:{0}".format(data_[0])
            raise SystemExit, "Undefined Type Error"
        
        return pair[data_[0]](data_)

    def load(self, filename, directory):
        with open(get_path(insert_path(filename, "event"), directory=directory), 'r') as f:
            for line in f:
                if line.startswith("#"): continue
                self.loaded_events.append(self.make_data(line.decode('utf-8')))
    
    def register(self, registers):
        pair = dict(zip(self.kind, registers))
        for event in self.loaded_events:
            aorp, event_id, dic = event.register(pair[event.info['type']])
            if aorp == "a_events":
                self.a_events[event_id] = dic
            elif aorp == "p_events":
                self.p_events[event_id] = dic

    def a_check(self, event_id, key):
        if key[K_z] == 1 and self.a_events.has_key(event_id):
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
    
    def look(self, scene, scmap):
        info, event = self.pull_event(scmap.check_gazing, self.a_check, {'K_z': 1})
        if info is not None and event is not None:
            if event['type'] == "TALK":
                info.change_dir(step_dir(tuple([scmap.player.pos_adjust(scmap.offset)[i] - info.pos[i] for i in [0,1]])))
                self.message = event['content']
                scene.transition("Layer")
                return scmap.check_pos
        
        return None
        
    def run(self, scene, scmap, key):
        info, event = self.pull_event(scmap.check_gazing, self.a_check, key)
        if info is not None and event is not None:
            if event['type'] == "TALK":
                info.change_dir(step_dir(tuple([scmap.player.pos_adjust(scmap.offset)[i] - info.pos[i] for i in [0,1]])))
                self.message = event['content']
                scene.transition("Layer")
            
        info, event = self.pull_event(scmap.check_pos, self.p_check, key)
        if info is not None and event is not None:
            if event['type'] == "MOVE":
                scmap.create(event['map'], event['to_position'])
                return event['map']
        
        if key[K_z] == 1 and scene.name == "Field":
            scene.transition("Command")
            return
        
        return None

    def announce(self, scene, message):
        self.message = message
        scene.transition("Layer")
