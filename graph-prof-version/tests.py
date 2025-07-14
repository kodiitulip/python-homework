from graphADT import *

from unittest import TestCase


# TODO implementar testes com grafos dirigidos
class TestEdgeListGraph(TestCase):

    def setUp(self):
        self.graph = EdgeListGraph(directed=False)
        self.v1 = Vertex('u')
        self.v2 = Vertex('v')
        self.v3 = Vertex('w')
        self.v4 = Vertex('z')
        self.graph.insert_vertex(self.v1)
        self.graph.insert_vertex(self.v2)
        self.graph.insert_vertex(self.v3)
        self.graph.insert_vertex(self.v4)

        self.digraph = EdgeListGraph(directed=True)
        self.u1 = Vertex('ud')
        self.u2 = Vertex('vd')
        self.u3 = Vertex('wd')
        self.u4 = Vertex('zd')
        self.digraph.insert_vertex_array([self.u1, self.u2, self.u3, self.u4])

    def test_vertex_operations(self):
        self.assertEqual(self.graph.vertex_count(), 4)
        self.graph.remove_vertex(self.v1)
        self.assertEqual(self.graph.vertex_count(), 3)

        self.assertEqual(self.digraph.vertex_count(), 4)
        self.digraph.remove_vertex(self.u1)
        self.assertEqual(self.digraph.vertex_count(), 3)

    def test_edge_operations(self):
        self.graph.insert_edge(self.v1, self.v2, 'edge1')
        self.assertEqual(self.graph.edge_count(), 2)  # undirected graph creates 2 edges
        edge = self.graph.get_edge(self.v1, self.v2)
        self.assertEqual(2,len(edge))
        self.graph.remove_edge(edge[0])
        self.assertEqual(self.graph.edge_count(), 0)

        self.digraph.insert_edge(self.u1, self.u2, 'dedge1')
        self.assertEqual(1, self.digraph.edge_count())  # directed graph creates 1 edge
        edge = self.digraph.get_edge(self.u1, self.u2)
        edge_2 = self.digraph.get_edge(self.u2, self.u1)
        self.assertEqual(1,len(edge))
        self.assertEqual(0, len(edge_2))
        self.digraph.remove_edge(edge[0])
        self.assertEqual(0, self.digraph.edge_count())

    def test_vertex_degree(self):
        self.graph.insert_edge(self.v1, self.v2, 'edge1')
        self.graph.insert_edge(self.v1, self.v3, 'edge2')
        self.assertEqual(self.graph.degree(self.v1), 2)
        self.assertEqual(self.graph.degree(self.v2), 1)

        self.digraph.insert_edge(self.u1, self.u2, 'edge1')
        self.digraph.insert_edge(self.u1, self.u3, 'edge2')
        self.assertEqual(self.digraph.degree(self.u1), 2)
        self.assertEqual(self.digraph.degree(self.u2, outgoing=False), 1)
        self.assertEqual(0, self.digraph.degree(self.u2))

    def test_incident_edges(self):
        self.graph.insert_edge(self.v1, self.v2, 'edge1')
        self.graph.insert_edge(self.v1, self.v3, 'edge2')
        edges = list(self.graph.incident_edges(self.v1))
        self.assertEqual(len(edges), 2)

        self.digraph.insert_edge(self.u1, self.u2, 'edge1')
        self.digraph.insert_edge(self.u1, self.u3, 'edge2')
        edges = list(self.digraph.incident_edges(self.u1))
        edges_2 = list(self.digraph.incident_edges(self.u2, outgoing=False))
        edges_3 = list(self.digraph.incident_edges(self.u3, outgoing=False))
        edges_4 = list(self.digraph.incident_edges(self.u2))
        edges_5 = list(self.digraph.incident_edges(self.u3))
        self.assertEqual(len(edges), 2)
        self.assertEqual(1, len(edges_2))
        self.assertEqual(1, len(edges_3))
        self.assertEqual(0, len(edges_4))
        self.assertEqual(0, len(edges_5))


class TestAdjacencyListGraph(TestCase):

    def setUp(self):
        self.graph = AdjacencyListGraph(directed=False)
        self.v1 = Vertex('u')
        self.v2 = Vertex('v')
        self.v3 = Vertex('w')
        self.v4 = Vertex('z')
        self.graph.insert_vertex(self.v1)
        self.graph.insert_vertex(self.v2)
        self.graph.insert_vertex(self.v3)
        self.graph.insert_vertex(self.v4)

        self.digraph = AdjacencyListGraph(directed=True)
        self.u1 = Vertex('ud')
        self.u2 = Vertex('vd')
        self.u3 = Vertex('wd')
        self.u4 = Vertex('zd')
        self.digraph.insert_vertex(self.u1)
        self.digraph.insert_vertex(self.u2)
        self.digraph.insert_vertex(self.u3)
        self.digraph.insert_vertex(self.u4)

    def test_vertex_operations(self):
        self.assertEqual(self.graph.vertex_count(), 4)
        self.graph.remove_vertex(self.v1)
        self.assertEqual(self.graph.vertex_count(), 3)


        self.assertEqual(self.digraph.vertex_count(), 4)
        self.digraph.remove_vertex(self.u1)
        self.assertEqual(self.digraph.vertex_count(), 3)

    def test_edge_operations(self):
        self.graph.insert_edge(self.v1, self.v2, 'edge1')
        self.assertEqual(self.graph.edge_count(), 1)
        edge = self.graph.get_edge(self.v1, self.v2)
        self.assertIsNotNone(edge)
        self.graph.remove_edge(edge)
        self.assertEqual(self.graph.edge_count(), 0)

        self.digraph.insert_edge(self.u1, self.u2, 'dedge1')
        self.assertEqual(self.digraph.edge_count(), 1)
        edge = self.digraph.get_edge(self.u1, self.u2)
        self.assertIsNotNone(edge)
        self.digraph.remove_edge(edge)
        self.assertEqual(self.digraph.edge_count(), 0)

    def test_vertex_degree(self):
        self.graph.insert_edge(self.v1, self.v2, 'edge1')
        self.graph.insert_edge(self.v1, self.v3, 'edge2')
        self.assertEqual(self.graph.degree(self.v1), 2)
        self.assertEqual(self.graph.degree(self.v2), 1)

        self.digraph.insert_edge(self.u1, self.u2, 'edge1')
        self.digraph.insert_edge(self.u1, self.u3, 'edge2')
        self.assertEqual(self.digraph.degree(self.u1), 2)
        self.assertEqual(self.digraph.degree(self.u2, outgoing=False), 1)

    def test_incident_edges(self):
        self.graph.insert_edge(self.v1, self.v2, 'edge1')
        self.graph.insert_edge(self.v1, self.v3, 'edge2')
        edges = list(self.graph.incident_edges(self.v1))
        self.assertEqual(len(edges), 2)


class TestAdjacencyMapGraph(TestCase):

    def setUp(self):
        self.graph = AdjacencyMapGraph(directed=False)
        self.v1 = Vertex('u')
        self.v2 = Vertex('v')
        self.v3 = Vertex('w')
        self.v4 = Vertex('z')
        self.graph.insert_vertex(self.v1)
        self.graph.insert_vertex(self.v2)
        self.graph.insert_vertex(self.v3)
        self.graph.insert_vertex(self.v4)

    def test_vertex_operations(self):
        self.assertEqual(self.graph.vertex_count(), 4)
        self.graph.remove_vertex(self.v1)
        self.assertEqual(self.graph.vertex_count(), 3)

    def test_edge_operations(self):
        self.graph.insert_edge(self.v1, self.v2, 'edge1')
        self.assertEqual(self.graph.edge_count(), 1)
        edge = self.graph.get_edge(self.v1, self.v2)
        self.assertIsNotNone(edge)
        self.graph.remove_edge(edge)
        self.assertEqual(self.graph.edge_count(), 0)

    def test_vertex_degree(self):
        self.graph.insert_edge(self.v1, self.v2, 'edge1')
        self.graph.insert_edge(self.v1, self.v3, 'edge2')
        self.assertEqual(self.graph.degree(self.v1), 2)
        self.assertEqual(self.graph.degree(self.v2), 1)

    def test_incident_edges(self):
        self.graph.insert_edge(self.v1, self.v2, 'edge1')
        self.graph.insert_edge(self.v1, self.v3, 'edge2')
        edges = list(self.graph.incident_edges(self.v1))
        self.assertEqual(len(edges), 2)


class TestAdjacencyMatrixGraph(TestCase):

    def setUp(self):
        self.graph = AdjacencyMatrixGraph(directed=False)
        self.v1 = Vertex('u')
        self.v2 = Vertex('v')
        self.v3 = Vertex('w')
        self.v4 = Vertex('z')
        self.graph.insert_vertex(self.v1)
        self.graph.insert_vertex(self.v2)
        self.graph.insert_vertex(self.v3)
        self.graph.insert_vertex(self.v4)

    def test_vertex_operations(self):
        self.assertEqual(self.graph.vertex_count(), 4)
        self.graph.remove_vertex(self.v1)
        self.assertEqual(self.graph.vertex_count(), 3)
        self.assertNotIn(self.v1, self.graph.vertices())

    def test_edge_operations(self):
        self.graph.insert_edge(self.v1, self.v2, 'edge1')
        self.assertEqual(self.graph.edge_count(), 1)
        edge = self.graph.get_edge(self.v1, self.v2)
        self.assertIsNotNone(edge)
        self.graph.remove_edge(edge)
        self.assertEqual(self.graph.edge_count(), 0)

    def test_vertex_degree(self):
        self.graph.insert_edge(self.v1, self.v2, 'edge1')
        self.graph.insert_edge(self.v1, self.v3, 'edge2')
        self.assertEqual(self.graph.degree(self.v1), 2)
        self.assertEqual(self.graph.degree(self.v2), 1)

    def test_incident_edges(self):
        self.graph.insert_edge(self.v1, self.v2, 'edge1')
        self.graph.insert_edge(self.v1, self.v3, 'edge2')
        edges = list(self.graph.incident_edges(self.v1))
        self.assertEqual(len(edges), 2)

    def test_directed_graph(self):
        directed_graph = AdjacencyMatrixGraph(directed=True)
        directed_graph.insert_vertex(self.v1)
        directed_graph.insert_vertex(self.v2)
        directed_graph.insert_edge(self.v1, self.v2, 'edge1')
        self.assertEqual(directed_graph.degree(self.v1, outgoing=True), 1)
        self.assertEqual(directed_graph.degree(self.v1, outgoing=False), 0)
        self.assertEqual(directed_graph.degree(self.v2, outgoing=True), 0)
        self.assertEqual(directed_graph.degree(self.v2, outgoing=False), 1)
