#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from functools import partial
import os
import random

import kivy
kivy.require('1.8.0')

from kivy.config import Config
Config.set('graphics', 'width', '1280')
Config.set('graphics', 'height', '720')

from kivy.app import App
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.graphics import Color
from kivy.graphics import Line
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.metrics import sp
from kivy.properties import NumericProperty
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.uix.accordion import AccordionItem
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.codeinput import CodeInput
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.scatter import Scatter
from kivy.uix.videoplayer import VideoPlayer
from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import SlideTransition

from libs import browser
from plyer import battery
from plyer.utils import platform


__version__ = '0.2.2'


slides = ["Title", "WhatIsKivy", "MobileToolchain", "PythonForAndroid", 
          "KivyIOs", "Buildozer", "Pyjnius", "Pyobjus", "Plyer", "KivyGarden", 
          "KivyDesigner", "Information"]
for slide in slides:
    kv_file = "{}.kv".format(slide.lower())
    Builder.load_file(os.path.join("slides", kv_file))


class TitleScreen(Screen):
    def on_enter(self):
        Clock.schedule_interval(self._schedule_animations, 60)
    
    def _schedule_animations(self, dt):
        Clock.schedule_once(partial(self._animate_title_out, self.ids.title1))
        Clock.schedule_once(partial(self._animate_title_out, self.ids.title2), 1)
        Clock.schedule_once(partial(self._animate_title_out, self.ids.title3), 2)
        Clock.schedule_once(partial(self._animate_title_out, self.ids.title4), 3)
        Clock.schedule_once(partial(self._animate_title_in, self.ids.title1), 4)
        Clock.schedule_once(partial(self._animate_title_in, self.ids.title2), 5)
        Clock.schedule_once(partial(self._animate_title_in, self.ids.title3), 6)
        Clock.schedule_once(partial(self._animate_title_in, self.ids.title4), 7)
    
    def _animate_title_out(self, widget, dt):
        anim = Animation(x=4000, duration=4, transition='out_back')
        anim.start(widget)
    
    def _animate_title_in(self, widget, dt):
        widget.x = -4000
        anim = Animation(x=0, duration=4, transition='in_back')
        anim.start(widget)


class WhatIsKivyScreen(Screen):
    def on_enter(self):
        vp = VideoPlayer(source=os.path.join("videos",
                                             "gvr_pycon2014_keynote_kivy.mp4"),
                         options={'allow_stretch': True})
        self.ids.video_ai.add_widget(vp)
        
        with open(os.path.join("slides", "whatiskivy.kv"), 'r') as kv_file:
            self.ids.kv_demo.text = kv_file.read()
        
        with open(os.path.join("snippets", "minimal_app.txt"), 'r') as py_file:
            self.ids.min_app.text = py_file.read()
        

class MobileToolchainScreen(Screen):    
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


class PythonForAndroidScreen(Screen):
    indic = NumericProperty(0)
    sad = NumericProperty(0)


class KivyIOsScreen(Screen):
    def on_enter(self):
        screenshots = ["2048", "angryblocks", "numberlane", "processcraft", 
                       "quizzn"]
        for ss in screenshots:
            src = os.path.join("images", "ios_ss_{}.jpg".format(ss))
            image = Image(source=src, allow_stretch=True)
            self.ids.ios_gallery.add_widget(image)


class BuildozerScreen(Screen):
    def open_comparisonpopup1(self):
        pop = ComparisonPopup1().open()
        
    def open_comparisonpopup2(self):
        pop = ComparisonPopup2().open()
        
    def open_futurepopup(self):
        pop = FuturePopup().open()


class PyjniusScreen(Screen):
    acc_x = StringProperty("N/A")
    acc_y = StringProperty("N/A")
    acc_z = StringProperty("N/A")
    battery_charging = StringProperty("N/A")
    battery_percent = StringProperty("N/A")
    latitude = StringProperty("N/A")
    longitude = StringProperty("N/A")
    
    def on_enter(self):
        Clock.schedule_interval(self._get_battery_status, 1)
    
    def _get_battery_status(self, dt=0):
        try:
            status = battery.status
            if status['connected']:
                self.battery_charging = "Charging"
            else:
                self.battery_charging = "Not Charging"
            self.battery_percent = "{}%".format(status['percentage'])
        except NotImplementedError:
            Logger.info("Battery facade not implemented on this platform.")


class PyobjusScreen(Screen):
    def on_enter(self):
        with open(os.path.join("snippets", 
                               "pyobjus_snippet.txt"), 'r') as py_file:
            self.ids.pyobjus_snippet.text = py_file.read()


class PlyerScreen(Screen):
    def on_enter(self):
        with open(os.path.join("snippets", "comp_battery_pyjnius.txt"), 'r') as file1:
            self.ids.comp_battery_pyjnius.text = file1.read()
        with open(os.path.join("snippets", "comp_battery_plyer.txt"), 'r') as file2:
            self.ids.comp_battery_plyer.text = file2.read()


class KivyGardenScreen(Screen):
    pass


class KivyDesignerScreen(Screen):
    pass


class InformationScreen(Screen):
    pass


class KivyPres(BoxLayout):
    def __init__(self, **kwargs):
        super(KivyPres, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.content = ScreenManager()
        self.content.add_widget(TitleScreen(name='Title'))
        self.content.add_widget(WhatIsKivyScreen(name='WhatIsKivy'))
        self.content.add_widget(MobileToolchainScreen(name="MobileToolchain"))
        self.content.add_widget(PythonForAndroidScreen(name='PythonForAndroid'))
        self.content.add_widget(KivyIOsScreen(name='KivyIOs'))
        self.content.add_widget(BuildozerScreen(name='Buildozer'))
        self.content.add_widget(PyjniusScreen(name='Pyjnius'))
        self.content.add_widget(PyobjusScreen(name='Pyobjus'))
        self.content.add_widget(PlyerScreen(name='Plyer'))
        self.content.add_widget(KivyGardenScreen(name='KivyGarden'))
        self.content.add_widget(KivyDesignerScreen(name='KivyDesigner'))
        self.content.add_widget(InformationScreen(name='Information'))

        self.add_widget(self.content)
        self.slide_menu = SlideMenu(root=self)
        self.add_widget(self.slide_menu)
        
    def get_current_slide(self):
        return self.content.current
    
    def set_current_slide(self, jump_to):
        if slides.index(jump_to) >= slides.index(self.get_current_slide()):    
            self.set_transition('left')
        else:
            self.set_transition('right')
        self.content.current = jump_to
        self.slide_menu.ids.slide_spinner.text = ""
    
    def set_transition(self, direction):
        self.content.transition = SlideTransition(direction=direction)


class FloatingButton(Button):
    def __init__(self, **kwargs):
        super(FloatingButton, self).__init__(**kwargs)
        self.velocity = [random.random()*2, random.random()*2]
        Clock.schedule_interval(self._update_pos, 1/60.)
    
    def _update_pos(self, dt):
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        
        if self.x < 0 or (self.x + self.width) > self.parent.width:
            self.velocity[0] *= -1
        if self.y < 0 or (self.y + self.height) > self.parent.height:
            self.velocity[1] *= -1
    
    def _dock(self):
        if not self.docked:
            self.docked = True
            Clock.unschedule(self._update_pos)
            anim = Animation(x=self.dock_to.center_x - self.width / 2, 
                             y=self.dock_to.center_y - self.height / 2,
                             duration=2, 
                             transition='out_elastic')
            anim.start(self)
        else:
            App.get_running_app().root.set_current_slide(self.screen)


class ComparisonPopup1(Popup):
    pass

class ComparisonPopup2(Popup):
    pass

class FuturePopup(Popup):
    pass


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
    font_size_regular = sp(25)
    font_size_large = font_size_regular * 2
    font_size_xlarge = font_size_regular * 3

    def build(self):
        return KivyPres()
    
    def on_pause(self):
        return true
        
    def on_resume(self):
        pass
    
    def open_browser(self, url):
        browser.open_url(url)


if __name__ == '__main__':
    KivyPresApp().run()
