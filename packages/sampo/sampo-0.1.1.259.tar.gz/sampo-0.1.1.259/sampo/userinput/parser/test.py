from collections import defaultdict


class Graph:
    def __init__(self, vertices):
        self.vertices = vertices
        self.graph = defaultdict(list)

    def add_edge(self, u, v, weight):
        self.graph[u].append((v, weight))

    def dfs_cycle(self, u, visited, path, parent):
        stack = [u]

        while len(stack) > 0:
            v = stack.pop()
            if visited[v] == 1:
                visited[v] = 2
                continue
            if visited[v] == 2:
                continue
            visited[v] = 1
            path.append(v)
            stack.append(v)
            if len(self.graph[v]) == 0:
                path = []
            for neighbour, weight in self.graph[v]:
                if visited[neighbour] == 0:
                    stack.append(neighbour)
                elif visited[neighbour] == 1:
                    path.append(neighbour)
                    return True
        return False

    def find_cycle(self):
        visited = {}
        for i in self.graph:
            visited[i] = 0
        path = []

        for key, value in visited.items():
            if value == 0:
                if self.dfs_cycle(key, visited, path, -1):
                    return path

        return None

    def eliminate_cycle(self, cycle):
        min_weight = float('inf')
        min_edge = None

        for i in range(len(cycle) - 1):
            u = cycle[i]
            v = cycle[i + 1]

            for neighbor, weight in self.graph[u]:
                if neighbor == v and weight < min_weight:
                    min_weight = weight
                    min_edge = (u, v)

        u, v = min_edge
        self.graph[u] = [(neighbor, weight) for neighbor, weight in self.graph[u] if neighbor != v]

    def eliminate_cycles(self):
        cycle = self.find_cycle()

        while cycle is not None:
            for i in range(len(cycle)):
                if cycle[i] == cycle[-1]:
                    cycle = cycle[i:]
                    break
            self.eliminate_cycle(cycle)
            cycle = self.find_cycle()


# Example usage
graph = Graph(7)
graph.add_edge('0', '1', 2)
graph.add_edge('0', '5', 2)
graph.add_edge('1', '2', 3)
graph.add_edge('2', '3', 1)
graph.add_edge('3', '1', 4)
graph.add_edge('5', '6', 3)
graph.add_edge('6', '3', 2)
graph.add_edge('3', '5', 1)
graph.add_edge('3', '2', 4)

print("Original graph:")
print(graph.graph)

graph.eliminate_cycles()

print("\nGraph after eliminating cycles:")
print(graph.graph)

