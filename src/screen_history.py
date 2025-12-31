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
from kivy.uix.popup import Popup
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.graphics import Color, Rectangle, Line
from kivy.metrics import sp
from kivy.properties import StringProperty, BooleanProperty, NumericProperty, ObjectProperty

from db import fetch_records, delete_record

## For Persian writitng
from persian_helper import persian_text
from persian_helper import IconButton



# --- Configuration ---
# We define the column widths here so we can change them easily for BOTH the header and the rows
COL_WIDTHS = {
    'date': sp(130),
    'daily_feed': sp(90),
    'feed_percentage': sp(90),
    'avg_weight': sp(90),
    'current_count': sp(90),
    'larve_count': sp(90),
    'survival_rate': sp(90),
    'biomass': sp(90),
    'daily_feeding_rate': sp(90),
    'delete_button': sp(50),
}
TOTAL_WIDTH = sum(COL_WIDTHS.values()) + sp(30) # Extra space for padding

class HistoryRow(BoxLayout):
    
    # Define all properties to receive data
    date = StringProperty()
    daily_feed = StringProperty()
    feed_percentage = StringProperty()
    avg_weight = StringProperty()
    current_count = StringProperty()
    larve_count = StringProperty()
    survival_rate = StringProperty()
    biomass = StringProperty()
    daily_feeding_rate = StringProperty()
    record_id = NumericProperty(-1)
    on_delete = ObjectProperty(None, allownone=True)
    
    # New Property: Is this a header row?
    is_header = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        # super().__init__(orientation='horizontal', padding=10, spacing=10, size_hint_y=None, height=40, **kwargs)
        super().__init__(
            orientation='horizontal', 
            padding=20, 
            spacing=5, 
            size_hint_y=None, 
            height=sp(50), # or 40
            size_hint_x=None,  # Tell Kivy not to squash the width
            width=TOTAL_WIDTH, # Make the row as wide as the header/layout
            **kwargs
        )
        
        # 🟢 VISUAL DEBUG: Add a background color to the row
        with self.canvas.before:
            self.bg_color = Color(0.15, 0.15, 0.15, 1)  # normal row color
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_bg, size=self._update_bg)
        
        
        # Create Labels with FIXED widths (size_hint_x=None)
        self.lbl_date = self._make_label(COL_WIDTHS['date'])
        self.lbl_feed = self._make_label(COL_WIDTHS['daily_feed'])
        self.lbl_weight = self._make_label(COL_WIDTHS['avg_weight'])
        self.lbl_percent = self._make_label(COL_WIDTHS['feed_percentage'])
        self.lbl_count = self._make_label(COL_WIDTHS['current_count'])
        self.lbl_larve = self._make_label(COL_WIDTHS['larve_count'])
        self.lbl_survival = self._make_label(COL_WIDTHS['survival_rate'])
        self.lbl_biomass = self._make_label(COL_WIDTHS['biomass'])
        self.lbl_rate = self._make_label(COL_WIDTHS['daily_feeding_rate'])
        self.delete_button = Button(
            text=persian_text("حذف"),
            font_name='vazir',
            font_size=sp(12),
            size_hint=(None, 1),
            padding=10,
            width=COL_WIDTHS['delete_button'],
            halign='center',
            valign='middle',
            background_normal='',
            background_color=(0.8, 0.2, 0.2, 1),
        )
        self.delete_button.bind(size=self.delete_button.setter('text_size')) # Ensure text wraps/aligns correctly
        self.delete_button.bind(on_release=self._on_delete_pressed)
        self.add_widget(self.delete_button)
        
        
        self._labels = [self.lbl_date, self.lbl_feed, self.lbl_percent, self.lbl_weight,
                        self.lbl_count, self.lbl_larve, self.lbl_survival,
                        self.lbl_biomass, self.lbl_rate]
        
        self.on_is_header(self, self.is_header)  # Initial call to set header color if needed

        
    def _make_label(self, w):
        # Helper to create consistent labels
        lbl = Label(text='-', font_name='vazir', font_size=sp(12), 
                    size_hint=(None, 1), width=w, halign='center', valign='middle')
        lbl.bind(size=lbl.setter('text_size')) # Ensure text wraps/aligns correctly
        self.add_widget(lbl)
        return lbl
            
    def _update_bg(self, instance, value):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        
    # When "is_header" changes, we update the color!
    def on_is_header(self, instance, value):
        # SAFETY CHECK: If bg_color doesn't exist yet, do nothing
        if not hasattr(self, 'bg_color'): return
            
        if value:
            self.bg_color.rgba = (0.3, 0.3, 0.5, 1) # Header color: Blue-ish
        else:
            self.bg_color.rgba = (0.15, 0.15, 0.15, 1) # Normal color: Dark Grey   
            
        for lbl in self._labels:
            lbl.color = (1, 1, 0, 1) if value else (0.9, 0.9, 0.9, 1)
            lbl.font_name = 'vazir_bold' if value else 'vazir'
            lbl.font_size = sp(14) if value else sp(12)
            
            
    def _on_delete_pressed(self, *args):
        if self.on_delete:
            self.on_delete(self.record_id)
         
            
    # Listeners to update text when data changes
    def on_date(self, instance, value): self.lbl_date.text = persian_text(value)
    def on_daily_feed(self, instance, value): self.lbl_feed.text = persian_text(value)
    def on_feed_percentage(self, instance, value): self.lbl_percent.text = persian_text(value)
    def on_avg_weight(self, instance, value): self.lbl_weight.text = persian_text(value)
    def on_current_count(self, instance, value): self.lbl_count.text = persian_text(value)
    def on_larve_count(self, instance, value): self.lbl_larve.text = persian_text(value)
    def on_survival_rate(self, instance, value): self.lbl_survival.text = persian_text(value)
    def on_biomass(self, instance, value): self.lbl_biomass.text = persian_text(value)
    def on_daily_feeding_rate(self, instance, value): self.lbl_rate.text = persian_text(value)
    def on_delete_button(self, instance, value): self.delete_button.text = value

class HistoryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=70, spacing=60)
        layout.add_widget(Label(text=persian_text("تاریخچه محاسبات"), halign='right', font_name='vazir_bold', font_size=sp(24), size_hint=(1, 0.1)))  
        
        BTON_Layout = BoxLayout(orientation='horizontal', padding=30, spacing=30, size_hint=(1, 0.10))
        home_button = IconButton(text="صفحه اصلی", size_hint=(0.5, 1))
        home_button.bind(on_press=lambda x: setattr(self.manager, 'current', 'general'))
        BTON_Layout.add_widget(home_button)
        
        
        # 3. THE HEADER ROW (Static, sits above the list)
        # We put it in a ScrollView matching the RV so if we scroll X, this should ideally move too, 
        # but for simplicity, we'll just fix it or make it part of the scroll view later. 
        # For now, let's just make a simple horizontal box for headers.
        headers = [
            ("تاریخ", COL_WIDTHS['date']),
            ("غذا روزانه", COL_WIDTHS['daily_feed']),
            ("درصد غذادهی", COL_WIDTHS['feed_percentage']),
            ("میانگین وزن", COL_WIDTHS['avg_weight']),
            ("تعداد", COL_WIDTHS['current_count']),
            ("تعداد لارو", COL_WIDTHS['larve_count']),
            ("نرخ بقا", COL_WIDTHS['survival_rate']),
            ("بیومس", COL_WIDTHS['biomass']),
            ("نرخ غذای روزانه", COL_WIDTHS['daily_feeding_rate']),
            ("حذف ❌", COL_WIDTHS['delete_button'])
        ]
        
        
        
        # 3. Create the RecycleView (Empty Frame)
        self.rv = RecycleView(size_hint=(1, 0.8))
        self.rv.do_scroll_x = True  # Enable Horizontal Scroll
        self.rv.do_scroll_y = True  # Enable Vertical Scroll 

        # 4. Create the Layout Manager (The Canvas)
        rv_layout = RecycleBoxLayout(
            default_size=(None, sp(50)), 
            default_size_hint=(None, None), # Allow rows to be their own size
            size_hint=(None, None),         # Allow layout to be huge
            width=TOTAL_WIDTH,              # Force it to be wide
            orientation='vertical'
        )
        
        rv_layout.bind(minimum_height=rv_layout.setter('height'))
        
        self.rv.layout_manager = rv_layout
        self.rv.add_widget(rv_layout)
        self.rv.viewclass = HistoryRow 
        
        # 8. Add the RV to the screen
        layout.add_widget(self.rv)
        
                
        layout.add_widget(BTON_Layout)      
        
        self.add_widget(layout)
        
    def load_records(self):
        app = App.get_running_app()
        records = fetch_records(app.db_path, limit=100)
        
        rv_data = []
        
        
        # 1. Define the Header Row
        header_row = {
            'is_header': True, # This triggers the Gold color
            'on_delete': None,
            'record_id': -1,
            'date': "تاریخ",
            'daily_feed': "غذا روزانه",
            'feed_percentage': "درصد غذادهی",
            'avg_weight': "میانگین وزن",
            'current_count': "تعداد",
            'larve_count': "تعداد لارو",
            'survival_rate': "نرخ بقا",
            'biomass': "بیومس",
            'daily_feeding_rate': "نرخ غذای روزانه",
            'delete_button': persian_text("حذف ❌"),
        }
        rv_data.append(header_row)

        # 2. Add Data Rows
        for record in records:
            # --- DATE FORMATTING ---
            raw_date = record.get("created_at")
            if raw_date and "T" in raw_date:
                try:
                    # Parse ISO format (2025-12-26T20:15:30)
                    dt = datetime.fromisoformat(raw_date)
                    # Format to: 2025/12/26 20:15 (No seconds)
                    final_date = dt.strftime("%Y/%m/%d %H:%M")
                except ValueError:
                    final_date = str(raw_date)
            else:
                final_date = str(raw_date or "نامشخص")

            rv_data.append({
                'is_header': False, # Normal row
                'record_id': record.get('id', None),
                'on_delete': self.request_delete,
                'date': final_date,
                'daily_feed': str(record.get('daily_feed') or 0),
                'avg_weight': str(record.get('avg_weight') or 0),
                'current_count': str(record.get('current_count') or 0),
                'larve_count': str(record.get('larve_count') or 0),
                'feed_percentage': str(record.get('feed_percentage') or 0),
                'survival_rate': f"{record.get('survival_rate') or 0:.1f}",
                'biomass': f"{record.get('biomass') or 0:.1f}",
                'daily_feeding_rate': f"{record.get('daily_feeding_rate') or 0:.2f}",
                'delete_button': persian_text("حذف ❌"),
            })
        
        self.rv.data = rv_data
        
        
    def request_delete(self, record_id):
        # ignore header/invalid
        if record_id is None or record_id < 0:
            return

        msg = persian_text("آیا از حذف این داده اطمینان دارید؟\nاین عملیات غیرقابل بازگشت است")

        content = BoxLayout(orientation="vertical", spacing=10, padding=15)

        lbl = Label(text=msg, halign="center", valign="middle")
        lbl.bind(size=lbl.setter("text_size"))
        content.add_widget(lbl)

        btns = BoxLayout(orientation="horizontal", size_hint_y=None, height=sp(50), spacing=10)

        popup = Popup(title=persian_text("تأیید حذف"), content=content,
                    size_hint=(0.65, 0.30), title_align='center', auto_dismiss=False)

        yes_btn = IconButton(text="بله")
        # yes_btn = Button(text=persian_text("بله"))
        no_btn  = IconButton(text="خیر")
        # no_btn  = Button(text=persian_text("خیر"))

        def yes(*_):
            popup.dismiss()
            self.confirm_delete(record_id)

        def no(*_):
            popup.dismiss()

        yes_btn.bind(on_release=yes)
        no_btn.bind(on_release=no)

        btns.add_widget(yes_btn)
        btns.add_widget(no_btn)
        content.add_widget(btns)

        popup.open()


    def confirm_delete(self, record_id):
        app = App.get_running_app()
        delete_record(app.db_path, record_id)
        self.load_records()

        
    def delete_row(self, record_id):
        app = App.get_running_app()
        delete_record(app.db_path, record_id)
        self.load_records()  # refresh RV
        
    def on_enter(self):
        self.load_records()  # Re-fetch and reload records into RV