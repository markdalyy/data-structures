""" Class definitions for implementation of the Queue ADT.

    Includes inefficient versions
"""

import time
import sys

class QueueV0:
    """ A queue using a python list, with the head at the front.

    """
    def __init__(self):
        self.body = []
        
    def __str__(self):
        if len(self.body) == 0:
            return '<--<'
        stringlist = ['<']
        for item in self.body:
            stringlist.append('-' + str(item))
        stringlist.append('-<')
        return ''.join(stringlist)
        # output = '<-'
        # i = 0
        # for item in self.body:
        #     output = output + str(item) + '-'
        # output = output +'<'
        # return output

    def summary(self):
        """ Return a string summary of the queue. """
        return ('length:' + str(len(self.body)))
    
    def get_size(self):
        """ Return the internal size of the queue. """
        return sys.getsizeof(self.body)

    def enqueue(self, item):
        """ Add an item to the queue.

        Args:
            item - (any type) to be added to the queue.
        """
        self.body.append(item)

    def dequeue(self):
        """ Return (and remove) the item in the queue for longest. """
        return self.body.pop(0)

    def length(self):
        """ Return the number of items in the queue. """
        return len(self.body)

    def first(self):
        """ Return the first item in the queue. """
        return self.body[0]




class QueueV1:
    """ A queue using a python list, with an internal head pointer.

    End of the list is the end of the queue.
    """
    def __init__(self):
        self.body = []
        self.head = 0

    def __str__(self):
        output = '<-'
        i = self.head
        while i < len(self.body):
            output = output + str(self.body[i]) + '-'
            i = i+1
        output = output +'<'
        output = output + '     ' + self.summary()
        return output

    def summary(self):
        """ Return a string summary of the queue. """
        return ('Head:' + str(self.head)
               + '; length:' + str(len(self.body) - self.head))

    def get_size(self):
        """ Return the internal size of the queue. """
        return sys.getsizeof(self.body)

    def enqueue(self, item):
        """ Add an item to the queue.

        Args:
            item - (any type) to be added to the queue.
        """
        self.body.append(item)

    def dequeue(self):
        """ Return (and remove) the item in the queue for longest. """
        item = self.body[self.head]
        self.body[self.head] = None
        self.head = self.head + 1
        return item

    def length(self):
        """ Return the number of items in the queue. """
        return len(self.body) - self.head

    def first(self):
        """ Return the first item in the queue. """
        return self.body[self.head]


class QueueV2:
    """ A queue using a python list, with internal wrap-around..

    Head and tail of the queue are maintained by internal pointers.
    When the list is full, a new bigger list is created.
    """
    def __init__(self):
        self.body = [None] * 10
        self.head = 0    #index of first element, but 0 if empty
        self.tail = 0    #index of free cell for next element
        self.size = 0    #number of elements in the queue

    def __str__(self):
        output = '<-'
        i = self.head
        if self.head < self.tail:
            while i < self.tail:
                output = output + str(self.body[i]) + '-'
                i = i+1
        else:
            while i < len(self.body):
                output = output + str(self.body[i]) + '-'
                i = i+1
            i = 0
            while i < self.tail:
                output = output + str(self.body[i]) + '-'
                i = i+1
        output = output +'<'
        output = output + '     ' + self.summary()
        return output

    def get_size(self):
        """ Return the internal size of the queue. """
        return sys.getsizeof(self.body)

    def summary(self):
        """ Return a string summary of the queue. """
        return ('Head:' + str(self.head)
               + '; tail:' +  str(self.tail)
               + '; size:' + str(self.size))
        
    def grow(self):
        """ Grow the internal representation of the queue.

        This should not be called externally.
        """
        # print('growing')
        # print('Before growing:')
        # print(self)
        oldbody = self.body
        self.body = [None] * (2*self.size)
        oldpos = self.head
        pos = 0
        if self.head < self.tail:     #data is not wrapped around in list
            while oldpos <= self.tail:
                self.body[pos] = oldbody[oldpos]
                oldbody[oldpos] = None           
                pos = pos + 1
                oldpos = oldpos + 1
        else:                         #data is wrapped around
            while oldpos < len(oldbody):
                self.body[pos] = oldbody[oldpos]
                oldbody[oldpos] = None           
                pos = pos + 1
                oldpos = oldpos + 1
            oldpos = 0
            while oldpos <= self.tail:
                self.body[pos] = oldbody[oldpos]
                oldbody[oldpos] = None
                pos = pos + 1
                oldpos = oldpos + 1
        self.head = 0
        self.tail = self.size 
         

    def enqueue(self,item):
        """ Add an item to the queue.

        Args:
            item - (any type) to be added to the queue.
        """
        #An improved representation would use modular arithmetic
        if self.size == 0:
            self.body[0] = item      #assumes an empty queue has head at 0
            self.size = 1
            self.tail = 1
        else:
            self.body[self.tail] = item
            # print('self.tail =', self.tail, ': ', self.body[self.tail])
            self.size = self.size + 1
            if self.size == len(self.body):  #list is now full
                self.grow()                  #so grow it ready for next enqueue
            elif self.tail == len(self.body)-1:  #no room at end, but must be at front
                self.tail = 0
            else:
                self.tail = self.tail + 1
        #print(self)

    def dequeue(self):
        """ Return (and remove) the item in the queue for longest. """
        #An improved implementation would use modular arithmetic
        if self.size == 0:     #empty queue
            return None
        item = self.body[self.head]
        self.body[self.head] = None
        if self.size == 1:  #just removed last element, so rebalance
            self.head = 0
            self.tail = 0
            self.size = 0
        elif self.head == len(self.body) - 1:  #if head was the end of the list
            self.head = 0  #we must have wrapped round, so point to start
            self.size = self.size - 1
        else:            
            self.head = self.head + 1  #just move the pointer on one cell
            self.size = self.size - 1
        #we haven't changed the tail, so nothing to do
        return item

    def length(self):
        """ Return the number of items in the queue. """
        return self.size

    def first(self):
        """ Return the first item in the queue. """
        return self.body[self.head]      # will return None if queue is empty

