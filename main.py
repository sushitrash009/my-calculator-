from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


class Calculator(App):

    def build(self):
        main = BoxLayout(orientation="vertical", padding=10, spacing=10)

        self.display = Label(
            text="0",
            font_size=45,
            size_hint_y=0.25
        )
        main.add_widget(self.display)

        buttons = [
            "7", "8", "9", "/",
            "4", "5", "6", "*",
            "1", "2", "3", "-",
            "0", "C", "=", "+"
        ]

        grid = GridLayout(cols=4, spacing=8)

        for text in buttons:
            button = Button(
                text=text,
                font_size=28
            )
            button.bind(on_press=self.press)
            grid.add_widget(button)

        main.add_widget(grid)

        return main

    def press(self, button):
        value = button.text

        if value == "C":
            self.display.text = "0"

        elif value == "=":
            try:
                self.display.text = str(eval(self.display.text))
            except:
                self.display.text = "Error"

        else:
            if self.display.text == "0":
                self.display.text = value
            else:
                self.display.text += value


Calculator().run()
