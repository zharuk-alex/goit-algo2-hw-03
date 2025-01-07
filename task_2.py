import pandas as pd
import timeit
from BTrees.OOBTree import OOBTree


def load_data(file_path):
    df = pd.read_csv(file_path)
    data = df.to_dict(orient="records")
    return data


def add_item_to_tree(tree, item):
    tree[item["ID"]] = item


def add_item_to_dict(dictionary, item):
    dictionary[item["ID"]] = item


def range_query_tree(tree, min_price, max_price):
    return [item for _, item in tree.items() if min_price <= item["Price"] <= max_price]


def range_query_dict(dictionary, min_price, max_price):
    return [
        item for item in dictionary.values() if min_price <= item["Price"] <= max_price
    ]


if __name__ == "__main__":

    data = load_data("generated_items_data.csv")

    tree = OOBTree()
    dictionary = {}

    for item in data:
        add_item_to_tree(tree, item)
        add_item_to_dict(dictionary, item)

    min_price = 100.0
    max_price = 200.0

    tree_time = timeit.timeit(
        lambda: range_query_tree(tree, min_price, max_price), number=100
    )

    dict_time = timeit.timeit(
        lambda: range_query_dict(dictionary, min_price, max_price), number=100
    )

    print(f"Total range_query time for OOBTree: {tree_time:.6f} seconds")
    print(f"Total range_query time for Dict: {dict_time:.6f} seconds")
