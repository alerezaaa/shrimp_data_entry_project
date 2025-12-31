from kivy.config import Config  # Font
Config.set('kivy', 'default_font', ['vazir', 'Vazir-Medium.ttf', 'Vazir-Medium.ttf'])

from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.metrics import sp
from kivy.core.clipboard import Clipboard

import webbrowser

from persian_helper import persian_text, IconButton


class ContactUsScreen(Screen):
    WEBSITE_URL = "https://alirezad.ir"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        root = BoxLayout(orientation="vertical", padding=90, spacing=20)

        title = Label(
            text=persian_text("تماس با ما"),
            font_name="vazir_bold",
            font_size=sp(24),
            halign="right",
            size_hint=(1, 0.12),
        )
        root.add_widget(title)

        contact_text = (
            "برای ارتباط، پیشنهاد، یا گزارش خطا می‌توانید از راه‌های زیر استفاده کنید:\n\n"
            f"• نام: علیرضا دهقانزاده\n"
            f"• سمت: Junior Developer\n"
            f"• وب‌سایت: {self.WEBSITE_URL}\n\n"
            "پیشنهاد: برای پیام دادن، بهتر است از فرم تماس داخل وب‌سایت استفاده کنید."
        )

        scroll = ScrollView(size_hint=(1, 0.60))
        lbl = Label(
            text=persian_text(contact_text),
            font_name="vazir",
            font_size=sp(16),
            halign="right",
            valign="top",
            size_hint_y=None,
        )
        lbl.bind(
            width=lambda inst, w: setattr(inst, "text_size", (w, None)),
            texture_size=lambda inst, ts: setattr(inst, "height", ts[1]),
        )
        scroll.add_widget(lbl)
        root.add_widget(scroll)

        self.status_label = Label(
            text="",
            font_name="vazir",
            font_size=sp(14),
            halign="center",
            size_hint=(1, 0.08),
        )
        root.add_widget(self.status_label)

        btns = BoxLayout(size_hint=(1, 0.20), spacing=20, padding=(0, 10))

        back_btn = IconButton(text="بازگشت")
        back_btn.bind(on_press=self.go_back)

        copy_btn = IconButton(text="کپی لینک")
        copy_btn.bind(on_press=self.copy_link)

        website_btn = IconButton(text="باز کردن وب‌سایت")
        website_btn.bind(on_press=self.open_website)

        btns.add_widget(back_btn)
        btns.add_widget(copy_btn)
        btns.add_widget(website_btn)

        root.add_widget(btns)
        self.add_widget(root)

    def go_back(self, *_):
        app = App.get_running_app()
        target = getattr(app, "last_screen", "") or "general"
        self.manager.current = target

    def copy_link(self, *_):
        Clipboard.copy(self.WEBSITE_URL)
        self.status_label.text = persian_text("لینک کپی شد ✅")

    def open_website(self, *_):
        webbrowser.open(self.WEBSITE_URL)
