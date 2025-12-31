from kivy.config import Config #Font?
Config.set('kivy', 'default_font', ['vazir', 'Vazir-Medium.ttf', 'Vazir-Medium.ttf'])

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior 
from kivy.graphics import Color, Rectangle, Line

## For Persian writitng
from persian_helper import persian_text, IconButton, go_to
import bidi.algorithm
import arabic_reshaper

class GeneralInfoScreen(Screen):
    
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        ## Create the page layout
        layout = BoxLayout(orientation='vertical', padding=30, spacing=30)
        
        # Title
        layout.add_widget(Label(text=persian_text("مدیریت پرورش میگو"), halign='right', font_name='vazir_bold', font_size=30, size_hint=(1, 0.1)))
        
        # Logo
        logo = Image(source='assets/images/shrimp_logo.jpg', size_hint=(1, 0.4), fit_mode="scale-down")
        layout.add_widget(logo)
        
        ###### Create a 4x4 buttom  style ######
        
        ## Box for calculation button
        calc_box = BoxLayout(orientation='horizontal', size_hint=(1, 0.5), spacing=20, padding=30)
        calc_btn = IconButton(icon_source='assets/images/6633209.png', text="محاسبات")
        calc_btn.bind(on_press=lambda x: go_to(self.manager, 'calculation'))
        calc_box.add_widget(calc_btn)
    
        print("type of `calc_box` is ", type(calc_box))
        print("type of `calc_btn` is ", type(calc_btn))  # What will this print?
        print(isinstance(calc_btn, BoxLayout))  # True or False?
        
        ## Box for History
        hist_btn = IconButton(icon_source='assets/images/6633209.png', text="تاریخچه")
        hist_btn.bind(on_press=lambda x: go_to(self.manager, 'history'))
        calc_box.add_widget(hist_btn)
        
        layout.add_widget(calc_box)
        
        
        ## Second row of buttons
        second_box = BoxLayout(orientation='horizontal', size_hint=(1, 0.5), spacing=20, padding=30)
        
        ## Box for About us
        abot_btn = IconButton(icon_source='assets/images/6633209.png', text="درباره ما")
        abot_btn.bind(on_press=lambda x: go_to(self.manager, 'about_us'))
        second_box.add_widget(abot_btn)
        
        ## Box for Contact us
        cont_box = BoxLayout(orientation='horizontal', size_hint=(0.4, 0.4), spacing=10)
        cont_btn = IconButton(icon_source='assets/images/6633209.png', text="تماس با ما")
        cont_btn.bind(on_press=lambda x: go_to(self.manager, 'contact_us'))
        second_box.add_widget(cont_btn)
        
        layout.add_widget(second_box)
                
        self.add_widget(layout)

