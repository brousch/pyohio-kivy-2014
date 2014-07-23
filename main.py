#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import os
import random

import kivy
kivy.require('1.8.0')

from kivy.config import Config
Config.set('graphics', 'width', '1280')
Config.set('graphics', 'height', '720')

from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color
from kivy.graphics import Line
from kivy.lang import Builder
from kivy.metrics import sp
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import SlideTransition


__version__ = '0.1.5'


slides = ["Title", "WhatIsKivy", "MobileToolchain", "Pyjnius", "Pyobjus", 
          "Plyer", "KivyGarden", "KivyDesigner"]
for slide in slides:
    kv_file = "{}.kv".format(slide.lower())
    Builder.load_file(os.path.join("slides", kv_file))

class TitleScreen(Screen):
    pass

class WhatIsKivyScreen(Screen):
    pass

class MobileToolchainScreen(Screen):
    
    #def __init__(self, **kwargs):
    #    super(MobileToolchainScreen, self).__init__(**kwargs)
    
    def on_enter(self):
        self._draw_tree()

    def _draw_tree(self):
        with self.ids.treelayout.canvas.before:
            Color(1,1,1,1)
            Line(points=[self.ids.ph_kivy.center_x, self.ids.ph_kivy.center_y, 
                         self.ids.ph_py4a.center_x, self.ids.ph_py4a.center_y],
                 width=5)
            Line(points=[self.ids.ph_kivy.center_x, self.ids.ph_kivy.center_y, 
                         self.ids.ph_kivyios.center_x, self.ids.ph_kivyios.center_y],
                 width=5)
            Line(points=[self.ids.ph_py4a.center_x, self.ids.ph_py4a.center_y, 
                         self.ids.ph_buildozer.center_x, self.ids.ph_buildozer.center_y],
                 width=5)
            Line(points=[self.ids.ph_kivyios.center_x, self.ids.ph_kivyios.center_y, 
                         self.ids.ph_buildozer.center_x, self.ids.ph_buildozer.center_y],
                 width=5)
            Line(points=[self.ids.ph_py4a.center_x, self.ids.ph_py4a.center_y, 
                         self.ids.ph_pyjnius.center_x, self.ids.ph_pyjnius.center_y],
                 width=5)
            Line(points=[self.ids.ph_kivyios.center_x, self.ids.ph_kivyios.center_y, 
                         self.ids.ph_pyobjus.center_x, self.ids.ph_pyobjus.center_y],
                 width=5)
            Line(points=[self.ids.ph_pyjnius.center_x, self.ids.ph_pyjnius.center_y, 
                         self.ids.ph_plyer.center_x, self.ids.ph_plyer.center_y],
                 width=5)
            Line(points=[self.ids.ph_pyobjus.center_x, self.ids.ph_pyobjus.center_y, 
                         self.ids.ph_plyer.center_x, self.ids.ph_plyer.center_y],
                 width=5)            


class PyjniusScreen(Screen):
    pass

class PyobjusScreen(Screen):
    pass

class PlyerScreen(Screen):
    pass

class KivyGardenScreen(Screen):
    pass

class KivyDesignerScreen(Screen):
    pass


class KivyPres(BoxLayout):
    def __init__(self, **kwargs):
        super(KivyPres, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.content = ScreenManager()
        self.content.add_widget(TitleScreen(name='Title'))
        self.content.add_widget(WhatIsKivyScreen(name='WhatIsKivy'))
        self.content.add_widget(MobileToolchainScreen(name="MobileToolchain"))
        self.content.add_widget(PyjniusScreen(name='Pyjnius'))
        self.content.add_widget(PyobjusScreen(name='Pyobjus'))
        self.content.add_widget(PlyerScreen(name='Plyer'))
        self.content.add_widget(KivyGardenScreen(name='KivyGarden'))
        self.content.add_widget(KivyDesignerScreen(name='KivyDesigner'))

        self.add_widget(self.content)
        self.add_widget(SlideMenu(root=self))
        
    def get_current_slide(self):
        return self.content.current
    
    def set_current_slide(self, jump_to):
        if slides.index(jump_to) >= slides.index(self.get_current_slide()):    
            self.set_transition('left')
        else:
            self.set_transition('right')
        self.content.current = jump_to
    
    def set_transition(self, direction):
        self.content.transition = SlideTransition(direction=direction)


class FloatingButton(Button):
    def __init__(self, **kwargs):
        super(FloatingButton, self).__init__(**kwargs)
        self.velocity = [random.random(), random.random()]
        Clock.schedule_interval(self._update_pos, 1/60.)
    
    def _update_pos(self, dt):
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        
        if self.x < 0 or (self.x + self.width) > self.parent.width:
            self.velocity[0] *= -1
        if self.y < 0 or (self.y + self.height) > self.parent.height:
            self.velocity[1] *= -1
    
    def _dock(self):
        Clock.unschedule(self._update_pos)
        self.center = self.dock_to.center


Builder.load_file("slidemenu.kv")
class SlideMenu(BoxLayout):
    slide_spinner = ObjectProperty(None)
    
    def __init__(self, root, **kwargs):
        super(SlideMenu, self).__init__(**kwargs)
        self.root = root
        self.slide_spinner.values = slides
        
    def go_slide(self, spinner):
        if spinner.text in slides:
            self.root.set_current_slide(spinner.text)
            
    def go_prev(self):
        cur_index = slides.index(self.root.get_current_slide())
        prev_index = cur_index if cur_index==0 else cur_index-1
        self.root.set_current_slide(slides[prev_index])
        
    def go_next(self):
        cur_index = slides.index(self.root.get_current_slide())
        next_index = cur_index if cur_index==len(slides)-1 else cur_index+1
        self.root.set_current_slide(slides[next_index])


class KivyPresApp(App):
    font_size_regular = sp(20)
    font_size_large = font_size_regular * 2
    font_size_xlarge = font_size_regular * 3

    def build(self):
        return KivyPres()
    
    def on_pause(self):
        return true
        
    def on_resume(self):
        pass


if __name__ == '__main__':
    KivyPresApp().run()
