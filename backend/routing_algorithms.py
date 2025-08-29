import heapq
from collections import deque

# ---------- BFS (unweighted shortest in hops) ----------
def bfs(graph, start, goal):
    if start == goal:
        return [start]
    visited = set([start])
    q = deque([[start]])
    while q:
        path = q.popleft()
        node = path[-1]
        for nbr in graph[node].keys():
            if nbr not in visited:
                visited.add(nbr)
                new_path = path + [nbr]
                if nbr == goal:
                    return new_path
                q.append(new_path)
    return None

# ---------- DFS (depth-first path, not guaranteed shortest) ----------
def dfs(graph, start, goal):
    stack = [[start]]
    visited = set()
    while stack:
        path = stack.pop()
        node = path[-1]
        if node == goal:
            return path
        if node not in visited:
            visited.add(node)
            for nbr in graph[node].keys():
                if nbr not in path:
                    stack.append(path + [nbr])
    return None

# ---------- Uniform Cost Search (Dijkstra) ----------
def ucs(graph, start, goal):
    pq = [(0.0, [start])]
    visited = dict()  # node -> best_cost_found
    while pq:
        cost, path = heapq.heappop(pq)
        node = path[-1]
        if node == goal:
            return path
        if node in visited and visited[node] <= cost:
            continue
        visited[node] = cost
        for nbr, w in graph[node].items():
            heapq.heappush(pq, (cost + w, path + [nbr]))
    return None

# ---------- A* Search ----------
def astar(graph, start, goal, coordinates):
    def h(a, b):
        (x1, y1), (x2, y2) = coordinates[a], coordinates[b]
        return ((x1 - x2)**2 + (y1 - y2)**2) ** 0.5

    pq = [(h(start, goal), 0.0, [start])]
    best_g = {start: 0.0}

    while pq:
        f, g, path = heapq.heappop(pq)
        node = path[-1]
        if node == goal:
            return path
        for nbr, w in graph[node].items():
            ng = g + w
            if nbr not in best_g or ng < best_g[nbr]:
                best_g[nbr] = ng
                heapq.heappush(pq, (ng + h(nbr, goal), ng, path + [nbr]))
    return None

# ---------- Greedy Best-First ----------
def greedy(graph, start, goal, coordinates):
    def h(a, b):
        (x1, y1), (x2, y2) = coordinates[a], coordinates[b]
        return ((x1 - x2)**2 + (y1 - y2)**2) ** 0.5

    pq = [(h(start, goal), [start])]
    visited = set()

    while pq:
        _, path = heapq.heappop(pq)
        node = path[-1]
        if node == goal:
            return path
        if node in visited:
            continue
        visited.add(node)
        for nbr in graph[node].keys():
            if nbr not in visited:
                heapq.heappush(pq, (h(nbr, goal), path + [nbr]))
    return None

# ---------- Depth Limited Search ----------
def dls(graph, start, goal, limit):
    def rec(node, goal, path, limit):
        if node == goal:
            return path
        if limit == 0:
            return None
        for nbr in graph[node].keys():
            if nbr not in path:
                res = rec(nbr, goal, path + [nbr], limit - 1)
                if res:
                    return res
        return None
    return rec(start, goal, [start], limit)

# ---------- Iterative Deepening Search ----------
def ids(graph, start, goal, max_depth=30):
    for d in range(max_depth + 1):
        res = dls(graph, start, goal, d)
        if res:
            return res
    return None

# ---------- AO* (OR-graph adaptation; behaves like an informed best-first that keeps g & h) ----------
def ao_star(graph, start, goal, coordinates):
    def h(a, b):
        (x1, y1), (x2, y2) = coordinates[a], coordinates[b]
        return ((x1 - x2)**2 + (y1 - y2)**2) ** 0.5

    # We’ll keep an open set keyed by node -> (f, g, path)
    open_map = {start: (h(start, goal), 0.0, [start])}
    closed = set()

    while open_map:
        # pick node with smallest f
        current = min(open_map.items(), key=lambda kv: kv[1][0])
        node, (f, g, path) = current
        del open_map[node]

        if node == goal:
            return path

        closed.add(node)

        for nbr, w in graph[node].items():
            if nbr in closed:
                continue
            ng = g + w
            nf = ng + h(nbr, goal)
            # Only keep the best variant per node
            if nbr not in open_map or nf < open_map[nbr][0]:
                open_map[nbr] = (nf, ng, path + [nbr])

    return None
