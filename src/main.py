#! /usr/bin/python
# -*- coding:utf-8 -*-

import pygame
from pygame.locals import *

from utility import *

import field_chara as fc
import field
import layer
import event
import battle

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

class System(GameFrame):
    def __init__(self):
        super(System, self).__init__(title=GAME_TITLE, size=SCREEN.size)

        self.map = field.ScrollMap("field1.txt")
        self.map.add_chara(fc.Player("vx_chara01_a.png", name="player"), is_player=True)
        self.event = event.EventManager("field1.txt")
        self.event.register([lambda *args, **kwargs:self.map.add_chara(fc.NPC(*args, **kwargs)),
                             lambda pos, *args, **kwargs:self.map.event_map.add(fc.SimpleEvent(*args, **kwargs), pos)])
        
        self.mes_layer = layer.MessageLayer("ipag.ttf", Rect(140,334,360,140))
        self.scene.transition("Field")
        
        self.battle = battle.BattleField()
        
    def create(self, filename):
        self.event.create(filename)
        self.event.register([lambda *args, **kwargs:self.map.add_chara(fc.NPC(*args, **kwargs)),
                             lambda pos, *args, **kwargs:self.map.event_map.add(fc.SimpleEvent(*args, **kwargs), pos)])

    def key_step(self):
        ks_pair = {K_UP: (0, -1), K_DOWN: (0, 1), K_RIGHT: (1, 0), K_LEFT: (-1, 0)}
        step = [ks_pair[i] for i in ks_pair if self.key[i]]
        return step[0] if step != [] else (0,0)
    
    def mainloop(self):
        if self.scene.name == "Field":
            self.map.draw(self.screen)
            self.map.move(self.key_step())
            if self.map.scroll.enable == False:
                info = self.event.run(self.scene, self.map, self.key)
                if info is not None:
                    self.create(info)
                
#                self.battle.run(self.scene)

            if self.map.scroll() != (0,0): self.battle.roll()

        elif self.scene.name == "Layer":
            self.map.draw(self.screen)
            self.mes_layer.draw(self.screen, self.event.message)
            if self.key[K_z] == 1:
                is_quit = self.mes_layer.next()
                if is_quit: self.scene.transition("Field")
        
        elif self.scene.name == "Battle":
            pass            
    
    def step(self): return self._step()
    def quit(self): return self._quit()

if __name__ == "__main__":
    game = System()
    while game.step() != -1:
        game.mainloop()
    game.quit()
