#! /usr/bin/python
# -*- coding:utf-8 -*-

#import pygame
#from pygame.locals import *

from utility import *

class Layer(object):
    EDGE_WIDTH = 4

    def __init__(self, rect, padding={'top':5, 'left':10, 'bottom':5, 'right':10}):
        self.rect = rect
        self.inner_rect = self.rect.inflate(-self.EDGE_WIDTH*2, -self.EDGE_WIDTH*2)
        self.is_visible = True
        self.is_focus = True
        self.padding = padding
        self.pos={'x':self.rect.left+self.padding['left'], 'y':self.rect.top+self.padding['top']}

    def draw(self, screen):
        if self.is_visible == False: return
        color = (255,255,255) if self.is_focus else (100,100,100)

        pygame.draw.rect(screen, color, self.rect, 0)
        pygame.draw.rect(screen, (0,0,0), self.inner_rect, 0)

    def active(self): self.is_visible = True
    def inactive(self): self.is_visible = False
    
    def focus(self): self.is_focus = True
    def defocus(self): self.is_focus = False

class SimpleMessageEngine(object):
    FONT_SIZE = 18

    def __init__(self, filename, rect, line_height=6):
        self.size = self.FONT_SIZE
        self.font = self.load(filename)
        self.messages = []
        self.rect = rect
        self.line_height = line_height
        self.running = False
        self.is_visible = True
        
    def load(self, filename, directory="font"):
        filename = get_path(filename, directory)
        try:
            font = pygame.font.Font(filename, self.size)
        except pygame.error, message:
            print "Cannot load font:", filename
            raise SystemExit, message
        return font
    
    def draw(self, screen, message, pos):
        if self.is_visible == False: return
        screen.blit(self.font.render(message, True, (255, 255, 255)), pos)
    
    def line_pos(self, pos, dy):
        return pos[0], pos[1]+(self.font.get_height()+self.line_height)*dy

    def active(self): self.is_visible = True
    def inactive(self): self.is_visible = False

class MessageEngine(SimpleMessageEngine):
    def __init__(self, filename, rect):
        super(MessageEngine, self).__init__(filename, rect)
        self.index = { 'page': None, 'line': None, 'letter': None }
        self.waiting = False
        self.running = False
        
    def new_index(self, keys):
        for key in keys:
            if self.index.has_key(key) == False:
                print "Illegal key:", key
                raise SystemExit, "Key Error"
    
            if key == 'page': self.index['page'] = IndexMarker(len(self.messages)+1)
            if key == 'line': self.index['line'] = IndexMarker(len(self.messages[self.index['page'].pos])+1)
            if key == 'letter': self.index['letter'] = IndexMarker(len(self.messages[self.index['page'].pos][self.index['line'].pos])+1, interval=3)

    def max_charactors(self, message):
        for i in range(1, len(message)):
            if self.font.size(message[:i])[0] > self.rect.width: return i-1
        return len(message)
    
    def split_by_width(self, message):
        length = self.max_charactors(message)
        if message[length:] == u'': return [message[:length]]
        return [message[:length]] + self.split_by_width(message[length:])
    
    def format(self, message):
        self.messages = []
        for line in message.rstrip().split("[p]"):
            self.messages.append(line.split("[l]"))
        self.messages = [[self.split_by_width(line) for line in page] for page in self.messages]
        self.messages = [flatten(page) for page in self.messages]

    def indexes_areas(self):
        areas = []
        for i in range(len(self.messages[self.index['page'].pos])):
            if i < self.index['line'].pos:
                areas.append(Rect(0, 0, self.rect.width, self.font.get_height()))
            elif i == self.index['line'].pos:
                areas.append(Rect((0, 0), self.font.size(self.messages[self.index['page'].pos][i][:self.index['letter'].pos])))
            else:
                areas.append(Rect(0, 0, 0, 0))
        return areas
    
    def init(self, message):
        self.format(message)
        self.running = True
        self.new_index(['page', 'line', 'letter'])
    
    def draw(self, screen, message, pos):
        if self.running == False: self.init(message)
        areas = self.indexes_areas()
        for i in range(len(self.messages[self.index['page'].pos])):
            screen.blit(self.font.render(self.messages[self.index['page'].pos][i], True, (255, 255, 255)), (pos[0], pos[1]+(self.font.get_height()+self.line_height)*i), area=areas[i])

        if self.waiting:
            screen.blit(self.font.render(u"▽", True, (255, 255, 255)), (pos[0]+self.rect.width/2-self.font.size("▽")[0]/2, pos[1]+self.rect.height-self.font.get_height()))
        else:
            self.count()

    def count(self):
        self.index['letter'].next()
        if self.index['letter'].is_next_end():
            self.index['line'].next()
            if self.index['line'].is_next_end():
                self.waiting = True
            else:
                self.new_index(['letter'])

    def next(self):
        self.waiting = False
        self.index['page'].next()
        if self.index['page'].is_next_end():
            self.running = False
            return True
        self.new_index(['line', 'letter'])
        return False

class MessageLayer(Layer):
    def __init__(self, filename, rect, padding={'top':15, 'left':20, 'bottom':15, 'right':20}):
        super(MessageLayer, self).__init__(rect, padding)
        self.mes_engine = MessageEngine(filename, Rect(0, 0, rect.width - padding['left'] - padding['right'], rect.height - padding['bottom'] - padding['top']))

    def draw(self, screen, message):
        super(MessageLayer, self).draw(screen)
        self.mes_engine.draw(screen, message, (self.rect.left + self.padding['left'], self.rect.top + self.padding['top']))

    def next(self): return self.mes_engine.next()

class StaticLayer(Layer):
    def __init__(self, filename, rect, messages=[], padding={'top':15, 'left':20, 'bottom':15, 'right':20}):
        super(StaticLayer, self).__init__(rect, padding)
        self.messages = messages
        self.mes_engine = [SimpleMessageEngine(filename, rect)]*len(self.messages)
    
    def draw(self, screen):
        super(StaticLayer, self).draw(screen)
        for i in range(len(self.messages)):
            self.mes_engine[i].draw(screen, self.messages[i], self.mes_engine[i].line_pos((self.rect.left + self.padding['left'], self.rect.top + self.padding['top']), i))
    
    def active(self):
        super(StaticLayer, self).active()
        for m in self.mes_engine:
            m.active()

    def inactive(self):
        super(StaticLayer, self).inactive()
        for m in self.mes_engine:
            m.inactive()

class StatusLayer(StaticLayer):
    def __init__(self, filename, rect, status):
        super(StatusLayer, self).__init__(filename, rect, status.to_command())
        self.status = status

    def draw(self, screen):
        self.messages = self.status.to_command()
        super(StatusLayer, self).draw(screen)

class CommandLeaf(object):
    def __init__(self, command):
        self.sub_layers = []
        self.parent = None
        self.command = command
    
    def add_parent(self, cls, root):
        self.parent = cls
    
    def draw(self, *arg): return
    def active(self, *arg): return
    def inactive(self, *arg): return
    def input(self, *arg):
        raise SystemExit, "Called `input' of CommandLeaf"

class CommandLayer(StaticLayer):
    def __init__(self, filename, rect, messages=[], padding={'top':15, 'left':50, 'bottom':15, 'right':20}):
        super(CommandLayer, self).__init__(filename, rect, messages, padding)
        self.index = Bounded(len(self.messages))
        self.index_engine = SimpleMessageEngine(filename, rect)
        self.parent = None
        self.root = None
        self.sub_layers = []

    def add_sub_layer(self, cls, root):
        self.sub_layers.append(cls)
        cls.add_parent(self, root)
    
    def add_parent(self, cls, root):
        self.parent = cls
        self.root = root
        
    def active(self):
        super(CommandLayer, self).active()
        self.index_engine.active()
    
    def inactive(self):
        super(CommandLayer, self).inactive()
        self.index_engine.inactive()
        self.focus()
    
    def draw(self, screen):
        super(StaticLayer, self).draw(screen)
        for i in range(len(self.messages)):
            self.mes_engine[i].draw(screen, self.messages[i], self.mes_engine[i].line_pos((self.rect.left + self.padding['left'], self.rect.top + self.padding['top']), i))
        self.index_engine.draw(screen, u"→", self.index_engine.line_pos((self.rect.left + self.padding['left'] - 30, self.rect.top + self.padding['top']), self.index.index))

        for s in self.sub_layers:
            s.draw(screen)
        
    def input(self, key):
        if key[K_DOWN] == 1: self.index.next()
        if key[K_UP] == 1: self.index.back()
        if key[K_z] == 1:
            self.defocus()
            self.sub_layers[self.index.index].active()
            return self.sub_layers[self.index.index]
        if key[K_x] == 1:
            self.inactive()
            self.parent.focus()
            return self.parent
        
class ToolBoxLayer(CommandLayer):
    def __init__(self, filename, rect, toolbox):
        super(ToolBoxLayer, self).__init__(filename, rect, messages=toolbox.list())
        self.toolbox = toolbox
        self.inactive()

    def draw(self, screen):
        super(ToolBoxLayer, self).draw(screen)
        if self.toolbox.is_empty(): self.index_engine.inactive()

    def input(self, key):
        if key[K_DOWN] == 1: self.index.next()
        if key[K_UP] == 1: self.index.back()
        if key[K_z] == 1:
#            self.defocus()
#            self.sub_layers[self.index.index].active()
            return self.sub_layers[self.index.index]
        if key[K_x] == 1:
            self.inactive()
            self.parent.focus()
            return self.parent

class LayerManager(object):
    FUNCTIONS = {0:u"しらべる", 1:u"どうぐ", 2:u"スキル", 3:u"せーぶ", 4:u"ろーど"}
    TAB_LIST = {CommandLayer:0, ToolBoxLayer:1}
    
    def __init__(self, filename, rect, status):
        self.mes_layer = MessageLayer(filename, rect)
        self.status = StatusLayer(filename, Rect(530,0,110,140), status)
        self.scene = None
        self.command = CommandLayer(filename, Rect(0,0,160,300), self.FUNCTIONS.values())
        self.command.add_parent(self, self)
        self.command.add_sub_layer(CommandLeaf("look"), self)
        self.command.add_sub_layer(ToolBoxLayer(filename, Rect(160,0,450,480), status.toolbox), self)
        self.command.sub_layers[1].add_sub_layer(CommandLeaf("tool"), self.command)
        self.command.add_sub_layer(CommandLeaf("skill"), self)
        self.command.add_sub_layer(CommandLeaf("save"), self)
        self.command.add_sub_layer(CommandLeaf("load"), self)
        self.sub_layers = [self.command]
        
        self.target = self.command
        
    def setup(self):
        self.mes_layer.active()
        self.mes_layer.focus()
        
    def draw(self, screen):
        self.status.draw(screen)
        self.command.draw(screen)
    
    def focus(self):
        self.target = None
        
    def next(self): return self.mes_layer.next()
    
    def set_focus(self, cls):
        self.target = cls
    
    def input(self, key, scene):
        cls = self.target.input(key)
        if self.target is None:
            self.target = self.command
            self.command.active()
            scene.transition("Field")
        elif isinstance(cls, CommandLeaf):
            self.target.focus()
            if cls.command == "look":
                scene.transition("Field")

                def look(cls):
                    info = cls.event.look(cls.scene, cls.map)
                    if info is None:
                        cls.event.announce(cls.scene, u"とくに何も見つからなかった。")
                    else:
                        cls.event.announce(cls.scene, u"アイテム番号 {0:03d}を発見した！".format(info['index']))
                return look
        elif cls is not None:
            self.set_focus(cls)
    
