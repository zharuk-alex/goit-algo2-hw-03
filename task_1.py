import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from edmonds_karp import edmonds_karp


def graph_visualisation(edges, pos, labels):
    G = nx.DiGraph()
    G.add_weighted_edges_from(edges)

    plt.figure(figsize=(12, 8))
    nx.draw(
        G,
        pos,
        with_labels=True,
        labels=labels,
        node_size=1200,
        node_color="skyblue",
        font_size=10,
    )
    labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.show()


if __name__ == "__main__":
    graph_data = {
        "nodes": {
            0: {
                "pos": (0, 4),
                "label": "Термінал 1",
                "type": "terminal",
                "range": (6, 14),
            },
            1: {
                "pos": (0, 2),
                "label": "Термінал 2",
                "type": "terminal",
                "range": (9, 19),
            },
            2: {"pos": (2, 5), "label": "Склад 1", "type": "storage"},
            3: {"pos": (2, 3), "label": "Склад 2", "type": "storage"},
            4: {"pos": (2, 1), "label": "Склад 3", "type": "storage"},
            5: {"pos": (2, -1), "label": "Склад 4", "type": "storage"},
            6: {"pos": (4, 6), "label": "Магазин 1", "type": "store"},
            7: {"pos": (4, 5), "label": "Магазин 2", "type": "store"},
            8: {"pos": (4, 4), "label": "Магазин 3", "type": "store"},
            9: {"pos": (4, 3), "label": "Магазин 4", "type": "store"},
            10: {"pos": (4, 2), "label": "Магазин 5", "type": "store"},
            11: {"pos": (4, 1), "label": "Магазин 6", "type": "store"},
            12: {"pos": (4, 0), "label": "Магазин 7", "type": "store"},
            13: {"pos": (4, -1), "label": "Магазин 8", "type": "store"},
            14: {"pos": (4, -2), "label": "Магазин 9", "type": "store"},
            15: {"pos": (4, -3), "label": "Магазин 10", "type": "store"},
            16: {"pos": (4, -4), "label": "Магазин 11", "type": "store"},
            17: {"pos": (4, -5), "label": "Магазин 12", "type": "store"},
            18: {"pos": (4, -6), "label": "Магазин 13", "type": "store"},
            19: {"pos": (4, -7), "label": "Магазин 14", "type": "store"},
        },
        "edges": [
            (0, 2, 25),  # Термінал 1 -> Склад 1
            (0, 3, 20),  # Термінал 1 -> Склад 2
            (0, 4, 15),  # Термінал 1 -> Склад 3
            (1, 3, 10),  # Термінал 2 -> Склад 2
            (1, 4, 15),  # Термінал 2 -> Склад 3
            (1, 5, 30),  # Термінал 2 -> Склад 4
            (2, 6, 15),  # Склад 1 -> Магазин 1
            (2, 7, 10),  # Склад 1 -> Магазин 2
            (2, 8, 20),  # Склад 1 -> Магазин 3
            (3, 9, 15),  # Склад 2 -> Магазин 4
            (3, 10, 10),  # Склад 2 -> Магазин 5
            (3, 11, 25),  # Склад 2 -> Магазин 6
            (4, 12, 20),  # Склад 3 -> Магазин 7
            (4, 13, 15),  # Склад 3 -> Магазин 8
            (4, 14, 10),  # Склад 3 -> Магазин 9
            (5, 15, 20),  # Склад 4 -> Магазин 10
            (5, 16, 10),  # Склад 4 -> Магазин 11
            (5, 17, 15),  # Склад 4 -> Магазин 12
            (5, 18, 5),  # Склад 4 -> Магазин 13
            (5, 19, 10),  # Склад 4 -> Магазин 14
        ],
    }

    edges = graph_data["edges"]
    num_nodes = len(graph_data["nodes"])
    capacity_matrix = [[0] * num_nodes for _ in range(num_nodes)]
    pos = {}
    labels = {}
    terminals = []
    storages = []
    stores = []

    for node, data in graph_data["nodes"].items():
        pos[node] = data["pos"]
        labels[node] = data["label"]
        if data["type"] == "terminal":
            terminals.append(node)
        elif data["type"] == "storage":
            storages.append(node)
        elif data["type"] == "store":
            stores.append(node)

    G = nx.DiGraph()

    for edge in graph_data["edges"]:
        source, target, capacity = edge
        capacity_matrix[source][target] = capacity
        G.add_edge(source, target, capacity=capacity)

    rows = []
    for terminal in terminals:
        terminal_label = graph_data["nodes"][terminal]["label"]
        start, end = graph_data["nodes"][terminal].get("range", (None, None))
        if start is not None and end is not None:
            for store in range(start, end + 1):
                store_label = graph_data["nodes"][store]["label"]
                flow = edmonds_karp(capacity_matrix, terminal, store)
                # flow_, _ = nx.maximum_flow(
                #     G, terminal, store, flow_func=nx.algorithms.flow.edmonds_karp
                # )

                rows.append(
                    {
                        "Термінал": terminal_label,
                        "Магазин": store_label,
                        "Фактичний потік": flow,
                        # "Фактичний потік": flow_,
                    }
                )

    df = pd.DataFrame(rows)
    print("\n")
    print(df)
    graph_visualisation(edges, pos, labels)

    terminal_totals = df.groupby("Термінал")["Фактичний потік"].sum()
    print("\n Загальний потік")
    print(terminal_totals)

    min_flow_routes = df[df["Фактичний потік"] == df["Фактичний потік"].min()]
    print("\n Мінімальний потік")
    print(min_flow_routes)
