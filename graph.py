"""@package Graph
A convenient class to handle a graph with nodes and edges.
"""

import logging
from collections import defaultdict
from itertools import combinations

import typing

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(message)s')


class Graph:
    """
    An adjacency list representation of an undirected graph.
    n1 : set([n3, n5])
    n2 : set([n4, n1, n3])
    n3 : .....
    n4 : .....
    .  : .....
    .  : .....
    """

    def __init__(self):
        self.graph = defaultdict(set)  # {node: set(adjacency list)}
        self.newnodes = set()
        self.connectedComps = []
        self.indices = {}

    def nodeExists(self, node: typing.Any):
        return True if self.graph[node] else False

    def edgeExists(self, node1: typing.Any, node2: typing.Any):
        return node2 in self.graph[node1]

    def addEdge(self, node1: typing.Any, node2: typing.Any):
        self.graph[node1].add(node2)
        self.graph[node2].add(node1)

    def deleteEdge(self, node1: typing.Any, node2: typing.Any):
        self.graph[node1].discard(node2)
        self.graph[node2].discard(node1)

    def dissolveNode(self, node: typing.Any):
        self.graph[node].clear()  # Clear the node's adjacency list.
        for _node in self.graph:
            if node in self.graph[_node]:
                self.newnodes.add(_node)  # keep track of connected nodes. Implementation might want to undo dissolve.
            self.graph[_node].discard(node)  # discard node from other node's adjacency list.
        nodepairs = list(combinations(self.newnodes, 2))  # connect nodepairs with edges.
        for nodepair in nodepairs:
            self.addEdge(nodepair[0], nodepair[1])

    def splitEdge(self, node1: typing.Any, node2: typing.Any):
        # split into two edges.
        newnode = ((node1[0] + node2[0]) * 0.5,
                   (node1[1] + node2[1]) * 0.5)
        # delete edge (node1, node2)
        self.deleteEdge(node1, node2)
        # add edge (node1, newnode) and (newnode, node2)
        self.addEdge(node1, newnode)
        self.addEdge(newnode, node2)

    def directlyConnected(self, node1: typing.Any, node2: typing.Any):
        return node1 in self.graph[node2] or node2 in self.graph[node1]

    def dfsiterative(self, thisnode: typing.Any, visited: list):
        """
        Depth first search algorithm. [https://en.wikipedia.org/wiki/Depth-first_search#cite_note-6] O(E)
        Args:
            thisnode: the current node in the dfs algorithm.
            visited: a list of nodes that have been visited.
        Returns:(list) component
        """
        # Use a custom stack.
        stack = [thisnode]
        component = []

        while stack:
            node = stack.pop()
            if node not in visited:
                visited.append(node)
                component.append(node)
                stack.extend(self.graph[node])
        return component

    def dfsrecrusive(self, thisnode: typing.Any, component: list, visited: list):
        """
        Depth first search algorithm. [https://en.wikipedia.org/wiki/Depth-first_search#cite_note-5]
        Args:
            thisnode: the current node in the dfs algorithm.
            component: a list of nodes that belong to a single component.
            visited: a list of nodes that have been visited.
        Returns:(list) temp
        """
        visited.append(thisnode)
        component.append(thisnode)

        for adjnode in self.graph[thisnode]:
            if adjnode not in visited:
                component = self.dfsrecrusive(adjnode, component, visited)

        return component

    def findConnectedComps(self):
        """
        Call this method when an edge is added or at once after all edges are added.
        Python is beautiful and all but unlike c++ it doesn't do tail call optimizations.
        So, this method automatically switches to iterative algorithm on a recursion error.
        Returns: None
        """
        self.connectedComps.clear()
        try:
            visited = []
            for node in self.graph:
                if node not in visited:
                    component = []
                    self.connectedComps.append(self.dfsrecrusive(node, component, visited))
        except RecursionError:
            logger.info("Switched to iterative")
            visited = []
            for node in self.graph:
                if node not in visited:
                    self.connectedComps.append(self.dfsiterative(node, visited))

    def areConnected(self, node1: typing.Any, node2: typing.Any):
        """
        Checks if node1, node2 belong to a same connected component.
        Args:
            node1: Any
            node2: Any

        Returns: bool

        """
        for comp in self.connectedComps:
            if node1 in comp and node2 in comp:
                return True
            else:
                continue
        return False

    def generateIndices(self):
        """
        Generates table of indices for nodes. key : value ==> node : index
        Can fetch index of a node. with self.indices.get(node)
        """
        for i, node in enumerate(self.graph):
            self.indices.update({node: i})


if __name__ == '__main__':
    import timeit

    dfsAlgo = """
from graph import Graph
g = Graph()
for i in range(1_000_000):
    g.addEdge((i, i), (i + 1, i + 1))
g.findConnectedComps()
print("No. of connected components: {0}".format(len(g.connectedComps)))
"""
    time = timeit.timeit(dfsAlgo, number=1)
    print("Executed in {0}".format(time))
