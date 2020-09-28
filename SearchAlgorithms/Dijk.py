from collections import defaultdict, deque

class Graph(object):
	def __init__(self):
		self.nodes = set()
		self.edges = defaultdict(list)
		self.distances = {}

	def add_node(self, value):
		self.nodes.add(value)

	def add_edge(self, fro, to, distance):
		self.edges[fro].append(to)
		self.edges[to].append(fro)
		self.distances[(fro, to)] = distance

def dijsktras(graph, start):
	visited = {start:0}
	path = {}
	nodes = set(graph.nodes)
	while nodes:
		min_node = None
		for node in nodes:
			if node in visited:
				if min_node is None:
					min_node = node
				elif visited[node] < visited[min_node]:
					min_node = node
		if min_node is None:
			break
		nodes.remove(min_node)
		weight = visited[min_node]

		for edge in graph.edges[min_node]:
			try:
				final_weight = weight + graph.distances[(min_node, edge)]
			except:
				continue
			if edge not in visited or final_weight < visited[edge]:
				visited[edge] = final_weight
				path[edge] = min_node
	return visited, path

def get_path(graph, origin, destination):
	visited, path = dijsktras(graph, origin)
	full_path = deque()
	_destination = path[destination]

	while _destination != origin:
		full_path.appendleft(_destination)
		_destination = path[_destination]

	full_path.appendleft(origin)
	full_path.append(destination)
	return visited[destination], list(full_path)

if __name__ == '__main__':
    graph = Graph()

    for node in ['A', 'B', 'C', 'D', 'E', 'F', 'G']:
        graph.add_node(node)

    graph.add_edge('A', 'B', 10)
    graph.add_edge('A', 'C', 20)
    graph.add_edge('B', 'D', 15)
    graph.add_edge('C', 'D', 30)
    graph.add_edge('B', 'E', 50)
    graph.add_edge('D', 'E', 30)
    graph.add_edge('E', 'F', 5)
    graph.add_edge('F', 'G', 2)

    print(get_path(graph, 'A', 'G')) # output: (25, ['A', 'B', 'D']) 


