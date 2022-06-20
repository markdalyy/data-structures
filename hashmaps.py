class Element:
    """ Represents an element with a key and value. """

    def __init__(self, k, v):
        """ Create an element with given key k and value v.

            The key must be an immutable type.
        """
        self._key = k
        self._value = v

    def __eq__(self, other):
        """ Return True if this element's key equals other's key. """
        return self._key == other._key

    def __lt__(self, other):
        """ Return True if this element's key is less than other's key. """
        return self._key < other._key

    def _wipe(self):
        """ Set the instance variables to None. """
        self._key = None
        self._value = None


class HashMapV1:
    """ An implementation of a simple Hash Map.

        Maintains a fixed length list of positions, and each position stores a
        list of elements.
    """

    def __init__(self, sz):
        """ Create an empty Hash Map with size sz. """
        if sz < 0:
            sz = 10  # sz is the number of cells in the list
        self._map = [None] * sz  # the container for the elements
        self._size = 0  # the number of elements in the map

    def __str__(self):
        """ Represent the Map as a string. """
        outstr = ''
        for alist in self._map:
            if alist is not None:
                for elt in alist:
                    outstr += '(' + str(self._hashvalue(elt._key)) + ') '
                    outstr += str(elt._key) + ' : ' + str(elt._value) + '\n'
        return outstr

    def getitem(self, key):
        """ Return the value with a given key, or None if key not in Map. """
        hv = self._hashvalue(key)
        if self._map[hv]:  # if the bucket at hv exists
            for elt in self._map[hv]:
                if elt._key == key:
                    return elt._value
        return None

    def setitem(self, key, value):
        """ Assign value to elt with key; create new elt if needed. """

        hv = self._hashvalue(key)
        # if the bucket at hv exists
        if self._map[hv]:
            pos = 0
            found = False
            while not found and pos < len(self._map[hv]):
                if self._map[hv][pos]._key == key:
                    self._map[hv][pos]._value = value
                    found = True
                pos += 1
            if not found:
                self._size += 1
                self._map[hv].append(Element(key, value))
        else:  # else create the bucket and add the new element
            self._map[hv] = [Element(key, value)]
            self._size += 1

    def contains(self, key):
        """ Return True if there is an elt with key in this map. """
        hv = self._hashvalue(key)
        if self._map[hv]:  # if the bucket at hv exists
            return self._bucketcontains(self._map[hv], key)
        return False

    def delitem(self, key):
        """ Remove element and return value of elt with key if exists.

            Returns None if no such elt is in Map.
        """
        hv = self._hashvalue(key)
        if self._map[hv]:  # if the bucket at hv exists
            for i in range(len(self._map[hv])):
                if self._map[hv][i]._key == key:
                    val = self._map[hv][i]._value
                    self._size -= 1
                    self._map[hv].pop(i)
                    return val
        return None

    def length(self):
        """ Return the number of items in the map. """
        return self._size

    def _hashvalue(self, ph):
        """ Turn an immutable type into a location in this hash map. """
        return hash(ph) % len(self._map)

    def _bucketcontains(self, bucket, key):
        """ Return True if bucket contains element with key. """
        for elt in bucket:
            if elt._key == key:
                return True
        return False


class HashMapV2:
    """ An implementation of a simple Hash Map.

        Maintains a variable-length list of positions, and each position
        stores a list of elements.
    """

    def __init__(self, sz):
        """ Create an empty Hash Map with size sz. """
        if sz < 0:
            sz = 10  # sz will be the initial number of cells
        self._map = [None] * sz
        self._size = 0  # the number of elements in the map

    def __str__(self):
        """ Represent the Map as a string. """
        outstr = 'size: ' + str(self._size)
        outstr += '; space: ' + str(len(self._map)) + '\n'
        for alist in self._map:
            if alist:
                for elt in alist:
                    outstr += '(' + str(self._hashvalue(elt._key)) + ') '
                    outstr += str(elt._key) + ' : ' + str(elt._value) + '\n'
        return outstr

    def _hashvalue(self, ph):
        """ Turn an immutable type into a location in this hash map. """
        return hash(ph) % len(self._map)

    def getitem(self, key):
        """ Return the value with a given key, or None if key not in Map. """
        hv = self._hashvalue(key)
        if self._map[hv]:  # if the bucket at hv exists
            for elt in self._map[hv]:
                if elt._key == key:
                    return elt._value
        return None

    def _resize(self, factor):
        """ Create a new list map, with size = factor * original size. """
        # Next three lines for testing / debugging only
        print('RESIZING: size =', self._size, '; space = ', len(self._map))
        print('Current map:')
        print(self)
        oldmap = self._map  # take a copy of the list
        self._map = [None] * len(oldmap) * factor  # create the new list
        for alist in oldmap:  # now rehash and copy all elements
            if alist:  # if this bucket exists
                # could just call self._setitem, but that would search for
                # duplicate before adding, and we know there are none
                for oldelt in alist:
                    hv = self._hashvalue(oldelt._key)  # rehash
                    if self._map[hv]:  # if new bucket already exists
                        self._map[hv].append(oldelt)
                    else:
                        self._map[hv] = [oldelt]
        print('\nNew map')
        print(self)

    def _bucketcontains(self, bucket, key):
        """ Return True if bucket contains element with key. """
        for elt in bucket:
            if elt._key == key:
                return True
        return False

    def setitem(self, key, value):
        """ Assign value to elt with key; create new elt if needed. """
        hv = self._hashvalue(key)
        # if the bucket at hv exists
        if self._map[hv]:
            pos = 0
            found = False
            while not found and pos < len(self._map[hv]):
                if self._map[hv][pos]._key == key:
                    self._map[hv][pos]._value = value
                    found = True
                pos += 1
            if not found:
                self._size += 1
                self._map[hv].append(Element(key, value))
        else:  # else create the bucket and add the new element
            self._map[hv] = [Element(key, value)]
            self._size += 1
        # if the load factor is too high (too many elements in map), resize
        if self._size / len(self._map) > 0.5:
            self._resize(2)

    def contains(self, key):
        """ Return True if there is an elt with key in this map. """
        hv = self._hashvalue(key)
        if self._map[hv]:  # if bucket at hv exists
            return self._bucketcontains(self._map[hv], key)
        return False

    def delitem(self, key):
        """ Remove element and return value of elt with key if exists.

            Returns None if no such elt is in Map.
        """
        hv = self._hashvalue(key)
        if self._map[hv]:  # if bucket at hv exists
            for i in range(len(self._map[hv])):
                if self._map[hv][i]._key == key:
                    val = self._map[hv][i]._value
                    self._size -= 1
                    self._map[hv].pop(i)
                    return val
        return None

    def length(self):
        """ Return the number of items in the map. """
        return self._size

    def is_empty(self):
        """ Return True if the map is empty. """
        return self.length() == 0


class HashMapLP:
    """ An implementation of a simple Hash Map using Linear Probing.

        Maintains a variable-length list of positions.
        On collisions, search forward for the first free cell.
        On searching, must search to the next free cell
    """

    def __init__(self, sz):
        """ Create an empty Hash Map with size sz. """
        if sz < 0:
            sz = 10  # sz will be the initial number of cells
        self._map = [None] * sz
        self._size = 0  # the number of elements in the map

    def __str__(self):
        """ Represent the Map as a string. """
        outstr = 'size: ' + str(self._size)
        outstr += '; space: ' + str(len(self._map)) + '\n'
        for i in range(len(self._map)):
            if isinstance(self._map[i], Element):  # not None and != 0
                elt = self._map[i]
                outstr += '(' + str(self._hashvalue(elt._key)) + ') '
                outstr += '[' + str(i) + '] '
                outstr += str(elt._key) + ' : ' + str(elt._value) + '\n'
            elif self._map[i] == 0:
                outstr += '     [' + str(i) + '] available\n'
        return outstr

    def _hashvalue(self, ph):
        """ Turn an immutable type into a location in this hash map. """
        return hash(ph) % len(self._map)

    def getitem(self, key):
        """ Return the value with a given key, or None if key not in Map. """
        hv = self._hashvalue(key)
        oldhv = hv
        inblock = True
        while inblock:
            if self._map[hv] is None:  # reached an empty cell, so not there
                return None
            if isinstance(self._map[hv], Element):
                if self._map[hv]._key == key:
                    return self._map[hv]._value
            # must be either a different element, or an 'available' slot
            # so move on, and wrap round if necessary
            hv = (hv + 1) % len(self._map)  # wrap round list if necessary
            if hv == oldhv:  # wrapped round back to start
                inBlock = False
        return None

    def _resize(self, factor):
        """ Create a new list map, with size = factor * original size. """
        # Next three lines for testing / debugging only
        print('RESIZING: size =', self._size, '; space = ', len(self._map))
        print('Current map:')
        print(self)
        oldmap = self._map  # take a copy of the list
        self._map = [None] * len(oldmap) * factor  # create the new list
        self._size = 0
        for elt in oldmap:  # now rehash and copy all elements
            if isinstance(elt, Element):  # not None and !=0  # i.e. only copy cells with real elements
                self.setitem(elt._key, elt._value)
        print('\nNew map')
        print(self)

    def setitem(self, key, value):
        """ Assign value to elt with key; create new elt if needed. """
        pos = self._hashvalue(key)
        oldpos = pos  # to check if we have wrapped all way round
        inblock = True  # in the block of elts for this hash key
        found = False  # have we found this key?
        firstfree = None  # the first free or empty cell
        while inblock and not found:
            if self._map[pos] is None:  # reached end of block; will add here
                inblock = False
            elif not isinstance(self._map[pos], Element):  # == 0 # found a 'free' cell
                if firstfree == None:  # if it is the first, keep it
                    firstfree = pos
                pos = (pos + 1) % len(self._map)  # keep moving (key may be later)
            elif self._map[pos]._key == key:  # found our element
                found = True
            else:
                pos = (pos + 1) % len(self._map)  # keep moving
            if pos == oldpos:  # if wrapped all the way round
                inblock = False
        if found:
            self._map[pos]._value = value
        elif firstfree != None:  # didn't find it, but found free cell
            self._map[firstfree] = Element(key, value)
            self._size += 1
        else:  # add into the None cell which quit the loop
            self._map[pos] = Element(key, value)
            self._size += 1
        # if the load factor is too high (too many elements in map), resize
        if self._size / len(self._map) > 0.5:
            self._resize(2)

    def contains(self, key):
        """ Return True if there is an elt with key in this map. """
        hv = self._hashvalue(key)
        oldhv = hv
        inblock = True
        while inblock:
            if self._map[hv] is None:  # reached an empty cell, so not there
                return False
            if isinstance(self._map[hv], Element):
                if self._map[hv]._key == key:
                    return True
            # must be either a different element, or an 'availble' slot
            # so move on, and wrap round if necessary
            hv = (hv + 1) % len(self._map)  # wrap round list if necessary
            if hv == oldhv:  # wrapped round back to start
                inBlock = False
        return False

    def delitem(self, key):
        """ Remove element and return value of elt with key if exists.

            Returns None if no such elt is in Map.
        """
        hv = self._hashvalue(key)
        oldhv = hv
        inblock = True
        retvalue = None
        while inblock:
            if self._map[hv] is None:  # reached an empty cell, so not there
                return None
            if isinstance(self._map[hv], Element):
                if self._map[hv]._key == key:
                    retvalue = self._map[hv]._value
                    self._map[hv]._wipe()
                    self._map[hv] = 0
                    self._size -= 1
                    return retvalue
            # must be either a different element, or an 'available' slot
            # so move on, and wrap round if necessary
            hv = (hv + 1) % len(self._map)  # wrap round list if necessary
            if hv == oldhv:  # wrapped round back to start
                inBlock = False
        return None

    def length(self):
        """ Return the number of items in the map. """
        return self._size

    def is_empty(self):
        """ Return True if the map is empty. """
        return self.length() == 0


def test():
    mymap = HashMapLP(10)  # test other versions
    mymap.setitem('CS1106', 'Introduction to Relational Databases')
    mymap.setitem('CS1110', 'Systems Organisation I')
    mymap.setitem('CS1111', 'Systems Organisation II')
    mymap.setitem('CS1112', 'Foundations of Computer Science I')
    mymap.setitem('CS1113', 'Foundations of Computer Science II')
    mymap.setitem('CS1115', 'Web Development 1')
    mymap.setitem('CS1116', 'Web Development 2')
    mymap.setitem('CS1117', 'Introduction to Programming')
    mymap.setitem('CS2051', 'Introduction to Digital Media')
    mymap.setitem('CS2052', 'Introduction to Internet Information Systems')
    mymap.setitem('CS2501', 'Database Design and Administration')
    mymap.setitem('CS2502', 'Logic Design')
    mymap.setitem('CS2503', 'Operating Systems 1')
    mymap.setitem('CS2505', 'Network Computing')
    mymap.setitem('CS2506', 'Operating Systems II')
    mymap.setitem('CS2507', 'Computer Architecture')
    mymap.setitem('CS2508', 'Computer Animation')
    mymap.setitem('CS2509', 'XML and the Extended Enterprise')
    mymap.setitem('CS2510', 'Web Servers')
    mymap.setitem('CS2511', 'Usability Engineering')
    mymap.setitem('CS2512', 'Authoring')
    mymap.setitem('CS2513', 'Intermediate Programming')
    mymap.setitem('CS2514', 'Introduction to Java')
    mymap.setitem('CS2515', 'Algorithms and Data Structures I')
    mymap.setitem('CS2516', 'Algorithms and Data Structures II')
    print('Book of Modules for 1st and 2nd year Computer Science')
    print(mymap)
    print('CS BoM contains CS2515 (true)?', mymap.contains('CS2515'))
    print('CS BoM contains CS2504 (false)?', mymap.contains('CS2504'))
    print('CS2515 has title (A&DS I):', mymap.getitem('CS2515'))
    print('CS2504 has title (None):', mymap.getitem('CS2504'))
    print('Add new module CS2599 (None):', mymap.setitem('CS2599', 'Facebook'))
    print('CS BoM contains CS2599 (true)?', mymap.contains('CS2599'))
    print('CS2599 has title (Facebook):', mymap.getitem('CS2599'))
    print('Book of Modules for 1st and 2nd year Computer Science')
    print(mymap)
    print('Change title of CS2599 to Twitter (None):', mymap.setitem('CS2599', 'Twitter'))
    print('CS2599 has title (Twitter):', mymap.getitem('CS2599'))
    print('Removing CS113 (FoCSII):', mymap.delitem('CS1113'))
    print('CS BoM contains CS1113 (false)?', mymap.contains('CS1113'))
    print('Book of Modules for 1st and 2nd year Computer Science')
    print(mymap)


test()
