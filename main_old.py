import os

from kivy import platform
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import StringProperty, ColorProperty
from kivy.uix.behaviors import ButtonBehavior
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.toast import toast
from kivymd.uix.behaviors import CircularRippleBehavior
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.utils.set_bars_colors import set_bars_colors

if platform == "win":
    Window.top = 30
    Window.left = 1050
    Window.size = 320, 650
    Window.always_on_top = True


Builder.load_string("""

<CustomIconButton@ButtonBehavior+MDIcon>:
    color: .2, .2, .2, 1
    padding: dp(7), dp(7)

    canvas.before:
        PushMatrix
        Rotate:
            angle: self.angle
            origin: self.center
    canvas.after:
        PopMatrix
        
        
<AddMoreImageWidget>:
    size_hint: None, None
    size: [dp(50)]*2
    FitImage:
        source: root.source
        radius: dp(50/2)
        nocache: True
        
    CustomIconButton:
    # MDIconButton:
        icon: 'close'
        color: 1, 1, 1, 1
        font_size: sp(16)
        padding: dp(4), dp(4)
        x: root.width - self.width / 2 - dp(4)
        y: root.height - self.height / 2 - dp(4)
        on_release: root.dispatch("on_close")
        canvas.before:
            Color:
                rgba: root.bg_color
            Ellipse:
                pos: self.pos
                size: self.size
            Color:
                rgba: app.theme_cls.error_color
            Ellipse:
                pos: self.x + dp(5 / 2), self.y + dp(5 / 2)
                size: self.width - dp(5), self.height - dp(5)
""")


class AddMoreImageWidget(CircularRippleBehavior, ButtonBehavior, MDRelativeLayout):
    source = StringProperty()
    bg_color = ColorProperty()

    def __init__(self, **kwargs):
        self.register_event_type("on_close")
        super(AddMoreImageWidget, self).__init__(**kwargs)

    def on_close(self):
        pass


kv = """
MDScreen:
    MDBoxLayout:
        orientation: "vertical"
        adaptive_height: True
        spacing: dp(16)
        pos_hint: {"center_y": .5}
        
        MDBoxLayout:
            adaptive_size: True
            pos_hint: {"center_x": .5}
            spacing: dp(20)
            
            MDRaisedButton:
                text: "Open WebView 1"
                on_release: app.open_webview1()
            
            MDRaisedButton:
                text: "Open WebView 2"
                on_release: app.open_webview2()
                
        MDLabel:
            text: "Select file path(s)"
            adaptive_height: True
            halign: "center"
                
        MDLabel:
            id: file_path_lbl
            text: "None"
            adaptive_height: True
            halign: "center"
                
        MDLabel:
            text: "Is readable?"
            adaptive_height: True
            halign: "center"
                
        MDLabel:
            id: is_readable_path_lbl
            text: "None"
            adaptive_height: True
            halign: "center"
            
        MDRaisedButton:
            text: "Request Read Permission"
            on_release: app.request_permission()
            pos_hint: {"center_x": .5}
            
        AddMoreImageWidget:
        # Image:
            source: app.img
            size_hint: None, None
            size: 50, 50
            canvas.before:
                Color:
                    rgba: 0, 0, 1, 1
                Rectangle:
                    # pos: self.pos
                    size: self.size
            
        Image:
            source: app.img
            size_hint: None, None
            size: 100, 100
            
            canvas.before:
                Color:
                    rgba: 1, 0, 0, 1
                Rectangle:
                    pos: self.pos
                    size: self.size
            
        MDRaisedButton:
            text: "Open File Picker ALT"
            on_release: app.open_file_chooser_in_add_more(False)


        MDBoxLayout:
            adaptive_height: True
            padding: dp(12), dp(15), 0, 0

            ScrollView:
                id: img_box
                effect_cls: "ScrollEffect"
                size_hint: None, None
                size: max(dp(60), min(att_box.width, self.parent.width - dp(20))), dp(70)
                bar_width: dp(1.2)

                canvas.after:
                    Color:
                        rgba: 0, 0, 0, .07
                    RoundedRectangle:
                        pos: self.x, self.y
                        size: self.width, self.height
                        radius: [dp(12)]

                MDBoxLayout:
                    id: att_box
                    adaptive_width: True
                    padding: dp(10)
                    spacing: dp(20)

                    MDIconButton:
                        icon: "plus"
                        size_hint: None, None
                        padding: dp(10), dp(10)
                        pos_hint: {'center_y': .5}
                        on_release: app.open_file_chooser_in_add_more(True)

                        canvas.before:
                            Color:
                                rgba: 0, 0, 0, .05
                            Ellipse:
                                pos: self.pos
                                size: self.size

"""


class DemoApp(MDApp):
    primary_color = ColorProperty([0 / 255, 153 / 255, 76 / 255, 1])
    img = "/storage/emulated/0/azag.jpg"
    # img = r"C:\Users\agboo\StudioProjects\work4me\assets\images\group.png"

    def build(self):
        return Builder.load_string(kv)

    def on_start(self):
        set_bars_colors(self.primary_color, None, "Light")

    def open_webview1(self):
        from utils.webview import WebView
        url = "https://www.google.com"
        webview = WebView(url, self.callback)
        webview.open()

    def open_webview2(self):
        from utils.webview import WebView
        url = "https://www.google.com"
        WebView(
            url,
            self.callback,
            True,
            True,
            True,
        )

    @staticmethod
    def callback():
        print("AZAG CAME BACK SUCCESSFULLY")

    def on_selection(self, paths):
        if paths:
            self.root.ids.file_path_lbl.text = "\n".join(paths)

            readable = []

            for file in paths:
                with open(file) as fd:
                    readable.append(str(fd.readable()))

            self.root.ids.is_readable_path_lbl.text = "\n".join(readable)

    def open_file_chooser_in_add_more(self, is_on_droid):
        def on_selection(paths):
            if paths:
                att_box = self.root.ids.att_box
                n = image_max_len - len(att_box.children) + 1
                for img in paths[:n]:
                    img_widget = AddMoreImageWidget(source=img, bg_color="EDEDED")
                    img_widget.bind(on_close=self.remove_image_in_add_more)
                    img_widget.bind(on_release=self.show_image_in_add_more)
                    att_box.add_widget(img_widget, len(att_box.children))
                    # self.app.add_more_images.append(img)

            from kivy import platform

            if platform == 'win':
                import os
                os.chdir(self.directory)

        image_max_len = 3
        if len(self.root.ids.att_box.children) > image_max_len:
            toast(f"Only {image_max_len} images allowed")
            return

        if is_on_droid:
            from utils.file_chooser import open_file_chooser

            open_file_chooser(
                multiple=True,
                # filters=['*jpg', '*png', '*jpeg'],
                filters="image",
                on_selection=lambda x: Clock.schedule_once(lambda _: on_selection(x))
            )
        else:
            from plyer import filechooser

            filechooser.open_file(
                multiple=True,
                filters=['*jpg', '*png', '*jpeg'],
                on_selection=lambda x: Clock.schedule_once(lambda _: on_selection(x)),
            )

    def remove_image_in_add_more(self, btn):
        self.root.ids.att_box.remove_widget(btn)
        # self.app.add_more_images.remove(btn.source)

    def show_image_in_add_more(self, btn):
        pass

    @staticmethod
    def request_permission():
        from utils.notification import azag
        azag()
        # create_notification()


if __name__ == "__main__":
    DemoApp().run()
