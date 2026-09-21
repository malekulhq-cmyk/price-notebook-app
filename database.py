import json
import os


DATA_FILE = "items.json"


def load_data():
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
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
