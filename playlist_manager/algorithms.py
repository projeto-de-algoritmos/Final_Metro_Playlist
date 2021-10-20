import math
from heapq import heapify, heappush

import networkx as nx
import matplotlib.pyplot as plt


def dijkstra(graph, source, destination):
    inf = math.inf
    node_data = {
        node: {
            "cost": inf, "pred": []
        }
        for node in graph
    }

    node_data[source]["cost"] = 0

    visited = []
    temp_source = source

    for _ in range(len(graph) - 1):
        if temp_source not in visited:
            visited.append(temp_source)
            min_heap = []

            for neighbour in graph[temp_source]:

                if neighbour not in visited:
                    cost = node_data[temp_source]["cost"] + graph[temp_source][neighbour]

                    if cost < node_data[neighbour]["cost"]:
                        node_data[neighbour]["cost"] = cost
                        node_data[neighbour]["pred"] = node_data[temp_source]["pred"] + [temp_source]

                    heappush(
                        min_heap,
                        (node_data[neighbour]["cost"], neighbour)
                    )

        heapify(min_heap)
        _, temp_source = min_heap[0] # Tuple containing cost and node (cost, node)

    print(f"Shortest distance: {node_data[destination]['cost']}")
    print(f"Shortest path: {node_data[destination]['pred'] + [destination]}")
    shortest_distance = node_data[destination]['cost']
    shortest_path = node_data[destination]['pred'] + [destination]
    return shortest_distance, shortest_path


def knapsack(capacity, weights, values): 
    w, h = capacity + 1, len(values)
    table = [
        [0 for _ in range(w)] for _ in range(h)
    ]

    for index in range(len(values)):
        for weight in range(w):
            # If the item weights more than the capacity at that column?
            # Take above value, that problem was solved
            if weights[index] > weight:
                table[index][weight] = table[index - 1][weight]
                continue
            
            # if the value of the item < capacity
            prior_value = table[index - 1][weight]
            #         val of current item  + val of remaining weight
            new_option_best = values[index] + table[index - 1][weight - weights[index]]
            table[index][weight] = max(prior_value, new_option_best)

    return table

def print_selected_items(dp, weights, capacity):
    idxes_list = []
    print("Selected weights are: ", end='')
    n = len(weights)
    i = n - 1
    while i >= 0 and capacity >= 0:
        if i > 0 and dp[i][capacity] != dp[i - 1][capacity]:
            # include this item
            idxes_list.append(i)
            capacity -= weights[i]
        elif i == 0 and capacity >= weights[i]:
            # include this item
            idxes_list.append(i)
            capacity -= weights[i]
        else:
            i -= 1
    weights = [weights[idx] for idx in idxes_list]
    print(weights)
    return weights

def chunks(l, n):
    n = max(1, n)
    return list((set(l[i:i+n]) for i in range(0, len(l), n)))

if __name__ == "__main__":
    graph = {
        'Manhattan': {
            'Washington': 2292.089,
            'Roosevelt is': 1603.554,
            'Grand': 1310.103,
            'Cropsey': 1870.891
        },
        'Washington': {
            'Manhattan': 1888.44,
            'Roosevelt is': 1300.956,
            'Grand': 1662.496,
            'Cropsey': 2809.858
        },
        'Roosevelt is': {
            'Manhattan': 1699.934,
            'Washington': 1819.653,
            'Grand': 1282.234,
            'Cropsey': 2769.109
        },
        'Grand': {
            'Manhattan': 1273.837,
            'Washington': 2024.26,
            'Roosevelt is': 1290.025,
            'Cropsey': 2498.591
        },
        'Cropsey': {
            'Manhattan': 1770.744,
            'Washington': 3018.751,
            'Roosevelt is': 2585.918,
            'Grand': 2400.92
        }
    }
    shortest_distance, shortest_path = dijkstra(graph, "Manhattan", "Roosevelt is")


    #values = [1,4,5,7]
    #weights = [1,3,4,5]
    #capacity = 5
#
    #res = knapsack(capacity, weights, values)
#
    #print_selected_items(res, weights, capacity)
