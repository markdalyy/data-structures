class BSTNode:
    """ An internal node for a Binary Search Tree.

    This gives a recursive definition of a BST, which consists of this node
    and all of its descendants. It allows us to implement recursive methods -
    e.g. to search a tree, we search at the root of the tree; if the element
    is there, we stop and return the value; if not, then we decide whether to
    go left or right, and then call the same search method on the appropriate
    child.

    Remember that if your recursive method ever returns anything, then it must
    return an appropriate value on every possible path through the method.
    """

    def __init__(self, item):
        """ Initialise a BSTNode on creation, with value==item. """
        self._element = item
        self._leftchild = None
        self._rightchild = None
        self._parent = None

    def __str__(self):
        """ Return a string representation of the tree rooted at this node.

        The string will be created by an in-order traversal.
        """
        outstr = ''
        if self._leftchild is not None:
            outstr = outstr + str(self._leftchild)
        outstr = outstr + ' / ' + str(self._element)
        if self._rightchild is not None:
            outstr = outstr + str(self._rightchild)
        return outstr

    def _stats(self):
        """ Return the basic stats on the tree. """
        return ('size = ' + str(self.size())
                + '; height = ' + str(self.height()))

    def search(self, searchitem):
        """ Return object matching searchitem if there, or None.

        Args:
            searchitem: an object of any class that could be stored in the BST.
        """
        node = self.search_node(searchitem)
        if node is not None:
            return node._element
        return None

    def search_node(self, searchitem):
        """ Return the BSTNode (with subtree) containing searchitem, or None.

        Args:
            searchitem: an object of any class that could be stored in the BST.
        """
        if self._element > searchitem:
            if self._leftchild is not None:
                return self._leftchild.search_node(searchitem)
            return None
        if self._element < searchitem:
            if self._rightchild is not None:
                return self._rightchild.search_node(searchitem)
            return None
        return self  # not < or >, so self._element must == searchitem
        #              relies on equality test, not identity

    def add(self, obj):
        """ Add item to the tree, maintaining BST properties.

        Note: if a matching object is already in the tree, this does nothing.
        """

        added = self._add_internal(obj)
        if added is not None:
            return added._element
        return None

    def _add_internal(self, obj):
        """ Add item to the tree, maintaining BST properties.

        Args:
            obj -- object of any class intended for this BST

        Returns: the BSTNode where the object was added, or None

        Note: if a matching object is already in the tree, this does nothing.
        """
        if self._element > obj:
            if self._leftchild is not None:
                return self._leftchild._add_internal(obj)
            self._leftchild = BSTNode(obj)  # if no child there, add obj
            self._leftchild._parent = self
            return self._leftchild
        if self._element < obj:
            if self._rightchild is not None:
                return self._rightchild._add_internal(obj)
            self._rightchild = BSTNode(obj)  # if no child there, add obj
            self._rightchild._parent = self
            return self._rightchild
        # so this node must have same object, so don't add
        return None

    def findmaxitem(self):
        """ Return the largest item in the BST rooted at this node. """
        return self.findmaxnode()._element

    def findmaxnode(self):
        """ Return the BSTNode with the maximal element at or below self. """
        if self._rightchild is not None:
            return self._rightchild.findmaxnode()
        return self

    def findminitem(self):
        """ Return the smallest item in the BST rooted at this node. """
        return self.findminnode()._element

    def findminnode(self):
        """ Return the BSTNode with the minimal element at or below self. """
        if self._leftchild is not None:
            return self._leftchild.findminnode()
        return self

    def height(self):
        """ Return the height of this node.

        Note that with the recursive definition of the tree the height of the
        node is the same as the depth of the tree rooted at this node.
        """
        if self._leftchild is not None:
            leftheight = self._leftchild.height() + 1
        else:
            leftheight = 0
        if self._rightchild is not None:
            rightheight = self._rightchild.height() + 1
        else:
            rightheight = 0
        return max(leftheight, rightheight)

    def size(self):
        """ Return the size of this subtree.

        The size is the number of nodes (or elements) in the tree.
        """
        leftsize = 0
        rightsize = 0
        if self._leftchild is not None:
            leftsize = self._leftchild.size()
        if self._rightchild is not None:
            rightsize = self._rightchild.size()
        return leftsize + rightsize + 1

    def leaf(self):
        """ Return True if this node has no children. """
        if self._leftchild is not None or self._rightchild is not None:
            return False
        return True

    def semileaf(self):
        """ Return True if this node has exactly one child. """
        if ((self._leftchild is not None and self._rightchild is None)
                or (self._rightchild is not None and self._leftchild is None)):
            return True
        return False

    def full(self):
        """ Return true if this node has two children. """
        return self._leftchild is not None and self._rightchild is not None

    def internal(self):
        """ Return True if this node has at least one child. """
        return not self.leaf()

    def remove(self, searchitem):
        """ Remove and return the object matching searchitem, if there.

        Args:
            searchitem - an object of any class that could be in BST.

        Remove the matching object from the tree rooted at this node.
        Maintains the BST properties.
        """
        node = self.search_node(searchitem)
        if node is None:
            return None
        else:
            return node._remove_node()

    def _remove_node(self):
        """ (Private) Remove this BSTBode from its tree, and return its element.

        Maintains the BST properties.
        """
        # if this is a full node
        # find the biggest item in the left tree
        #  - there must be a left tree, since this is a full node
        #  - the node for that item can have no right children
        # move that item up into this item
        # remove that old node, which is now a semileaf
        # return the original element
        # else if this has no children
        # find who the parent was
        # set the parent's appropriate child to None
        # wipe this node
        # return this node's element
        # else if this has no right child (but must have a left child)
        # shift leftchild up into its place, and clean up
        # return the original element
        # else this has no left child (but must have a right child)
        # shift rightchild up into its place, and clean up
        # return the original element
        if self.full():
            elt = self._element
            biggest = self._leftchild.findmaxnode()
            self._element = biggest._element
            biggest._remove_node()
            return elt
        elif self.leaf():
            elt = self._element
            if self._parent is not None:
                if self._parent._leftchild == self:
                    self._parent._leftchild = None
                else:
                    self._parent._rightchild = None
            self._element = None
            self._parent = None
            return elt
        elif self._rightchild is None:  # but must have left child
            elt = self._element
            self._pullup(self._leftchild)
            return elt
        else:  # self._leftchild is None, but must have right child
            elt = self._element
            self._pullup(self._rightchild)
            return elt

    def _pullup(self, node):
        """ Pull up the data from a child (subtree) node into this BSTNode.

            Note: rather than updates the links so that the child node takes
            the place of the removed semileaf, instead, we will copy the
            child's element into the semileaf, and then readjust the links, and
            then remove the now empty child node. This means that when we remove
            a root semileaf, the code that called the remove method still
            maintains a reference to the root of the tree, and so can continue
            processing the tree (otherwise, if we removed the actual BSTNode
            that was the root, the calling code would lose all reference to
            the tree).
        """
        self._element = node._element
        self._leftchild = node._leftchild
        if node._leftchild:
            node._leftchild._parent = self
        self._rightchild = node._rightchild
        if node._rightchild:
            node._rightchild._parent = self
        node._element = None
        node._parent = None
        node._leftchild = None
        node._rightchild = None

    def _print_structure(self):
        """ (Private) Print a structured representation of tree at this node. """
        if self._properBST() == False:
            print("ERROR: this is not a proper Binary Search Tree. ++++++++++")
        outstr = str(self._element) + ' (hgt=' + str(self.height()) + ')['
        if self._leftchild is not None:
            outstr = outstr + "left: " + str(self._leftchild._element)
        else:
            outstr = outstr + 'left: *'
        if self._rightchild is not None:
            outstr = outstr + "; right: " + str(self._rightchild._element) + ']'
        else:
            outstr = outstr + '; right: *]'
        if self._parent is not None:
            outstr = outstr + ' -- parent: ' + str(self._parent._element)
        else:
            outstr = outstr + ' -- parent: *'
        print(outstr)
        if self._leftchild is not None:
            self._leftchild._print_structure()
        if self._rightchild is not None:
            self._rightchild._print_structure()

    def _properBST(self):
        """ Return True if this is the root of a proper BST; False otherwise. """

        if not self._isthisapropertree():
            return False
        return self._BSTproperties()[0]

    def _BSTproperties(self):
        """ Return a tuple describing state of this node as root of a BST.

        Returns:
            (boolean, minvalue, maxvalue):
                boolean is True if it is a BST, and false otherwise
                minvalue is the lowest value in this subtree
                maxvalue is the highest value in this subtree
        """
        minvalue = self._element
        maxvalue = self._element
        if self._leftchild is not None:
            leftstate = self._leftchild._BSTproperties()
            if not leftstate[0] or leftstate[2] > self._element:
                return (False, None, None)
            minvalue = leftstate[1]

        if self._rightchild is not None:
            rightstate = self._rightchild._BSTproperties()
            if not rightstate[0] or rightstate[1] < self._element:
                return (False, None, None)
            maxvalue = rightstate[2]

        return (True, minvalue, maxvalue)

    def _isthisapropertree(self):
        """ Return True if this is a properly implemented tree; else False. """
        ok = True
        if self._leftchild is not None:
            if self._leftchild._parent != self:
                ok = False
            if self._leftchild._isthisapropertree() == False:
                ok = False
        if self._rightchild is not None:
            if self._rightchild._parent != self:
                ok = False
            if self._rightchild._isthisapropertree() == False:
                ok = False
        if self._parent is not None:
            if (self._parent._leftchild != self
                    and self._parent._rightchild != self):
                ok = False
        return ok
