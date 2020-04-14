import unittest

from editor.graph import Graph

NNODES = 1 << 10


class TestGraph(unittest.TestCase):
    def setUp(self):
        self.graph = Graph()
        print("Input size = {0}".format(NNODES))
        for i in range(NNODES):
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
        for i in range(NNODES):
            self.assertTrue(self.graph.directlyConnected((i, i), (i + 1, i + 1)))
        for i in range(0, NNODES, 2):
            self.assertFalse(self.graph.directlyConnected((i, i), (i + 2, i + 2)))

    def test_find_connected_comps(self):
        self.assertEqual(len(self.graph.connectedComps), 1)

    def test_are_connected(self):
        for i in range(NNODES + 1):
            n1 = (i, i)
            n2 = ((i + 1) % (NNODES + 1), (i + 1) % (NNODES + 1))  # wrap around.
            self.assertTrue(self.graph.areConnected(n1, n2))
        for i in range(0, NNODES + 1, 2):
            n1 = (i, i)
            n2 = ((i + 2) % (NNODES + 1), (i + 2) % (NNODES + 1))  # wrap around.
            self.assertTrue(self.graph.areConnected(n1, n2))
        for i in range(0, NNODES + 1, 10):
            n1 = (i, i)
            n2 = ((i + 10) % (NNODES + 1), (i + 10) % (NNODES + 1))  # wrap around.
            self.assertTrue(self.graph.areConnected(n1, n2))

    def test_move_node(self):
        for i in range(NNODES + 1):
            self.graph.moveNode((i, i), (0.1, 0.1))

        # It is sufficient to check these.
        self.assertTrue(len(self.graph.vertIndices) == NNODES + 1)
        self.assertTrue(len(self.graph.edgeIndices) == NNODES * 2)
        self.assertTrue(len(self.graph.connectedComps) == 1)
        self.assertTrue(len(self.graph.graph) == NNODES + 1)


if __name__ == '__main__':
    unittest.main()
