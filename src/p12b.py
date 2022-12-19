import sys
import numpy as np

import heapq
from collections import defaultdict


def dijkstra(graph, start_id):
    visited_node_ids = set()
    path_parent_mapping = {}
    pq = []
    node_costs = defaultdict(lambda: float('inf'))
    node_costs[start_id] = 0

    heapq.heappush(pq, (0, start_id))
    while pq:
        _, node_id = heapq.heappop(pq)
        visited_node_ids.add(node_id)

        for adjacent_node_id, weight in graph[node_id]:
            if adjacent_node_id in visited_node_ids:
                continue

            new_cost = node_costs[node_id] + weight
            if node_costs[adjacent_node_id] > new_cost:
                path_parent_mapping[adjacent_node_id] = node_id
                node_costs[adjacent_node_id] = new_cost
                heapq.heappush(pq, (new_cost, adjacent_node_id))
    return node_costs


ORD_UFUNC = np.frompyfunc(ord, 1, 1)


def read_map(fd):
    heightmap = np.array([list(line.strip()) for line in fd])
    start_node_id = find_letter(heightmap, 'S')
    end_node_id = find_letter(heightmap, 'E')

    heightmap[start_node_id] = 'a'
    heightmap[end_node_id] = 'z'
    heightmap_int = ORD_UFUNC(heightmap)

    height, width = heightmap_int.shape
    graph = {
        (x, y): [
            ((x + dx, y + dy), 1)
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
            if 0 <= x + dx < height and 0 <= y + dy < width
            and heightmap_int[x, y] <= 1 + heightmap_int[x + dx, y + dy]
        ]
        for x in range(height)
        for y in range(width)
    }

    start_node_ids = list(zip(*np.where(heightmap == 'a')))

    return graph, start_node_ids, end_node_id


def main(filename):
    with open(filename) as fd:
        graph, start_node_ids, end_node_id = read_map(fd)

    node_costs = dijkstra(graph, end_node_id)
    print(min(node_costs[node_id] for node_id in start_node_ids))


def find_letter(map, letter):
    xs, ys = np.where(map == letter)
    return xs[0], ys[0]


if __name__ == '__main__':
    main(sys.argv[1])
