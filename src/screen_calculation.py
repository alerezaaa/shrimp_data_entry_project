from kivy.config import Config #Font?
Config.set('kivy', 'default_font', ['vazir', 'Vazir-Medium.ttf', 'Vazir-Medium.ttf'])

from datetime import datetime
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior 
from kivy.graphics import Color, Rectangle, Line
from kivy.metrics import sp 

## For Persian writitng
from persian_helper import persian_text, go_to, IconButton
import bidi.algorithm
import arabic_reshaper

class CalculationScreen(Screen):
    
    class CalcInputs (BoxLayout):
        def __init__(self, input_title, input_filter='float', **kwargs):
            super().__init__(spacing=10, padding=10, orientation="vertical", size_hint=(1, 1), **kwargs)
            
            self.add_widget(Label(text=persian_text(input_title), base_direction='rtl', halign='right', font_name='vazir_bold', font_size=28, size_hint=(1, 0.3)))
            self.value = TextInput(
                hint_text=persian_text(input_title),
                base_direction='rtl',
                halign='right',
                multiline=False,
                font_size=28,
                size_hint=(1, 0.7),
                input_filter=input_filter
            )
            self.add_widget(self.value)
            
        def get_value(self):
            try:
                return float(self.value.text)
            except ValueError:
                return 0.0
            
        def get_value_str(self):
            try:
                return str(float(self.value.text))
            except ValueError:
                return persian_text('عددی وارد نشده یا خطایی پیش آمده')
            
        def reset(self):
            self.value.text = ''
    
    
    class display_results (BoxLayout):
        def __init__(self, title, calculated, size_hint=(1, 0.233), **kwargs):
            super().__init__(orientation='horizontal', padding=10, spacing=10)
            
            numbr_layout = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint=(1, 1))
            self.number = Label(text=str(calculated), halign='right', font_name='vazir_bold', font_size=sp(15), size_hint=(1, 1))
            numbr_layout.add_widget(self.number)
            label_layout = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint=(1, 1))
            label_layout.add_widget(Label(text=persian_text(title), base_direction='rtl', halign='left', font_name='vazir_bold', font_size=sp(15), size_hint=(1, 1)))
            
            self.add_widget(numbr_layout)
            self.add_widget(label_layout)
            
        def reset(self):
            self.number.text = ''


    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.did_math = False
                
        ## Create the page layout
        layout = BoxLayout(orientation='vertical', padding=50, spacing=50)

        ## seperate input and calculation layout
        INPT_layout = BoxLayout(orientation='vertical', padding=30, spacing=30, size_hint=(1, 0.55))
        CALC_layout = BoxLayout(orientation='vertical', padding=30, spacing=30, size_hint=(1, 0.35))
        BTON_Layout = BoxLayout(orientation='horizontal', padding=30, spacing=30, size_hint=(1, 0.10))
        
        
        next_button = IconButton(text="ذخیره", size_hint=(0.5, 1))
        next_button.bind(on_press=lambda x: go_to(self.manager, 'current') if self.did_math else None)
        
        home_button = IconButton(text="صفحه اصلی", size_hint=(0.5, 1))
        home_button.bind(on_press=lambda x: go_to(self.manager, 'general'))
        
        BTON_Layout.add_widget(home_button)
        BTON_Layout.add_widget(next_button)
        
        
        # Title
        layout.add_widget(Label(text=persian_text("درصد بازماندگی / ضریب تبدیل"), halign='right', font_name='vazir_bold', font_size=36, size_hint=(1, 0.1)))
        
        
        # Daily-food-intake input
        input1_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.1), spacing=1)
        self.daily_feed_weight = self.CalcInputs(input_title="میزان غذای روزانه (کیلوگرم)")
        input1_layout.add_widget(self.daily_feed_weight)
        
        INPT_layout.add_widget(input1_layout)
        
        # mean of weight input
        # input2_layout = StackLayout(orientation='rl-tb')
        input2_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=1)
        self.daily_feed_perc = self.CalcInputs(input_title="درصد غذا دهی")
        self.weight_mean = self.CalcInputs(input_title="میانگین وزن (گرم)")
        input2_layout.add_widget(self.daily_feed_perc)
        input2_layout.add_widget(self.weight_mean)
        
        INPT_layout.add_widget(input2_layout)
        
        
        # Current Count
        count_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=1)
        self.current_count = self.CalcInputs(input_title="تعداد فعلی میگو", input_filter='int')
        count_layout.add_widget(self.current_count)
        
        INPT_layout.add_widget(count_layout)
        
        
        # Total Number of Larve
        input3_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=1)
        self.larve_saving = self.CalcInputs(input_title="تعداد لارو ذخیره‌سازی", input_filter='int')
        input3_layout.add_widget(self.larve_saving)
        
        INPT_layout.add_widget(input3_layout)
        
        layout.add_widget(INPT_layout)
        
        
        
        submit_button = IconButton(text="محاسبه کن", font_size=sp(20), size_hint=(1, 0.1))
        submit_button.bind(on_press=self.do_the_math)
        
        layout.add_widget(submit_button)
        
        


        # RESULTS | CALCULATION
        
        CALC_layout.add_widget(Label(text=persian_text('مقادیر محاسبه شده به شرح زیر است'), font_size=28, size_hint=(1, 0.3)))
        ## layouts
        
        
        
        self.cal_survival_rate_layout = self.display_results(title='نرخ بقا', calculated=self.larve_saving.get_value_str())
        self.cal_daily_feeding_rate_layout = self.display_results(title='نرخ غذادهی روزانه', calculated=self.larve_saving.get_value_str())
        self.cal_biomass = self.display_results(title='بیومس کل', calculated=self.larve_saving.get_value_str())
        
        
        CALC_layout.add_widget(self.cal_survival_rate_layout)
        CALC_layout.add_widget(self.cal_daily_feeding_rate_layout)
        CALC_layout.add_widget(self.cal_biomass)
        
        
        
        layout.add_widget(CALC_layout)

        
        layout.add_widget(BTON_Layout)
        
        self.add_widget(layout)
        
    def on_enter(self, *args):
        app = App.get_running_app()
        
        # prev = self.manager.previous()
        # prev_name = prev.name if hasattr(prev, "name") else prev  # handle Screen or string
        
        # print(f"Calculation Screen: on_pre_enter from {prev_name}")
                
        if app.last_screen == 'general':
            print("Resetting Calculation Screen inputs...")           
            self.daily_feed_weight.reset()
            self.daily_feed_perc.reset()
            self.weight_mean.reset()
            self.current_count.reset()
            self.larve_saving.reset()
            self.cal_survival_rate_layout.reset()
            self.cal_daily_feeding_rate_layout.reset()
            self.cal_biomass.reset()
            self.did_math = False
            
    # def on_enter(self):
    #     pass
    
    def do_the_math(self, instance):
        try:
            daily_feed = self.daily_feed_weight.get_value()
            feed_percentage = self.daily_feed_perc.get_value()
            avg_weight = self.weight_mean.get_value()
            current_count = int(self.current_count.get_value())
            larve_count = int(self.larve_saving.get_value())
            
            # print("Starting calculations...")
            # print("Inputs are: daily_feed= {}, feed_percentage= {}, avg_weight= {}, current_count= {}, larve_count= {}".format(
            #           daily_feed, feed_percentage, avg_weight, current_count, larve_count))
            
            
            if larve_count > 0:
                survival_rate = round((current_count / larve_count) * 100.000, 3)
            else:
                survival_rate = 0
                
                
            biomass = round((avg_weight * current_count) / 1000.000, 3)
            
            
            if biomass > 0:
                daily_feeding_rate = round((daily_feed / biomass) * 100.000, 3)
            else:
                daily_feeding_rate = 0
                
                
            self.cal_survival_rate_layout.number.text = str(survival_rate)
            self.cal_daily_feeding_rate_layout.number.text = str(daily_feeding_rate)
            self.cal_biomass.number.text = str(biomass)
                
            # print("Data recieved for calculation:\n"
            #       "> daily_feed= {}, feed_percentage= {}, avg_weight= {}, current_count= {}, larve_count= {}\n".format(
            #           daily_feed, feed_percentage, avg_weight, current_count, larve_count))
            # print("Results are: Survival Rate= {}, Daily Feeding Rate= {}, Biomass={}\n".format(
            #     survival_rate, daily_feeding_rate, biomass))
            # print("Results Set to: Survival Rate= {}, Daily Feeding Rate= {}, Biomass={}".format(self.cal_survival_rate_layout.number, self.cal_daily_feeding_rate_layout.number, self.cal_biomass.number))
            
            # save to app data
            app = App.get_running_app()
            
            app.user_data['calculation'] = {
                'created_at': datetime.now().isoformat(timespec="seconds"),
                'daily_feed': daily_feed,
                'feed_percentage': feed_percentage,
                'avg_weight': avg_weight,
                'current_count': current_count,
                'larve_count': larve_count,
                'survival_rate': survival_rate,
                'biomass': biomass,
                'daily_feeding_rate': daily_feeding_rate                
            }
            
            self.did_math = True
            
            
        except ValueError:
            msg = persian_text("لطفا اعداد معتبر وارد کنید")
            self.cal_survival_rate_layout.number.text = msg
            self.cal_daily_feeding_rate_layout.number.text = msg
            self.cal_biomass.number.text = msg

    
    def go_to_main_screen(self, instance):
        # Save all current data before moving
        app = App.get_running_app()
        
        self.manager.current = 'general'