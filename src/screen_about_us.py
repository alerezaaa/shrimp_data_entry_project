from kivy.config import Config  # Font
Config.set('kivy', 'default_font', ['vazir', 'Vazir-Medium.ttf', 'Vazir-Medium.ttf'])

from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.metrics import sp

import webbrowser

from persian_helper import persian_text, IconButton


class AboutUsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        root = BoxLayout(orientation="vertical", padding=40, spacing=40)

        title = Label(
            text=persian_text("درباره ما"),
            font_name="vazir_bold",
            font_size=sp(24),
            halign="right",
            size_hint=(1, 0.12),
        )
        root.add_widget(title)

        about_text = (
            "این اپلیکیشن یک ابزار ساده برای ثبت و محاسبهٔ شاخص‌های مهم در پرورش میگو است.\n\n"
            "امکانات اصلی:\n"
            "• ثبت اطلاعات خوراک و وزن و تعداد\n"
            "• محاسبهٔ نرخ بقا، بیوماس و نرخ تغذیهٔ روزانه\n"
            "• ذخیره‌سازی نتایج در پایگاه داده (SQLite)\n"
            "• مشاهدهٔ تاریخچه و امکان حذف رکوردها\n\n"
            "هدف این برنامه کمک به تصمیم‌گیری سریع‌تر و کاهش خطای انسانی در محاسبات روزمره است.\n\n"
            "توسعه‌دهنده: علیرضا دهقانزاده\n"
            "وب‌سایت: https://alirezad.ir\n"
            "سمت: Junior Developer\n\n"
            "نکته: این برنامه یک ابزار کمکی است و جایگزین نظر متخصص/کارشناس نیست."
        )

        scroll = ScrollView(size_hint=(1, 0.73))
        lbl = Label(
            text=persian_text(about_text),
            font_name="vazir",
            font_size=sp(16),
            halign="right",
            valign="top",
            size_hint_y=None,
        )
        # Wrap & auto-height
        lbl.bind(
            width=lambda inst, w: setattr(inst, "text_size", (w, None)),
            texture_size=lambda inst, ts: setattr(inst, "height", ts[1]),
        )
        scroll.add_widget(lbl)
        root.add_widget(scroll)

        btns = BoxLayout(size_hint=(1, 0.15), spacing=20, padding=(0, 10))

        back_btn = IconButton(text="بازگشت")
        back_btn.bind(on_press=self.go_back)

        website_btn = IconButton(text="باز کردن وب‌سایت")
        website_btn.bind(on_press=self.open_website)

        btns.add_widget(back_btn)
        btns.add_widget(website_btn)

        root.add_widget(btns)
        self.add_widget(root)

    def go_back(self, *_):
        app = App.get_running_app()
        target = getattr(app, "last_screen", "") or "general"
        self.manager.current = target

    def open_website(self, *_):
        webbrowser.open("https://alirezad.ir")
