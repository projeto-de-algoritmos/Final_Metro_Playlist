import math
from heapq import heapify, heappush


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

if __name__ == "__main__":
    graph = {
        "A": {"B": 20, "C": 40},
        "B": {"A": 20, "C": 30, "D": 80},
        "C": {"A": 40, "B": 30, "E": 50, "D": 20},
        "D": {"B": 80, "C": 20, "E": 110, "F": 220},
        "E": {"C": 50, "D": 110, "F": 10},
        "F": {"D": 220, "E": 10},
    }
    dijkstra(graph, "A", "F")


    values = [1,4,5,7]
    weights = [1,3,4,5]
    capacity = 5

    res = knapsack(capacity, weights, values)

    print_selected_items(res, weights, capacity)
