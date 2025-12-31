from kivy.config import Config #Font?
Config.set('kivy', 'default_font', ['vazir', 'Vazir-Medium.ttf', 'Vazir-Medium.ttf'])

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
# from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior 
from kivy.graphics import Color, Rectangle, Line
from kivy.metrics import sp 

## Import helpers
from persian_helper import persian_text, IconButton, go_to
## Import database functions
from db import insert_record, count_records

import bidi.algorithm
import arabic_reshaper



## The Class for Summary Screen

class SummaryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=50, spacing=50)
        
        layout.add_widget(Label(text=persian_text("خلاصه اطلاعات"), halign='right', font_name='vazir_bold', font_size=sp(24), size_hint=(1, 0.1)))
        
        table_container = BoxLayout(orientation='vertical', size_hint=(1, 0.8))
        
        self.table = GridLayout(
            cols=2,
            spacing=10,
            padding=10,
            orientation="rl-tb",
            row_default_height=sp(45),
            row_force_default=True,
            size_hint_y=None)
        
        self.table.bind(minimum_height=self.table.setter('height'))
        
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(self.table)
        
        table_container.add_widget(scroll)
        layout.add_widget(table_container)
        
        
        self.summary_label = Label(text=persian_text('برای ذخیره سازی اطلاعات روی ذخیره ضربه بزنید!'), halign='center', font_name='vazir', font_size=sp(16), markup=True, size_hint=(1, 0.1))
        layout.add_widget(self.summary_label)
        
        # Buttons
        btn_layout = BoxLayout(size_hint=(1, 0.2), spacing=20, padding=20)
        self.back_btn = IconButton(text='بازگشت')
        self.back_btn.bind(on_press=self.go_back)
        self.submit_btn = IconButton(text='ذخیره اطلاعات')
        self.submit_btn.bind(on_press=self.submit_data)
        
        btn_layout.add_widget(self.back_btn)
        btn_layout.add_widget(self.submit_btn)
        layout.add_widget(btn_layout)
        
        self.add_widget(layout)
    
    def on_enter(self):
        # This runs every time we enter this screen
        app = App.get_running_app()
        
        r = app.user_data.get('calculation', {})
                        
        if r:
            self.show_record(r)
        self.submit_btn.children[0].text = persian_text("ذخیره اطلاعات")
        self.submit_btn.disabled = False  # Disable to prevent multiple submissions
        self.submit_btn.opacity = 0.9  # Visual feedback
        self.back_btn.children[0].text = persian_text("بازگشت")
            
    def go_back(self, instance):
        self.show_record({})
        if self.submit_btn.disabled:
            go_to(self.manager, 'history')
        else:
            go_to(self.manager, 'calculation')

    
    def submit_data(self, instance):
        app = App.get_running_app()
        
        print("Data to save to database:", app.user_data)
        # Here you would save to your local database
        insert_record(app.db_path, app.user_data.get('calculation', {}))
        
        self.submit_btn.children[0].text = persian_text("ذخیره شد")
        self.submit_btn.disabled = True  # Disable to prevent multiple submissions
        self.submit_btn.opacity = 0.5  # Visual feedback
        self.back_btn.children[0].text = persian_text("رفتن به تاریخچه")
        
        
        
        n = count_records(app.db_path)
        
        self.summary_label.text = "[color=05f569]" + persian_text('اطلاعات با موفقیت ذخیره شد.') + "[/color]" + "\n" + persian_text(f'شما اکنون {n} رکورد در پایگاه داده خود دارید.')
        
    def _add_row(self, left_text, right_text, header=False, **kwargs):
        # You can swap Label -> your custom widgets if you want nicer style
        self.table.add_widget(Label(text=persian_text(left_text), **kwargs))
        self.table.add_widget(Label(text=persian_text(str(right_text)), **kwargs))

    def show_record(self, r: dict):
        self.table.clear_widgets()

        # header
        self._add_row("مـــورد", "مقــدار", header=True, font_size=sp(28))

        # rows (example)
        self._add_row("زمان", r.get("created_at", ""))
        self._add_row("غذای روزانه (کیلوگرم)", r.get("daily_feed", ""))
        self._add_row("میانگین وزن (گرم)", r.get("avg_weight", ""))
        self._add_row("تعداد فعلی", r.get("current_count", ""))
        self._add_row("تعداد لارو", r.get("larve_count", ""))
        self._add_row("نرخ بقا (درصد)", r.get("survival_rate", ""))
        self._add_row("بیومس کل (کیلوگرم)", r.get("biomass", ""))
        self._add_row("نرخ غذادهی (درصد)", r.get("daily_feeding_rate", ""))
        
        
