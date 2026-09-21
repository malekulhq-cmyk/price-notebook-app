from kivy.app import App
import os
import json


def get_data_file():
    return os.path.join(
        App.get_running_app().user_data_dir,
        "items.json"
    )


def load_data():
    data_file = get_data_file()

    if not os.path.exists(data_file):
        return []

    with open(data_file, "r", encoding="utf-8") as file:
        return json.load(file)


def save_data(data):
    data_file = get_data_file()

    with open(data_file, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=4
        )


def add_item(name, price):
    data = load_data()

    for item in data:
        if item["name"].lower() == name.lower():
            item["price"] = price
            save_data(data)
            return

    data.append({
        "name": name,
        "price": price
    })

    save_data(data)


def delete_item(name):
    data = load_data()

    for item in data:
        if item["name"].lower() == name.lower():
            data.remove(item)
            save_data(data)
            return True

    return False


def update_price(name, price):
    data = load_data()

    for item in data:
        if item["name"].lower() == name.lower():
            item["price"] = price
            save_data(data)
            return True

    return False
