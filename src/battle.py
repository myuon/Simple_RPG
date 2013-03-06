#! /usr/bin/python
# -*- coding:utf-8 -*-

import pygame
from pygame.locals import *

import utility
import random

class BattleField(object):
    def __init__(self, maximum=10):
        self._maximum = maximum
        self._dice = -1
    
    def roll(self):
        self._dice = random.randint(0, self._maximum-1)
    
    def run(self, scene):
        if self._dice == 0: scene.transition("Battle")

class Field(object):
    def __init__(self):
        pass
