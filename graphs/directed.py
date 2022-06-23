'''
# 1. Revision
# i. What is the difference between depth-first search and breadth-first search
    on undirected simple graphs with no edge loops?
With DFS some vertices which are very close to the start vertex are not discovered until late in the traversal.
Breadth-first traversal visits all vertices that are 1 hop away from the start before those that are 2 hops away, etc.


# ii. What is the difference between an undirected graph and a directed graph? What is a DAG?
In a directed graph we treat the order of the vertices in an Edge as significant
a path from X to Y does not imply that there is a path from Y to X

A graph which is directed but does not contain a cycle is a DAG (Directed Acyclic Graph)

# iii. What is a topological sort of a DAG?
an ordered sequence of all vertices in the graph such that if two vertices x and y have a directed edge (x,y),
then x appears before y in the sequence

'''

from stack import Stack
import copy


class Vertex:
    """ A Vertex in a graph. """

    def __init__(self, element):
        """ Create a vertex, with data element. """
        self._element = element

    def __str__(self):
        """ Return a string representation of the vertex. """
        return str(self._element)

    def __lt__(self, v):
        return self._element < v.element()

    def element(self):
        """ Return the data for the vertex. """
        return self._element


class Edge:
    """ An edge in a graph.

    Implemented with an order, so can be used for directed or undirected
    graphs. Methods are provided for both. It is the job of the Graph class
    to handle them as directed or undirected.
    """

    def __init__(self, v, w, element):
        """ Create an edge between vertices v and w, with label element.

            element can be an arbitrarily complex structure.
        """
        self._vertices = (v, w)
        self._element = element

    def __str__(self):
        """ Return a string representation of this edge. """
        return ('(' + str(self._vertices[0]) + '--'
                + str(self._vertices[1]) + ' : '
                + str(self._element) + ')')

    def vertices(self):
        """ Return an ordered pair of the vertices of this edge. """
        return self._vertices

    def start(self):
        """ Return the first vertex in the ordered pair. """
        return self._vertices[0]

    def end(self):
        """ Return the second vertex in the ordered. pair. """
        return self._vertices[1]

    def opposite(self, v):
        """ Return the opposite vertex to v in this edge. """
        if self._vertices[0] == v:
            return self._vertices[1]
        elif self._vertices[1] == v:
            return self._vertices[0]
        else:
            return None

    def element(self):
        """ Return the data element for this edge. """
        return self._element


class DirectedGraph:
    """ Represent a simple directed graph.

    Implemented as two adjacency maps (dictionary of dictionaries)
     - as with the undirected graph, each edge is represented twice:
       - the first dictionary maintains the out-edges
       - the second maintains the in-edges
     - the keys are the vertices
     - the values are the edges for the corresponding vertex
       Each edge set is also maintained as a dictionary,
       with opposite vertex as the key and the edge object as the value
    """

    def __init__(self):
        """ Create an initial empty graph. """
        self._structure = dict()  # keep old name to reuse methods
        self._inedges = dict()

    def __str__(self):
        """ Return a string representation of the graph.

        Only represents the forward edges.
        """
        hstr = ('|V| = ' + str(self.num_vertices())
                + '; |E| = ' + str(self.num_edges()))
        vstr = '\nVertices: '
        for v in self._structure:
            vstr += str(v) + '-'
        edges = self.edges()
        estr = '\nEdges: '
        for e in edges:
            estr += str(e) + ' '
        return hstr + vstr + estr

    # -------------------------------------------------- #
    # ADT methods to query the graph

    def num_vertices(self):
        """ Return the number of vertices in the graph. """
        return len(self._structure)

    def num_edges(self):
        """ Return the number of edges in the graph. """
        num = 0
        for v in self._structure:
            num += len(self._structure[v])  # the dict of edges for v
        return num  # don't divide by 2 - only look at out edges

    def vertices(self):
        """ Return a list of all vertices in the graph. """
        return [key for key in self._structure]

    def get_vertex_by_label(self, element):
        """ Return the first vertex that matches element. """
        for v in self._structure:
            if v.element() == element:
                return v
        return None

    def edges(self):
        """ Return a list of all edges in the graph. """
        edgelist = []
        for v in self._structure:
            for w in self._structure[v]:
                # to avoid duplicates, only return out edges
                if self._structure[v][w].start() == v:
                    edgelist.append(self._structure[v][w])
        return edgelist

    def get_edges(self, v):
        """ Return a list of all (out) edges incident on v. """
        return self.get_outedges(v)

    def get_outedges(self, v):
        """ Return a list of all out edges from v. """
        if v in self._structure:
            edgelist = []
            for w in self._structure[v]:
                edgelist.append(self._structure[v][w])
            return edgelist
        return None

    def get_inedges(self, v):
        """ Return a list of all edges into v. """
        if v in self._structure:
            edgelist = []
            for w in self._inedges[v]:
                edgelist.append(self._inedges[v][w])
            return edgelist
        return None

    def get_edge(self, v, w):
        """ Return the edge from v to w, or None. """
        if (self._structure is not None
                and v in self._structure
                and w in self._structure[v]):
            return self._structure[v][w]
        return None

    def degree(self, v):
        """ Return the (out) degree of vertex v. """
        return self.out_degree(v)

    def out_degree(self, v):
        """ Return the out_degree of vertex v. """
        return len(self._structure[v])

    def in_degree(self, v):
        """ Return the in_degree of vertex v. """
        return len(self._inedges[v])

    # -------------------------------------------------- #
    # ADT methods to modify the graph

    def add_vertex(self, element):
        """ Add a new vertex with data element.

        If there is already a vertex with the same data element,
        this will create another vertex instance.
        """
        v = Vertex(element)
        self._structure[v] = dict()
        self._inedges[v] = dict()
        return v

    def add_vertex_if_new(self, element):
        """ Add and return a vertex with element, if not already in graph.

        Checks for equality between the elements. If there is special
        meaning to parts of the element (e.g. element is a tuple, with an
        'id' in cell 0), then this method may create multiple vertices with
        the same 'id' if any other parts of element are different.

        To ensure vertices are unique for individual parts of element,
        separate methods need to be written.
        """
        for v in self._structure:
            if v.element() == element:
                return v
        return self.add_vertex(element)

    def add_edge(self, v, w, element):
        """ Add and return an edge between two vertices v and w, with  element.

        If either v or w are not vertices in the graph, does not add, and
        returns None.
            
        If an edge already exists between v and w, this will
        replace the previous edge.
        """
        if not v in self._structure or not w in self._structure:
            return None
        e = Edge(v, w, element)
        self._structure[v][w] = e
        self._inedges[w][v] = e
        return e

    def add_edge_pairs(self, elist):
        """ add all vertex pairs in elist as edges with empty elements. """
        for (v, w) in elist:
            self.add_edge(v, w, None)

    # -------------------------------------------------- #
    # Additional methods to explore the graph

    def highest_degreevertex(self):
        """ Return the vertex with highest degree. """
        hd = -1
        hdv = None
        for v in self._structure:
            if self.degree(v) > hd:
                hd = self.degree(v)
                hdv = v
        return hdv

    def highest_in_degreevertex(self):
        """ Return the vertex with highest in-degree. """
        hd = -1
        hdv = None
        for v in self._inedges:
            if self.in_degree(v) > hd:
                hd = self.in_degree(v)
                hdv = v
        return hdv

    def highest_out_degreevertex(self):
        """ Return the vertex with highest out-degree. """
        return self.highest_degreevertex()

    def dfs_stack(self, v):
        """ Return a DFS tree from v, using a stack.

        Corrected version (23/03/2020)
        """
        marked = {}
        stack = Stack()
        stack.push((v, None))
        # print('   pushed', v, 'from None')
        while stack.length() > 0:
            (vertex, edge) = stack.pop()
            if vertex not in marked:
                # print('popped unvisited', vertex)
                marked[vertex] = edge
                for e in self.get_edges(vertex):
                    w = e.opposite(vertex)
                    stack.push((w, e))
                    # print('   pushed', w, 'from', e)
        return marked

    def depthfirstsearch(self, v):
        """ Return a DFS tree from v. """
        marked = {v: None}
        self._depthfirstsearch(v, marked)
        return marked

    def _depthfirstsearch(self, v, marked):
        """ Do a DFS from v, storing nodes in marked. """
        for e in self.get_edges(v):
            w = e.opposite(v)
            if w not in marked:
                marked[w] = e
                self._depthfirstsearch(w, marked)

    def breadthfirstsearch(self, v):
        """ Return a BFS tree from v. """
        marked = {v: None}
        level = [v]
        while len(level) > 0:
            nextlevel = []
            for w in level:
                for e in self.get_edges(w):
                    x = e.opposite(w)
                    if x not in marked:
                        marked[x] = e
                        nextlevel.append(x)
            level = nextlevel
        return marked

    def BFS_length(self, v):
        """ Return a BFS tree from v, with path lengths. """
        marked = {v: (None, 0)}
        # dic values: tuple of parent vertex and level number of the key
        level = [v]
        levelint = 1
        while len(level) > 0:
            nextlevel = []
            for w in level:
                for e in self.get_edges(w):
                    x = e.opposite(w)
                    if x not in marked:
                        marked[x] = (w, levelint)
                        nextlevel.append(x)
            level = nextlevel
            levelint += 1
        return marked

    def breadthfirstsearchtree(self, v):
        """ Return a down-directed BFS tree from v. """
        marked = {v: []}
        level = [v]
        while len(level) > 0:
            nextlevel = []
            for w in level:
                for e in self.get_edges(w):
                    x = e.opposite(w)
                    if x not in marked:
                        marked[x] = []
                        marked[w].append(x)
                        nextlevel.append(x)
            level = nextlevel
        return marked

    def transitiveclosure(self):
        """ Return the transitive closure using version of FloydWarshall. """
        gstar = copy.deepcopy(self)
        vs = gstar.vertices()
        n = len(vs)
        for k in range(n):
            for i in range(n):
                if i != k and gstar.get_edge(vs[i], vs[k]) is not None:
                    for j in range(n):
                        if (i != j and k != j
                                and gstar.get_edge(vs[k], vs[j]) is not None):
                            if gstar.get_edge(vs[i], vs[j]) is None:
                                gstar.add_edge(vs[i], vs[j], 1)
        return gstar

    """ any vertex that has no in-edges, or only has in-edges from vertices
           already added to the sort, can go next in the sort
    so:
    get a list of all vertices with 0 degree, and pick one
    check the vertices it points to.
    If any of them now have no more inedges, add them to the list
    pick another vertex from the list and repeat

    How can we check whether or not a vertex has 0 in-edges from non tsort vertices?
    - record the in-degree of each vertex
    - each time we add a vertex into tsort, go to each of its opposites,
             and decrement their in-edge count
    - when a vertex count reduces to 0, add it to the list of available vertices
    """

    def topological_sort(self):
        """ Return a list of the vertices of the graph in topological sort order.

            If the graph is not a DAG, return None.
        """
        inedgecount = {}  # map of v:id, where id is the number of inedges in
        # for v from vertices not in tsort
        tsort = []  # t-sorted list of vertices
        available = []  # list of vertices with no in-edges left from non tsort

        # initialise the inedgecount map
        for v in self._structure:
            v_incount = self.in_degree(v)
            inedgecount[v] = v_incount
            if v_incount == 0:
                available.append(v)

        # repeat: take next available vertex, and append to tsort; update
        while len(available) > 0:
            w = available.pop()
            tsort.append(w)
            for e in self.get_edges(w):
                u = e.opposite(w)
                inedgecount[u] -= 1
                if inedgecount[u] == 0:
                    available.append(u)

        # if tsort is not same length as num_vertices, return None
        if len(tsort) == self.num_vertices():
            return tsort
        else:
            return None

    # End of class definition


# ---------------------------------------------------------------------------#
# Test methods

def test_tsort():
    graph = DirectedGraph()
    a = graph.add_vertex('a')
    b = graph.add_vertex('b')
    c = graph.add_vertex('c')
    d = graph.add_vertex('d')
    e = graph.add_vertex('e')
    f = graph.add_vertex('f')
    ##    a --> b -->d
    ##    c --/  \-->e
    ##     \--f----/
    eab = graph.add_edge(a, b, 1)
    ebd = graph.add_edge(b, d, 1)
    ecb = graph.add_edge(c, b, 1)
    ebe = graph.add_edge(b, e, 1)
    ecf = graph.add_edge(c, f, 1)
    efe = graph.add_edge(f, e, 1)

    tsort = graph.topological_sort()
    for v in tsort:
        print(v, '- ', end='')


def test_graph():
    """ Test on a simple 3-vertex, 2-edge graph. """
    graph = DirectedGraph()
    a = graph.add_vertex('a')
    b = graph.add_vertex('b')
    c = graph.add_vertex('c')
    d = graph.add_vertex_if_new('b')  # should not create a vertex
    eab = graph.add_edge(a, b, 2)
    ebc = graph.add_edge(b, c, 9)

    vnone = Vertex('dummy')
    evnone = graph.add_edge(vnone, c, 0)  # should not create an edge
    if evnone is not None:
        print('ERROR: attempted edges  should have been none')

    edges = graph.get_edges(vnone)  # should be None: vnone not in graph
    if edges != None:
        print('ERROR: returned edges for non-existent vertex.')

    print('number of vertices:', graph.num_vertices())
    print('number of edges:', graph.num_edges())

    print('Vertex list should be a,b,c in any order :')
    vertices = graph.vertices()
    for key in vertices:
        print(key.element())
    print('Edge list should be (a,b,2),(b,c,9) in any order :')
    edges = graph.edges()
    for edge in edges:
        print(edge)

    print('Graph display should repeat the above:')
    print(graph)

    v = graph.add_vertex('d')
    edges = graph.get_edges(v)
    if edges != []:
        print('ERROR: should have returned an empty list, but got', edges)
    print('Graph should now have a new vertex d with no edges')
    print(graph)

    print('DFS tree from a:')
    vlist = graph.depthfirstsearch(a)
    for key in vlist:
        print(key, vlist[key])
    print('DFS tree from b:')
    vlist = graph.depthfirstsearch(b)
    for key in vlist:
        print(key, vlist[key])


def get_path(v, tree):
    """ Extract a path from root to v, from backwards search tree. """
    s = Stack()
    s.push(v)
    _get_path(v, tree, s)
    return s


def _get_path(v, tree, stack):
    """ Extract a path from root to v in tree, and add to stack. """
    previous = tree[v][0]
    if previous != None:
        stack.push(previous)
        _get_path(previous, tree, stack)


def test_graph2():
    """ Test Graph with the standard 6-vertex graph from lectures.

        Graph has been transformed into a directed graph;
        a->b, b->a, b->d, b->em c->a, c->b, f->c, f->e
    """

    graph = DirectedGraph()
    a = graph.add_vertex('a')
    b = graph.add_vertex('b')
    c = graph.add_vertex('c')
    d = graph.add_vertex('d')
    e = graph.add_vertex('e')
    f = graph.add_vertex('f')
    graph.add_edge(a, b, 1)
    graph.add_edge(b, a, 1)
    graph.add_edge(c, a, 1)
    graph.add_edge(c, b, 1)
    graph.add_edge(b, d, 1)
    graph.add_edge(b, e, 1)
    graph.add_edge(f, c, 1)
    graph.add_edge(f, e, 1)

    # DFS from a, print the search tree (as a map)
    print('DFS from a:')
    vlist = graph.depthfirstsearch(a)
    for key in vlist:
        print(key, vlist[key])

    # Obtain transitive closure, print the edges
    print('Transitive closure:')
    closure = graph.transitiveclosure()
    edges = closure.edges()
    for e in edges:
        print(e)

    # BFS, augmenting search tree with path lengths, print the paths
    print('BFS from a:')
    tree = graph.BFS_length(a)
    for v in tree:
        path = get_path(v, tree)
        print(v, '(', end='')
        while path.length() > 0:
            print(path.pop(), '', end='')
        print('):', tree[v][1])
    # Now find the deepest node
    furthest = a
    maxlength = 0
    for v in tree:
        if tree[v][1] > maxlength:
            furthest = v
            maxlength = tree[v][1]
    print('The max length from a was', maxlength, 'to', furthest)


def test_graph3():
    graph = DirectedGraph()
    a = graph.add_vertex('a')
    b = graph.add_vertex('b')
    c = graph.add_vertex('c')
    d = graph.add_vertex('d')
    e = graph.add_vertex('e')
    f = graph.add_vertex('f')
    g = graph.add_vertex('g')
    h = graph.add_vertex('h')
    i = graph.add_vertex('i')
    j = graph.add_vertex('j')
    k = graph.add_vertex('k')
    l = graph.add_vertex('l')
    m = graph.add_vertex('m')
    graph.add_edge(a, b, 1)
    graph.add_edge(a, e, 1)
    graph.add_edge(a, h, 1)
    graph.add_edge(b, c, 1)
    graph.add_edge(b, e, 1)
    graph.add_edge(c, d, 1)
    graph.add_edge(c, g, 1)
    graph.add_edge(d, f, 1)
    graph.add_edge(e, f, 1)
    graph.add_edge(e, k, 1)
    graph.add_edge(f, i, 1)
    graph.add_edge(g, j, 1)
    graph.add_edge(h, m, 1)
    graph.add_edge(i, j, 1)
    graph.add_edge(i, k, 1)
    graph.add_edge(j, l, 1)
    graph.add_edge(k, l, 1)
    graph.add_edge(k, m, 1)

    print('DFS from a:')
    vlist = graph.depthfirstsearch(c)
    for key in vlist:
        print(key, vlist[key])


# test_graph3()
# print('now running on a smaller graph')
# test_graph2()

test_tsort()
