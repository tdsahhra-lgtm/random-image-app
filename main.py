
import os
import random

import arabic_reshaper
from bidi.algorithm import get_display

from kivy.app import App
from kivy.core.text import LabelBase
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image


#IMAGE_FOLDER = r"C:\Images"

import os

IMAGE_FOLDER = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "images"
)



FONT_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "tahoma.ttf"
)
MAX_IMAGES = 7


LabelBase.register(
    name="Tahoma",
    fn_regular=FONT_FILE
)


def persian_text(text):
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)


class RandomImageApp(App):

    def build(self):

        self.used_images = []

        main_layout = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=10
        )

        # دکمه‌ها
        button_layout = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=50,
            spacing=10
        )

        self.random_button = Button(
            text=persian_text("تصویر تصادفی"),
            font_name="Tahoma",
            font_size=18
        )

        self.random_button.bind(
            on_press=self.show_random_image
        )

        self.clear_button = Button(
            text=persian_text("پاک کردن"),
            font_name="Tahoma",
            font_size=18
        )

        self.clear_button.bind(
            on_press=self.clear_images
        )

        button_layout.add_widget(self.random_button)
        button_layout.add_widget(self.clear_button)

        main_layout.add_widget(button_layout)

        # محل تصاویر
        self.image_layout = BoxLayout(
            orientation="horizontal",
            spacing=5
        )

        main_layout.add_widget(self.image_layout)

        # ایمیل انگلیسی
        email = Button(
            text="Email: your@email.com",
            font_name="Tahoma",
            font_size=14,
            size_hint_y=None,
            height=40,
            background_normal="",
            background_color=(0, 0, 0, 0)
        )

        main_layout.add_widget(email)

        return main_layout

    def show_random_image(self, instance):

        if len(self.used_images) >= MAX_IMAGES:
            self.random_button.disabled = True
            return

        try:
            files = [
                f for f in os.listdir(IMAGE_FOLDER)
                if f.lower().endswith(
                    (".jpg", ".jpeg", ".png")
                )
            ]
        except Exception:
            return

        available = [
            f for f in files
            if f not in self.used_images
        ]

        if not available:
            self.random_button.disabled = True
            return

        selected = random.choice(available)

        self.used_images.append(selected)

        image_path = os.path.join(
            IMAGE_FOLDER,
            selected
        )

        img = Image(
    source=image_path,
    size_hint_x=1 / MAX_IMAGES,
    size_hint_y=None,
    height=120,
    allow_stretch=True,
    keep_ratio=True
)

        self.image_layout.add_widget(img)

        if len(self.used_images) >= MAX_IMAGES:
            self.random_button.disabled = True

    def clear_images(self, instance):

        self.image_layout.clear_widgets()

        self.used_images = []

        self.random_button.disabled = False


if __name__ == "__main__":
    RandomImageApp().run()
