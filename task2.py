import csv
import timeit
from typing import Dict
from BTrees.OOBTree import OOBTree
from random import randint


def load_items_from_csv(file_path):
    items = []
    with open(file_path, "r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            item = {
                "ID": int(row["ID"]),
                "Name": row["Name"],
                "Category": row["Category"],
                "Price": float(row["Price"]),
            }
            items.append(item)
    return items


def add_item_to_tree(tree: OOBTree, item: Dict[str, str]):
    price = item["Price"]
    if price in tree:
        tree[price].append(item)
    else:
        tree[price] = [item]


def add_item_to_dict(dictionary: Dict[int, Dict[str, str]], item: Dict[str, str]):
    dictionary[item["ID"]] = item


def range_query_tree(tree: OOBTree, start_price: int, end_price: int):
    results = []
    for _, item in tree.items(start_price, end_price):
        results.extend(item)
    return results


def range_query_dict(
    dictionary: Dict[int, Dict[str, str]], start_price: int, end_price: int
):
    return [
        item
        for item in dictionary.values()
        if start_price <= item["Price"] <= end_price
    ]


def measure_time(func, *args):
    return timeit.timeit(lambda: func(*args), number=100)


def main():
    # Завантаження даних з CSV файлу
    items = load_items_from_csv("generated_items_data.csv")

    # Створення OOBTree
    tree = OOBTree()
    # Створення словника
    dictionary = {}

    for item in items:
        add_item_to_tree(tree, item)
        add_item_to_dict(dictionary, item)

    start_price = randint(0, 200)
    end_price = start_price + randint(1, 100)

    time_tree = measure_time(range_query_tree, tree, start_price, end_price)
    time_dict = measure_time(range_query_dict, dictionary, start_price, end_price)

    print(f"Range query from {start_price} to {end_price}:")
    print(f"Total range_query time for OOBTree: {time_tree:.6f} seconds")
    print(f"Total range_query time for Dict: {time_dict:.6f} seconds")


if __name__ == "__main__":
    main()
