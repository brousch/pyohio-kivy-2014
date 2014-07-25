from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
 
 
kv = """
<Test>:
    Button:
"""
 
Builder.load_string(kv)
 
 
class Test(BoxLayout):
    def __init__(self, **kwargs):
        super(Test, self).__init__(**kwargs)
 
 
class TestApp(App):
    def build(self):
        return Test()
 
if __name__ == '__main__':
    TestApp().run()