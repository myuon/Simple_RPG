#! /usr/bin/python
# -*- coding:utf-8 -*-

import pygame
from pygame.locals import *

from utility import *

class ToolBox(object):
    def __init__(self):
        self._tools = {}
    
    def add(self, tool):
        if self._tools.has_key(tool): self._tools[tool] += 1
        else: self._tools[tool] = 1
    
    def use(self, tool):
        if self._tools[tool] != 1: self._tools.pop(tool)
        else: self._tools[tool] -= 1
    
    def list(self):
        return [u"{0} x {1:3d}".format(k,v) for k,v in self._tools.iteritems()]
    
    def is_empty(self):
        return self._tools == {}

class Status(object):
    def __init__(self, dic={"NAME": u"ゆうしゃ", "HP":10, "MP":8, "Lv":1, "Tools":ToolBox()}):
        self._param = dic
    
    def to_pair(self, attr):
        if attr == "NAME": return self._param[attr]
        return u"{0} {1:4d}".format(attr, self._param[attr])

    def to_command(self):
        return [self.to_pair("NAME"), self.to_pair("HP"), self.to_pair("MP"), self.to_pair("Lv")]

    @property
    def toolbox(self): return self._param["Tools"]
