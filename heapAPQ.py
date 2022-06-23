"""
An APQ is an adaptable collection of objects where the item with the highest priority is removed next
adaptable meaning the priority of objects can change, or any object can be removed
Objects are stored with three pieces of data:
    the value, representing the original item
    the key, representing its priority
    the index, representing its position in the APQ which enables constant access
"""


class Element:
    """ A key, value and index. """

    def __init__(self, k, v, i):
        self._key = k
        self._value = v
        self._index = i

    def __str__(self):
        """ Return a short string representation of this element. """
        outstr = str(self._key)
        return outstr

    def full_str(self):
        """ Return a full string representation of this element. """
        outstr = str(self._key) + ": "
        outstr = outstr + str(self._value) + "; "
        outstr = outstr + str(self._index)
        return outstr

    def __eq__(self, other):
        return self._key == other._key

    def __lt__(self, other):
        return self._key < other._key

    def _wipe(self):
        self._key = None
        self._value = None
        self._index = None

class Heap_APQ:
    """ APQ implemented as an array-based representation of a Binary Heap
    Root node is at index 0
    Next item to be added is at index size.
    Last item is at index size-1
    """
    def __init__(self):
        self._body = []
        self._size = 0

    def __str__(self):
        if self._size == 0:
            return '<--<'
        keys = []
        for i in range(self._size):
            keys.append(str(self._body[i]))
        return '[' + ', '.join(keys) + ']'

    def add(self, k, v):
        """ Add a new item into the APQ with priority key, and return its Element in the APQ
                Add element in last position
                Update heap size
                Bubble element up heap
                Return element
        """
        e = Element(k, v, self._size)
        # self._body[self._size] = e
        self._body.append(e)
        self._size += 1
        self.bubbleup(self._size - 1)
        return e

    def bubbleup(self, i):
        """ Bubble up item currently in pos i in a min heap. """
        while i > 0:
            parent = (i - 1) // 2
            if self._body[i] < self._body[parent]:
                self._body[i], self._body[parent] = self._body[parent], self._body[i]
                # NOTE: Whenever we swap two elements in the heap
                # we must update the _index attributes in the Elements.
                self._body[i]._index = i
                self._body[parent]._index = parent
                i = parent
            else:
                i = 0

    def bubbledown(self, i, last):
        """ Bubble down item currently in pos i in a min heap. """
        while last > (i * 2):  # so at least one child
            lc = i * 2 + 1
            rc = i * 2 + 2
            minc = lc  # start by assuming left child is the min child
            if last > lc and self._body[rc] < self._body[lc]:  # rc exists and is smaller
                minc = rc
            if self._body[i] > self._body[minc]:
                self._body[i], self._body[minc] = self._body[minc], self._body[i]
                # NOTE: Whenever we swap two elements in the heap
                # we must update the _index attributes in the Elements.
                self._body[i]._index = i
                self._body[minc]._index = minc
                i = minc
            else:
                i = last

    def min(self):
        """Return the value with the minimum key"""
        min = self._body[0]
        return min._value, min._key

    def remove_min(self):
        """ Remove and return the value with the min key
                Extract the root value
                Copy the last element into the root
                Remove last
                Update size
                Bubble root element down
        """
        if self._size == 0:  # empty queue
            return None
        min = self._body[0]
        minv, mink = min._value, min._key
        self._body[0] = self._body[self._size - 1]
        self._body.pop()
        self._size -= 1
        if self._size == 0:
            return minv, mink
        # else we just swapped two elements in the heap
        # we must update the _index attributes in the Elements.
        self._body[0]._index = 0
        self.bubbledown(0, self._size - 1)
        return minv, mink

    def is_empty(self):
        """return True if no items in the priority queue"""
        if self._size == 0:
            return True
        return False

    def length(self):
        """return the number of items in the priority queue"""
        return self._size

    def update_key(self, element, newkey):
        """update the key in element to be newkey, and rebalance the APQ"""
        element._key = newkey
        self.bubbleup(element._index)
        self.bubbledown(element._index, self._size - 1)
        # this will bubble up the element if parent key is greater than new key
        # else it will bubble down the element

    def get_key(self, element):
        """return the current key for element"""
        return element._key

    def remove(self, element):
        """ Remove the element from the APQ, and rebalance APQ
                Extract the elements value
                Copy the last element into its place
                Remove last
                Update size
                Bubble copied element up or down
        """
        if self._size == 0:  # empty queue
            return None
        v, k = element._value, element._key
        index = element._index
        self._body[index] = self._body[self._size - 1]
        self._body.pop()
        self._size -= 1
        if self._size == 0:
            return v, k
        # else we just swapped two elements in the heap
        # we must update the _index attributes in the Elements.
        self._body[index]._index = index
        self.bubbleup(index)
        self.bubbledown(index, self._size - 1)
        return v, k