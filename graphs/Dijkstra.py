"""
# Revision

# What is the definition of the shortest path between two vertices in a weighted graph?
the path (sequence of oriented edges) of total minimum weight i.e smallest cost between two vertices

# What are the main steps in Dijkstra's algorithm?
while we still have open vertices
    pick the open vertex with lowest cost
    expand from that vertex to all neighbours not yet closed
    for each neighbour we reached
        add the cost of the edge to the neighbour onto the cost for the vertex to get a new path cost to the neighbour
        if the path cost is lower than the previous one, or neighbour is new
        update the neighbours path cost
    close the current vertex


# What is an Adaptable Priority Queue? Where would you use it in Dijkstra's algorithm?
# What APQ implementation would be best for use in Dijkstra applied to standard road maps?

An APQ is an adaptable collection of objects where the item with the highest priority is removed next
adaptable meaning the priority of objects can change, or any object can be removed
Objects are stored with three pieces of data:
    the value, representing the original item
    the key, representing its priority
    the index, representing its position in the APQ which enables constant access


In Dijkstra's algorithm
we need to maintain the path costs for all open vertices in a structure we can query,
obtain the minimum cost vertex efficiently, and update with new costs efficiently
-- an APQ is ideal for this structure
we use an APQ for open vertices, key is the cost, value is the vertex
and a dictionary of locations for accessing elements in the APQ


Heap APQ or Unsorted APQ
Dijkstra requires:
n additions to the APQ: n*O(log n) or n*O(1)
n removals of min key item from APQ: n*O(log n) or n*O(n)
m updates (or additions) to the APQ = m*O(log n) or m*O(1)

total is O(n log n + m log n) or O(n + n**2 + m)
    = O((n+m)log n) or O(n**2 + m)

Heap APQ or Unsorted APQ
Dense Graph: O(n**2 log n)  or O(n**2)
Sparse Graph: O(n log n)    or O(n**2)

Since a graph for standard road maps is very sparse
i.e for every junction, it is not directly connected to more than 5 other junctions
a Heap AQP is a more efficient implementation
"""

from heapAPQ import *
from graph import *


class Dijkstra(Graph):

    def __init__(self):
        """ Create an initial empty graph. """
        super().__init__()

    def dijkstra(self, s):
        """find all shortest paths from s"""
        open = Heap_APQ()  # open starts as an empty APQ
        locs = {}  # locs is an empty dictionary (keys are vertices, values are location in open)
        closed = {}  # closed starts as an empty dictionary
        preds = {s: None}  # preds starts as a dictionary with value for s= None
        elt = open.add(0, s)  # add s with APQ key 0 to open,
        locs[s] = elt  # and add s:(elt returned from APQ) to locs
        while not open.is_empty():  # while open is not empty
            v, cost = open.remove_min()  # remove the min element v and its cost (key) from open
            del locs[v]  # remove the entry for v from locs and preds(which returns predecessor)
            predecessor = preds.pop(v)
            closed[v] = (cost, predecessor)  # add an entry for v:(cost, predecessor) into closed
            for e in self.get_edges(v):  # for each edge e from v
                w = e.opposite(v)  # w is the opposite vertex to v in e
                if w not in closed:  # if w is not in closed
                    newcost = cost + e.element()  # newcost is v's key plus e's cost
                    if w not in locs:  # if w is not in locs //i.e. not yet added into open
                        preds[w] = v  # add w:v to preds
                        elt = open.add(newcost, w)  # add w:newcost to open
                        locs[w] = elt  # add w:(elt returned from open) to locs
                    elif newcost < open.get_key(locs[w]):  # else if newcost is better than w's oldcost
                        preds[w] = v  # update w:v in preds
                        open.update_key(locs[w], newcost)  # update w's cost in open to newcost
        return closed


def graphreader(filename):
    """ Read and return the route map in filename. """
    graph = Dijkstra()
    file = open(filename, 'r')
    entry = file.readline() #either 'Node' or 'Edge'
    num = 0
    while entry == 'Node\n':
        num += 1
        nodeid = int(file.readline().split()[1])
        vertex = graph.add_vertex(nodeid)
        entry = file.readline() #either 'Node' or 'Edge'
    print('Read', num, 'vertices and added into the graph')
    num = 0
    while entry == 'Edge\n':
        num += 1
        source = int(file.readline().split()[1])
        sv = graph.get_vertex_by_label(source)
        target = int(file.readline().split()[1])
        tv = graph.get_vertex_by_label(target)
        length = float(file.readline().split()[1])
        edge = graph.add_edge(sv, tv, length)
        file.readline() #read the one-way data
        entry = file.readline() #either 'Node' or 'Edge'
    print('Read', num, 'edges and added into the graph')
    print(graph)
    return graph

def print_results(dic):
    for vertex in dic:
        result = dic[vertex]
        vstr = 'Vertex:' + str(vertex) + ' --->'
        cstr = 'Cost: ' + str(result[0])
        pstr = 'Predecessor: ' + str(result[1])
        print("{0:16}{1:12}{2}".format(vstr, cstr, pstr))

graph1 = graphreader('data/simplegraph1.txt')
v1 = graph1.get_vertex_by_label(1)
print_results(graph1.dijkstra(v1))

graph2 = graphreader('data/simplegraph2.txt')
v14 = graph2.get_vertex_by_label(14)
print_results(graph2.dijkstra(v14))
