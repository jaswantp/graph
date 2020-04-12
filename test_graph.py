import unittest

from graph import Graph


class TestGraph(unittest.TestCase):
    def setUp(self):
        self.graph = Graph()
        for i in range(10000):
            self.graph.addEdge((i, i), (i + 1, i + 1))

    def test_delete_edge(self):
        self.graph.deleteEdge((1, 1), (2, 2))
        self.assertFalse(self.graph.edgeExists((1, 1), (2, 2)))

    def test_delete_node(self):
        self.assertTrue(self.graph.nodeExists((2, 2)))
        self.graph.deleteNode((2, 2))
        self.assertFalse(self.graph.nodeExists((2, 2)))

    def test_dissolve_node(self):

        # * ----> node3
        #  \
        #   \
        #    \
        #     * ----> node2 (this will be dissolved)
        #     |
        #     |
        #     |
        #     * ----> node1

        # * ----> node3
        #  \                   ------------
        #   \                              |
        #    \                             |
        #     \                             == > New edge connects node1, node3
        #      \                           |
        #       \                          |
        #        \             ------------
        #         *  ----> node1
        node1 = (1, 1)
        node2 = (2, 2)
        node3 = (3, 3)
        self.graph.dissolveNode(node2)
        # Verify node2 is dissolved.
        self.assertFalse(self.graph.nodeExists(node2))
        self.assertFalse(self.graph.edgeExists(node1, node2))
        self.assertFalse(self.graph.directlyConnected(node1, node2))
        # Verify that an edge connects node1, node3
        self.assertTrue(self.graph.edgeExists(node1, node3))
        self.assertTrue(self.graph.directlyConnected(node1, node3))

    def test_split_edge(self):

        # * ----> node3
        #  \                   ------------
        #   \                              |
        #    \                             |
        #     \                             == > This edge will be split.
        #      \                           |
        #       \                          |
        #        \             ------------
        #         *  ----> node2

        # * ----> node3
        #  \
        #   \
        #    \
        #     * ----> node (this will be added)
        #      \
        #       \
        #        \
        #         * ----> node2

        node2 = (2, 2)
        node3 = (3, 3)
        self.graph.splitEdge(node2, node3)
        # Verify node is present.
        node = ((node2[0] + node3[0]) * 0.5,
                (node2[1] + node3[1]) * 0.5)

        self.assertTrue(self.graph.nodeExists(node))
        # Verify that an edge connects node, node2
        self.assertTrue(self.graph.edgeExists(node, node2))
        self.assertTrue(self.graph.directlyConnected(node, node2))
        # Verify that an edge connects node, node3
        self.assertTrue(self.graph.edgeExists(node, node3))
        self.assertTrue(self.graph.directlyConnected(node, node3))

    def test_directly_connected(self):
        for i in range(10000):
            self.assertTrue(self.graph.directlyConnected((i, i), (i + 1, i + 1)))
        for i in range(0, 10000, 2):
            self.assertFalse(self.graph.directlyConnected((i, i), (i + 2, i + 2)))

    def test_find_connected_comps(self):
        self.graph.findConnectedComps()
        self.assertEqual(len(self.graph.connectedComps), 1)

    def test_are_connected(self):
        self.graph.findConnectedComps()
        for i in range(10000):
            self.assertTrue(self.graph.areConnected((i, i), (i + 1, i + 1)))
        for i in range(0, 10000, 2):
            self.assertTrue(self.graph.areConnected((i, i), (i + 2, i + 2)))
        for i in range(0, 10000, 10):
            self.assertTrue(self.graph.areConnected((i, i), (i + 10, i + 10)))


if __name__ == '__main__':
    unittest.main()
