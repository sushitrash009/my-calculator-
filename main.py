from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label


class Calculator(App):
    def build(self):
        Window.clearcolor = (0.055, 0.055, 0.07, 1)

        root = BoxLayout(
            orientation="vertical",
            padding=dp(12),
            spacing=dp(10),
        )

        self.display = Label(
            text="0",
            font_size=dp(42),
            halign="right",
            valign="middle",
            color=(1, 1, 1, 1),
            size_hint_y=0.24,
        )
        self.display.bind(
            size=lambda *_: setattr(self.display, "text_size", self.display.size)
        )
        root.add_widget(self.display)

        rows = [
            ["AC", "⌫", "%", "÷"],
            ["7", "8", "9", "×"],
            ["4", "5", "6", "−"],
            ["1", "2", "3", "+"],
            ["±", "0", ".", "="],
        ]

        grid = GridLayout(
            cols=4,
            spacing=dp(8),
            size_hint_y=0.76,
        )

        for row in rows:
            for value in row:
                button = Button(
                    text=value,
                    font_size=dp(25),
                    background_normal="",
                    background_color=(0.16, 0.16, 0.20, 1),
                    color=(1, 1, 1, 1),
                )

                if value in {"÷", "×", "−", "+", "="}:
                    button.background_color = (0.18, 0.42, 0.75, 1)
                elif value in {"AC", "⌫", "%", "±"}:
                    button.background_color = (0.25, 0.25, 0.30, 1)

                button.bind(on_press=self.press)
                grid.add_widget(button)

        root.add_widget(grid)

        self.expression = ""
        self.just_calculated = False
        return root

    def press(self, button):
        value = button.text

        if value == "AC":
            self.expression = ""
            self.display.text = "0"
            self.just_calculated = False
            return

        if value == "⌫":
            self.expression = self.expression[:-1]
            self.display.text = self.expression or "0"
            return

        if value == "=":
            self.calculate()
            return

        if value == "±":
            if self.expression and self.expression[-1].isdigit():
                i = len(self.expression) - 1
                while i >= 0 and (
                    self.expression[i].isdigit() or self.expression[i] == "."
                ):
                    i -= 1

                start = i + 1
                number = self.expression[start:]

                if number.startswith("-"):
                    replacement = number[1:]
                else:
                    replacement = "-" + number

                self.expression = self.expression[:start] + replacement
                self.display.text = self.expression
            return

        if value == "%":
            if self.expression and self.expression[-1].isdigit():
                i = len(self.expression) - 1
                while i >= 0 and (
                    self.expression[i].isdigit() or self.expression[i] == "."
                ):
                    i -= 1

                start = i + 1
                try:
                    number = float(self.expression[start:]) / 100
                    replacement = str(number).rstrip("0").rstrip(".")
                    self.expression = self.expression[:start] + replacement
                    self.display.text = self.expression
                except ValueError:
                    self.show_error()
            return

        if self.just_calculated and (value.isdigit() or value == "."):
            self.expression = ""
            self.just_calculated = False

        if value in {"÷", "×", "−", "+"}:
            op = {"÷": "/", "×": "*", "−": "-", "+": "+"}[value]

            if not self.expression:
                if op == "-":
                    self.expression = "-"
                else:
                    return
            elif self.expression[-1] in "+-*/":
                self.expression = self.expression[:-1] + op
            else:
                self.expression += op

        elif value == ".":
            current = self.expression
            for operator in "+-*/":
                current = current.split(operator)[-1]

            if "." not in current:
                self.expression += "."

        else:
            self.expression += value

        self.display.text = self.expression or "0"
        self.just_calculated = False

    def calculate(self):
        if not self.expression:
            return

        try:
            if self.expression[-1] in "+-*/.":
                self.expression = self.expression[:-1]

            if not self.expression:
                self.display.text = "0"
                return

            result = eval(self.expression, {"__builtins__": {}}, {})

            if (
                not isinstance(result, (int, float))
                or result != result
                or abs(result) == float("inf")
            ):
                raise ValueError

            if isinstance(result, float) and result.is_integer():
                result = int(result)

            self.expression = str(result)
            self.display.text = self.expression
            self.just_calculated = True

        except (ArithmeticError, ValueError, SyntaxError, TypeError):
            self.show_error()

    def show_error(self):
        self.expression = ""
        self.display.text = "Error"
        self.just_calculated = True


if __name__ == "__main__":
    Calculator().run()
