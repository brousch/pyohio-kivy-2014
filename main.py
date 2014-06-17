#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from kivy.config import Config
Config.set('graphics', 'width', '1280')
Config.set('graphics', 'height', '720')

from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import sp
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import SlideTransition


__version__ = '0.1.3'


slides = ["Title", "WhatIsKivy", "MobileToolchain", "Pyjnius", "Pyobjus", 
          "Plyer"]
for slide in slides:
    Builder.load_file("slide_{}.kv".format(slide.lower()))

class TitleScreen(Screen):
    pass

class WhatIsKivyScreen(Screen):
    pass

class MobileToolchainScreen(Screen):
    pass

class PyjniusScreen(Screen):
    pass

class PyobjusScreen(Screen):
    pass

class PlyerScreen(Screen):
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
    font_size_regular = sp(18)
    font_size_large = font_size_regular * 2
    font_size_xlarge = font_size_regular * 3

    def build(self):
        return KivyPres()


if __name__ == '__main__':
    KivyPresApp().run()
