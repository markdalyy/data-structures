# Singly Linked List

class SLLNode:
    def __init__(self, item, nextnode):
        self.element = item      # any object
        self.next = nextnode     # an SLLNode


class SLinkedList:
    def __init__(self):
        self.first = None        # an SLLNode
        self.size = 0            # an integer

    def __str__(self):
        node = self.first
        if node is None:
            return '[]'
        elements = []
        while node:
            elements.append(node.element)
            node = node.next
        return '->'.join(elements)

    def add_first(self, element):
        """ add at front of list """
        node = SLLNode(element, self.first)
        self.first = node
        self.size += 1

    def remove_first(self):
        """ remove the first element """
        if self.size == 0:
            return None
        item = self.first.element
        self.first = self.first.next
        self.size -= 1
        return item

    def add_after(self, prev_node, element):
        """ add after the given node """
        node = SLLNode(element, prev_node.next)
        prev_node.next = node
        self.size += 1

    def add_last(self, element):
        """ add at end of list """
        new_node = SLLNode(element, None)
        node = self.first
        if node is None:
            self.first = new_node
        else:
            while node.next:
                node = node.next
            node.next = new_node
        self.size += 1

    def remove_last(self):
        """ remove the last element """
        node = self.first

        if node is None:  # empty
            return None

        if node.next is None:  # remove first
            item = node.element
            self.first = None
            return item

        # Continue to last and keep track of previous node
        prev = None
        while node.next is not None:
            prev = node
            node = node.next

        item = node.element
        prev.next = None  # Fix broken link
        node = None  # delete node
        self.size -= 1

        return item

    def delete_node(self, key):
        """ delete first occurrence of key in linked list """
        node = self.first

        if node is not None:
            if node.element == key:
                self.first = node.next
                self.size -= 1
                return

        # Search for key and keep track of previous node
        prev = None
        while node is not None:
            if node.element == key:
                break
            prev = node
            node = node.next

        # if key wasn't in linked list
        if node is None:
            return

        # Fix broken link
        prev.next = node.next
        node = None  # delete node
        self.size -= 1

    def get_first(self):
        """ report the first element """
        if self.size == 0:
            return None
        return self.first.element

    def get_last(self):
        """ report the last element """
        if self.size == 0:
            return None
        node = self.first
        while node.next:
            node = node.next
        return node.element

    def length(self):
        """ report the number of elements """
        return self.size
