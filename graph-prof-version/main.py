from abc import ABC, abstractmethod


class GraphADT(ABC):
    """The primary abstraction for a graph is the Graph ADT.
    We presume that a graph can be either undirected or directed,
    with the designation declared upon construction; recall that
    a mixed graph can be represented as a directed graph, modeling
    edge {u,v} as a pair of directed edges (u,v) and (v,u)."""

    @abstractmethod
    def vertex_count(self):
        """Return the number of graph's vertices."""
        ...

    @abstractmethod
    def vertices(self):
        """Return an iteration of all the graph's vertices."""
        ...

    @abstractmethod
    def edge_count(self):
        """Return the number of the graph's edges."""
        ...

    @abstractmethod
    def edges(self):
        """Return an iteration of all the graphs' edges."""
        ...

    @abstractmethod
    def get_edge(self, vertex1, vertex2):
        """Return the edge from vertex1 to vertex2 if one exists;
        otherwise return None. For an undirected graph, there is
        no difference between get edge(u,v) and get edge(v,u)."""
        ...

    @abstractmethod
    def degree(self, vertex, outgoing=True):
        """For an undirected graph, return the number of edges incident
         to vertex. For a directed graph, return the number of outgoing
         (resp. incoming) edges incident to vertex, as designated by
         the optional parameter."""
        ...

    @abstractmethod
    def incident_edges(self, vertex, outgoing=True):
        """Return an iteration of all edges incident to vertex. In the case
         of a directed graph, report outgoing edges by default; report
         incoming edges if the optional parameter is set to False."""
        ...

    @abstractmethod
    def insert_vertex(self, vertex):
        """Storese vertex in the graph"""
        ...

    @abstractmethod
    def insert_edge(self, vertex1, vertex2, weight=None):
        """Create and return a new Edge from vertex1 to vertex2,
        storing weight (None by default)."""
        ...

    @abstractmethod
    def remove_vertex(self, vertex):
        """Remove vertex and all its incident edges from the graph."""
        ...

    @abstractmethod
    def remove_edge(self, edge):
        """Remove an edge from the graph."""
        ...


class Vertex:
    __slots__ = '_value'

    def __init__(self, value):
        self._value = value

    def value(self):
        return self._value

    def __hash__(self):
        return hash(id(self))

    def __str__(self):
        return self._value.__str__() if self._value is not None else "Vertex"

    def __eq__(self, other):
        result = False
        if isinstance(other, Vertex) and self._value == other._value:
            result = True
        return result


# TODO adicionar a propriedade de direção na aresta
class Edge:
    """Representation of an edge in a simple graph."""
    __slots__ = '_origin', '_destination', '_weight'

    def __init__(self, u: Vertex, v: Vertex, weight):
        self._origin = u
        self._destination = v
        self._weight = weight

    def endpoints(self):
        return self._origin, self._destination

    def opposite(self, v):
        return self._destination if v is self._origin else self._origin

    def weight(self):
        return self._weight

    def hash(self):
        return hash((self._origin, self._destination))

    def __str__(self):
        return f"Edge({self._origin.value()}, {self._destination.value()}, {self._weight})"


# Todo: implementar grafos mistos (mixed graphs), por hora o grafo é dirigido ou não dirigido

# implementações
class EdgeListGraph(GraphADT):

    def __init__(self, directed=False):
        self._vertices = []
        self._edges = []
        self._directed = directed

    def vertex_count(self):
        return len(self._vertices)

    def vertices(self):
        return self._vertices

    def edge_count(self):
        return len(self._edges)

    def edges(self):
        return self._edges

    def get_edge(self, vertex1, vertex2):
        res = []
        for edge in self._edges:
            if self._directed:
                if edge.endpoints()[0] == vertex1 and edge.endpoints()[1] == vertex2:
                    res.append(edge)
            elif edge.endpoints()[0] == vertex1 and edge.endpoints()[1] == vertex2 or \
                    edge.endpoints()[0] == vertex2 and edge.endpoints()[1] == vertex1:
                res.append(edge)
        return res

    def degree(self, vertex, outgoing=True):
        if self._directed and not outgoing:  # incoming edges
            return sum(1 for edge in self._edges if edge.endpoints()[1] == vertex)
        else: # outgoing edges in a directed graph or all edges in an undirected graph
            return sum(1 for edge in self._edges if edge.endpoints()[0] == vertex)

    def incident_edges(self, vertex, outgoing=True):
        if self._directed and not outgoing:  # incoming edges
            for edge in self._edges:
                if edge.endpoints()[1] == vertex:
                    yield edge
        else:  # outgoing edges in a directed graph or all edges in an undirected graph
            for edge in self._edges:
                if edge.endpoints()[0] == vertex:
                    yield edge

    def insert_vertex(self, vertex):
        self._vertices.append(vertex)

    def insert_vertex_array(self, vertex: list[Vertex]):
        for v in vertex:
            self.insert_vertex(v)

    def insert_edge(self, vertex1, vertex2, weight=None):
        edge = Edge(vertex1, vertex2, weight)
        self._edges.append(edge)
        if not self._directed:
            self._edges.append(Edge(vertex2, vertex1, weight))

        if not vertex1 in self._vertices:
            self._vertices.append(vertex1)
        if not vertex2 in self._vertices:
            self._vertices.append(vertex2)

    def remove_vertex(self, vertex):
        # Remove all edges directed to/from this vertex
        self._edges = [edge for edge in self._edges if edge.endpoints()[0] != vertex and edge.endpoints()[1] != vertex]
        if vertex in self._vertices:
            self._vertices.remove(vertex)

    def remove_edge(self, edge):
        if self._directed:
            self._edges.remove(edge)
            return

        edges = [e for e in self._edges if
                 e.endpoints()[1] == edge.endpoints()[0] and e.endpoints()[0] == edge.endpoints()[1]
                 or e == edge]
        for e in edges:
            self._edges.remove(e)


class AdjacencyListGraph(GraphADT):
    def __init__(self, directed=False):
        self._adjacency_list = {}
        self._directed = directed

    def vertex_count(self):
        return len(self._adjacency_list)

    def vertices(self):
        return self._adjacency_list.keys()

    def edge_count(self):
        total = sum(len(edges) for edges in self._adjacency_list.values())
        return total if self._directed else total // 2

    def edges(self):
        result = set()
        for u, edges in self._adjacency_list.items():
            for v in edges:
                if self._directed or (v, u) not in result:
                    result.add((u, v))
        return result

    def get_edge(self, u, v):
        if u in self._adjacency_list and v in self._adjacency_list[u]:
            return (u, v)
        return None

    def degree(self, v, outgoing=True):
        if outgoing:
            return len(self._adjacency_list.get(v, []))
        else:
            return sum(1 for edges in self._adjacency_list.values() if v in edges)

    def incident_edges(self, v, outgoing=True):
        if outgoing:
            for u in self._adjacency_list.get(v, []):
                yield (v, u)
        else:
            for u, edges in self._adjacency_list.items():
                if v in edges:
                    yield (u, v)

    def insert_vertex(self, x=None):
        if x not in self._adjacency_list:
            self._adjacency_list[x] = []

    def insert_edge(self, u, v, weight=None):
        if u not in self._adjacency_list:
            self.insert_vertex(u)
        if v not in self._adjacency_list:
            self.insert_vertex(v)
        self._adjacency_list[u].append(v)
        if not self._directed:
            self._adjacency_list[v].append(u)

    def remove_vertex(self, vertex):
        if vertex in self._adjacency_list:
            del self._adjacency_list[vertex]
            for edges in self._adjacency_list.values():
                if vertex in edges:
                    edges.remove(vertex)

    def remove_edge(self, edge):
        u, v = edge
        if u in self._adjacency_list and v in self._adjacency_list[u]:
            self._adjacency_list[u].remove(v)
            if not self._directed and u in self._adjacency_list[v]:
                self._adjacency_list[v].remove(u)


class AdjacencyMapGraph(GraphADT):

    def __init__(self, directed=False):
        self._outgoing = {}
        # only create a second map for directed graph; use alias for undirected
        self._incoming = {} if directed else self._outgoing

    def is_directed(self):
        return self._incoming is not self._outgoing

    def vertex_count(self):
        return len(self._outgoing)

    def vertices(self):
        return self._outgoing.keys()

    def edge_count(self):
        total = sum(len(self._outgoing[v]) for v in self._outgoing)
        return total if self.is_directed() else total // 2

    def edges(self):
        result = set()
        for secondary_map in self._outgoing.values():
            result.update(secondary_map.values())  # add edges to a resulting set
        return result

    def get_edge(self, u, v):
        return self._outgoing[u].get(v)  # returns None if v not adjacent

    def degree(self, v, outgoing=True):
        adj = self._outgoing if outgoing else self._incoming
        return len(adj[v])

    def incident_edges(self, v, outgoing=True):
        adj = self._outgoing if outgoing else self._incoming
        for edge in adj[v].values():
            yield edge

    def insert_vertex(self, vertex):
        self._outgoing[vertex] = {}
        if self.is_directed():
            self._incoming[vertex] = {}  # need a distinct map for incoming edges

    def insert_edge(self, u, v, weight=None):
        edge = Edge(u, v, weight)
        self._outgoing[u][v] = edge
        self._incoming[v][u] = edge

    def remove_vertex(self, vertex):
        # Remove all edges incoming to this vertex
        for u in list(self._incoming[vertex].keys()):
            del self._outgoing[u][vertex]
        # Remove all edges outgoing from this vertex
        for v in list(self._outgoing[vertex].keys()):
            del self._incoming[v][vertex]
        # Remove the vertex itself
        del self._outgoing[vertex]
        if self.is_directed():
            del self._incoming[vertex]

    def remove_edge(self, edge):
        u, v = edge.endpoints()
        del self._outgoing[u][v]
        del self._incoming[v][u]


class AdjacencyMatrixGraph(GraphADT):

    def __init__(self, directed=False):
        self._directed = directed
        self._vertices = []  # List of vertices
        self._matrix = []  # Adjacency matrix initialized as empty

    def vertex_count(self):
        return len(self._vertices)

    def vertices(self):
        return self._vertices

    def edge_count(self):
        count = 0
        for row in self._matrix:
            count += sum(1 for weight in row if weight is not None)
        return count if self._directed else count // 2

    def edges(self):
        result = set()
        for i, row in enumerate(self._matrix):
            for j, weight in enumerate(row):
                if weight is not None:
                    result.add((self._vertices[i], self._vertices[j], weight))
        return result

    def get_edge(self, vertex1, vertex2):
        i = self._vertices.index(vertex1)
        j = self._vertices.index(vertex2)
        weight = self._matrix[i][j]
        return Edge(vertex1, vertex2, weight) if weight is not None else None

    def degree(self, vertex, outgoing=True):
        index = self._vertices.index(vertex)
        if outgoing:
            return sum(1 for weight in self._matrix[index] if weight is not None)
        else:
            return sum(1 for row in self._matrix if row[index] is not None)

    def incident_edges(self, vertex, outgoing=True):
        index = self._vertices.index(vertex)
        if outgoing:
            for j, weight in enumerate(self._matrix[index]):
                if weight is not None:
                    yield Edge(vertex, self._vertices[j], weight)
        else:
            for i, row in enumerate(self._matrix):
                if row[index] is not None:
                    yield Edge(self._vertices[i], vertex, row[index])

    def insert_vertex(self, vertex):
        if vertex not in self._vertices:
            self._vertices.append(vertex)
            size = len(self._vertices)
            # Expand the matrix
            for row in self._matrix:
                row.append(None)  # Add a new column
            self._matrix.append([None] * size)  # Add a new row

    def insert_edge(self, vertex1, vertex2, weight=None):
        i = self._vertices.index(vertex1)
        j = self._vertices.index(vertex2)
        self._matrix[i][j] = weight
        if not self._directed:
            self._matrix[j][i] = weight

    def remove_vertex(self, vertex):
        if vertex in self._vertices:
            index = self._vertices.index(vertex)
            # Remove the vertex from vertices list
            self._vertices.pop(index)
            # Remove the row corresponding to this vertex
            self._matrix.pop(index)
            # Remove the column corresponding to this vertex from each remaining row
            for row in self._matrix:
                row.pop(index)

    def remove_edge(self, edge):
        u, v = edge.endpoints()
        if u in self._vertices and v in self._vertices:
            i = self._vertices.index(u)
            j = self._vertices.index(v)
            self._matrix[i][j] = None
            if not self._directed:
                self._matrix[j][i] = None
