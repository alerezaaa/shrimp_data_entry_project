from kivy.config import Config #Font?
from kivy.config import platform
Config.set('kivy', 'default_font', ['vazir', 'assets/fonts/Vazir-Medium.ttf', 'assets/fonts/Vazir-Medium.ttf'])
if platform in ("win", "linux", "macosx"):
    Config.set("graphics", "width", "470")
    Config.set("graphics", "height", "844")
    Config.set("graphics", "resizable", "1") 

from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior 
from kivy.graphics import Color, Rectangle, Line

from kivy.resources import resource_find
from kivy.core.text import LabelBase

import os
from db import init_db


## For Persian writitng
from persian_helper import persian_text
from persian_helper import IconButton
import bidi.algorithm
import arabic_reshaper

## Pages

### General Info Screen
from screen_general_info import GeneralInfoScreen

### Calculation
from screen_calculation import CalculationScreen

### Summary and Save to SQL screen
from screen_summary import SummaryScreen

### History Screen
from screen_history import HistoryScreen

### about us and contact us
from screen_about_us import AboutUsScreen
from screen_contact_us import ContactUsScreen


# font_path = resource_find("src/assets/fonts/Vazir-Medium.ttf")
# if not font_path:
#     raise FileNotFoundError("Font not packaged: src/assets/fonts/Vazir-Medium.ttf")

# LabelBase.register(name="vazir", fn_regular=font_path)


# 1. Register your Persian font
# 'Vazir' is the name you will use to reference the font in Kivy.
# 'vazir.ttf' is the actual file name.
LabelBase.register(name='vazir_bold', fn_regular='assets/fonts/Vazir-Medium.ttf')
LabelBase.register(name='vazir_light', fn_regular='assets/fonts/Vazir-Medium.ttf')
LabelBase.register(name='vazir', fn_regular='assets/fonts/Vazir-Medium.ttf')

# 2. Set the default font for all widgets
# The 'all' category applies the font to all text in the application



class SecondScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        layout.add_widget(Label(text='Step 2: Additional Info (Placeholder)'))
        
        # Placeholder for future content
        layout.add_widget(Label(text='This screen will contain additional\ndata collection fields later.'))
        
        # Buttons
        btn_layout = BoxLayout(size_hint=(1, 0.2), padding=20)
        back_btn = Button(text='Back')
        back_btn.bind(on_press=self.go_back)
        next_btn = Button(text='Next')
        next_btn.bind(on_press=self.go_to_next)
        
        btn_layout.add_widget(back_btn)
        btn_layout.add_widget(next_btn)
        layout.add_widget(btn_layout)
        
        self.add_widget(layout)
    
    def go_back(self, instance):
        self.manager.current = 'general'
    
    def go_to_next(self, instance):        
        self.manager.current = 'summary'


class MultiScreenApp(App):
    name = "shrimp_farming_decision_app"
    title = "Shrimp Farming Decision App"
    last_screen = StringProperty("")
    
    def build(self):
        # Initialize shared data storage
        self.user_data = {}
        
        self.db_path = os.path.join(self.user_data_dir, "shrimp.db")
        init_db(self.db_path)
        print(">> DB PATH:", self.db_path)
        print(">> App name:", self.name)
        print(">> user_data_dir:", self.user_data_dir)


        
        # Create screen manager
        sm = ScreenManager()
        
        # Add screens
        sm.add_widget(GeneralInfoScreen(name='general'))
        sm.add_widget(CalculationScreen(name='calculation'))
        sm.add_widget(SummaryScreen(name='summary'))
        sm.add_widget(HistoryScreen(name='history'))
        sm.add_widget(AboutUsScreen(name='about_us'))
        sm.add_widget(ContactUsScreen(name='contact_us'))

        
        return sm

if __name__ == '__main__':
    MultiScreenApp().run()
