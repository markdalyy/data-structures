# Doubly Linked List

class DLLNode:
    def __init__(self, prev_node, item, next_node):
        self.prev = prev_node
        self.element = item
        self.next = next_node


class DLinkedList:
    def __init__(self):
        self.head = DLLNode(None, None, None)  # next is actually undefined self.tail
        self.tail = DLLNode(self.head, None, None)
        self.head.next = self.tail  # now we can complete the link
        self.size = 0

    def __str__(self):
        node = self.head.next
        if node is None:
            return '[]'
        # elements = [node]
        # while node.next != self.tail:
        #     elements.append(node.next.element)
        #     node = node.next
        # return '-'.join(elements)
        string = str(node.element)
        while node.next != self.tail:
            string += '-' + str(node.next.element)
            node = node.next
        return string

    def add_first(self, item):
        """ add at front of list """
        node = DLLNode(self.head, item, self.head.next)
        self.add_node(node)

    def add_after(self, prev_node, element):
        """ add after the given node """
        node = DLLNode(prev_node, element, prev_node.next)
        self.add_node(node)

    def add_last(self, element):
        """ add at end of list """
        node = DLLNode(self.tail.prev, element, self.tail)
        self.add_node(node)

    def add_node(self, node):
        node.next.prev = node
        node.prev.next = node
        self.size += 1

    def remove_first(self):
        """ remove the first element """
        if self.size == 0:
            return None
        item = self.head.next.element
        # fix two broken links after removing node
        self.head.next = self.head.next.next
        self.head.next.prev = self.head
        self.size -= 1
        return item

    def remove_last(self):
        """ remove the last element """
        if self.size == 0:
            return None
        item = self.tail.prev.element
        # fix two broken links after removing node
        self.tail.prev = self.tail.prev.prev
        self.tail.prev.next = self.tail
        self.size -= 1
        return item

    def delete_node(self, key):
        """ delete first occurrence of key in linked list """
        if self.size == 0:
            return None

        # Search for key
        node = self.head.next
        while node != self.tail:
            if node.element == key:
                break
            node = node.next

        # if key wasn't in linked list
        if node == self.tail:
            return None

        # fix two broken links after removing node
        node.next.prev = node.prev
        node.prev.next = node.next
        node = None  # delete node
        self.size -= 1

    def get_first(self):
        """ report the first element """
        if self.size == 0:
            return None
        return self.head.next.element

    def get_last(self):
        """ report the last element - now O(1) with tail reference """
        if self.size == 0:
            return None
        return self.tail.prev.element

    def length(self):
        """ report the number of elements """
        return self.size
