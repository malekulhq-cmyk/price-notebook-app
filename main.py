__version__ = "1.0.0"

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

import database


class PriceNotebook(App):

    def build(self):
        root = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=10
        )

        self.output = Label(
            text=(
                "PRICE NOTEBOOK\n\n"
                "Command:\n"
                "Rice 650\n"
                "ls\n"
                "find Rice\n"
                "edit Rice 700\n"
                "del Rice\n"
                "clear"
            ),
            size_hint_y=None,
            halign="left",
            valign="top"
        )

        self.output.bind(
            texture_size=self.output.setter("size")
        )

        scroll = ScrollView()
        scroll.add_widget(self.output)
        root.add_widget(scroll)

        bottom = BoxLayout(
            size_hint_y=None,
            height=55,
            spacing=5
        )

        self.command = TextInput(
            hint_text="Enter command...",
            multiline=False
        )

        run_button = Button(
            text="RUN",
            size_hint_x=None,
            width=90
        )

        run_button.bind(
            on_press=self.run_command
        )

        bottom.add_widget(self.command)
        bottom.add_widget(run_button)

        root.add_widget(bottom)

        return root

    def run_command(self, instance):
        command = self.command.text.strip()

        if not command:
            return

        try:
            result = self.process_command(command)
        except Exception as e:
            result = f"Error: {e}"

        if command == "clear":
            self.output.text = ""
        else:
            self.output.text += f"\n\n> {command}\n{result}"

        self.command.text = ""

    def process_command(self, command):

        if command == "ls":
            data = database.load_data()

            if not data:
                return "No items found."

            lines = []

            for item in data:
                lines.append(
                    f"{item['name']} = ₹{item['price']}"
                )

            return "\n".join(lines)

        if command.startswith("find "):
            name = command[5:].strip()
            data = database.load_data()

            for item in data:
                if item["name"].lower() == name.lower():
                    return f"{item['name']} = ₹{item['price']}"

            return "Item not found."

        if command.startswith("del "):
            name = command[4:].strip()

            if database.delete_item(name):
                return "Deleted successfully."

            return "Item not found."

        if command.startswith("edit "):
            parts = command.split()

            if len(parts) < 3:
                return "Example: edit Rice 700"

            name = " ".join(parts[1:-1])

            try:
                price = float(parts[-1])
            except ValueError:
                return "Price must be a number."

            if database.update_price(name, price):
                return "Price updated successfully."

            return "Item not found."

        parts = command.rsplit(" ", 1)

        if len(parts) == 2:
            name = parts[0].strip()

            try:
                price = float(parts[1])
            except ValueError:
                return "Price must be a number."

            database.add_item(name, price)

            return f"{name} added at ₹{price}"

        return "Unknown command."


if __name__ == "__main__":
    PriceNotebook().run()
