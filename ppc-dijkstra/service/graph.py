import copy
import heapq
import random as rd


VERTICES = 20

def generate():
    g = gen_graph(VERTICES)
    a = solve(g)
    return g, a


class Matrix(object):
    def __init__(self, matrix):
        self.matrix = matrix

    def __getitem__(self, ij):
        i, j = ij
        return matrix[i][j]

    def raw(self):
        return self.matrix

    def length(self):
        return len(self.matrix)

    def mirror(self):
        for i in range(len(self.matrix)):
            for j in range(i, len(self.matrix)):
                if i == j:
                    self.matrix[i][j] = float('inf')
                else:
                    self.matrix[j][i] = self.matrix[i][j]


class MaskedMatrix(object):
    def __init__(self, matrix, threshold):
        self._matrix = matrix
        self._threshold = threshold

    def __getitem__(self, ij):
        i, j = ij
        element = self._matrix[i][j]
        if element > self._threshold:
            return None
        return element

    def length(self):
        return len(self._matrix)

    def mask(self):
        return [[x if x <= self._threshold else None for x in row] for row in self._matrix]


def gen_graph(n: int):
    matrix = Matrix([
        [rd.randint(1, 10000) for i in range(n)]
        for j in range(n)
    ])
    matrix.mirror()
    threshold = find_optimal_treshold(matrix, low=0, high=10001)
    matrix = MaskedMatrix(matrix.raw(), threshold)
    return build_graph(matrix)


def find_optimal_treshold(matrix: Matrix, low: int, high: int):
    if high - low <= 1:
        return round(high * 1.5)
    mid = (low + high) // 2
    if is_connected(MaskedMatrix(matrix.raw(), mid)):
        return find_optimal_treshold(matrix, low, mid)
    else:
        return find_optimal_treshold(matrix, mid, high)


def is_connected(matrix: MaskedMatrix):
    used = [False for i in range(matrix.length())]
    dfs(matrix, current=0, prev=-1, used=used)
    return all(used)


def dfs(matrix: MaskedMatrix, current: int, prev: int, used: list):
    if used[current]:
        return
    used[current] = True
    for to in range(matrix.length()):
        if matrix[current, to] is None or to == prev:
            continue
        dfs(matrix, to, current, used)


def build_graph(matrix: MaskedMatrix):
    g = {i + 1: [] for i in range(matrix.length())}
    for i in range(matrix.length()):
        for j in range(matrix.length()):
            if matrix[i,j] is None:
                continue
            g[i+1].append({'connection_to': j+1, 'ping_value': matrix[i,j]})
    return g


def solve(graph):
    inf = float('inf')
    n = len(graph)
    temp = [(inf, i+1) for i in range(n)]
    temp[0] = (0, 1)
    temp.sort()
    distances = {i+1: inf for i in range(n)}
    distances[1] = 0
    while temp:
        dist, vertex = heapq.heappop(temp)
        for target in graph[vertex]:
            connection_to = target['connection_to']
            ping_value = target['ping_value']
            distances[connection_to] = min(distances[connection_to], dist + ping_value)
            for i in range(len(temp)):
                if temp[i][1] == connection_to:
                    temp[i] = distances[connection_to], connection_to
            # Мы обновили элемент в куче, теперь её нужно пересобрать
            # Есть что-то вроде _siftup и _siftdown, но (1) они типа непубличные
            # и (2) мне лень. Поэтому:
            temp.sort()

    return distances
