"""
Persian text helper for Kivy applications
Handles RTL text direction and character shaping
"""

try:
    import arabic_reshaper
    from bidi.algorithm import get_display
    PERSIAN_SUPPORT = True
except ImportError:
    PERSIAN_SUPPORT = False
    print("Warning: arabic_reshaper or python-bidi not installed")
    print("Install with: pip install arabic-reshaper python-bidi")

try:
    from kivy.app import App            ## Helper for 'go_to' function
    from kivy.uix.label import Label
    from kivy.uix.image import Image
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.behaviors import ButtonBehavior 
    from kivy.graphics import Color, Rectangle, Line
    from kivy.metrics import sp
    KIVY_MODULES_SUPPORT = True
except ImportError:
    KIVY_MODULES_SUPPORT = False
    print("Warning: kivy.uix.label or kivy.uix.image or kivy.uix.behaviors or kivy.graphics not installed")
    print("Install with: pip install [packages]")


def persian_text(text):
    """
    Convert Persian/Arabic text to display correctly in Kivy

    Args:
        text: String containing Persian/Arabic characters

    Returns:
        Properly shaped and ordered text for display
    """
    if not PERSIAN_SUPPORT:
        return text
    
    try:
        # Reshape the text (connect characters properly)
        reshaped_text = arabic_reshaper.reshape(text)
        
        # Apply bidirectional algorithm (handle RTL)
        bidi_text = get_display(reshaped_text)
        
        return bidi_text
    except Exception as e:
        print(f"Error processing Persian text: {e}")
        return text


class IconButton (ButtonBehavior, BoxLayout):
    def __init__(self, icon_source=None, text="No Text provided", font_size=sp(16), disabled=False, **kwargs):
        super().__init__(spacing=10, padding=30, orientation="vertical", **kwargs)
        # disabled=disabled
        # for background color:
        # Draw background
        # color = (0.2, 0.2, 0.8, 0.9) if not disabled else (0.2, 0.2, 0.8, 0.5)
        with self.canvas.before:
            Color(0.2, 0.2, 0.8, 0.9)  # RGBA: white
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        
        with self.canvas.after:
            Color(1, 1, 1, 1)  # RGBA: white
            self.bg_line = Line(rectangle=self.pos + self.size, width=2)
            
        def update_visuals(instance, value):
            self.bg_rect.pos = instance.pos
            self.bg_rect.size = instance.size
            self.bg_line.rectangle = instance.pos + instance.size
            
        self.bind(pos=update_visuals, size=update_visuals)
        
        if icon_source:
            self.add_widget(Image(source=icon_source, size_hint=(1, 0.6)))
        self.add_widget(Label(text=persian_text(text), font_size=font_size, size_hint=(1, 0.4)))
        
def go_to(sm, target_name):
    app = App.get_running_app()
    app.last_screen = sm.current
    sm.current = target_name


# Quick test
if __name__ == "__main__":
    test_texts = [
        "مدیریت پرورش میگو",
        "وگی‌م شروپ تکای‌یدم",
        "Person Name:",
        "درصد بازماندگی/ ضریب تبدیل"
    ]
    
    print("Testing Persian text conversion:")
    for text in test_texts:
        print(f"Original: {text}")
        print(f"Converted: {persian_text(text)}")
        print("-" * 50)