def bfs(graph, start, end):
    visited = set()
    queue = [[start]]

    if start == end:
        return [start]

    while queue:
        path = queue.pop(0)
        node = path[-1]

        if node not in visited:
            neighbours = graph.get(node, [])

            for neighbour in neighbours:
                new_path = list(path)
                new_path.append(neighbour)
                queue.append(new_path)

                if neighbour == end:
                    return new_path

            visited.add(node)

    return []


def dfs(graph, start, end, path=None, visited=None):
    if visited is None:
        visited = set()
    if path is None:
        path = []

    path.append(start)
    visited.add(start)

    if start == end:
        return path

    for neighbor in graph.get(start, []):
        if neighbor not in visited:
            result = dfs(graph, neighbor, end, list(path), set(visited))
            if result:
                return result

    return []
