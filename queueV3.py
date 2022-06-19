""" Functions to test Queue class.

Includes the modular arithmetic implementation of a queue.
"""

from stack import Stack
from queues import *


class QueueV3:
    """ Reasonably efficient implementation of the Queue ADT.

    Efficient enqueuing, and efficient space use.
    Uses modular arithmetic.
    (Should be the same performance as Queue() from queues.py)
    """
    def __init__(self):
        self.body = [None] * 10
        self.head = 0    # index of first element, but 0 if empty
        self.size = 0    # number of elements in the queue

    def __str__(self):
        if self.size == 0:
            return '<--<'
        stringlist = ['<']
        for i in range(self.size):
            stringlist.append('-' 
                         + str(self.body[(self.head + i)%len(self.body)]))
        stringlist.append('-<')
        return ''.join(stringlist)


    def get_size(self):
        """ Return the internal size of the queue. """
        return sys.getsizeof(self.body)

    
    def grow(self, newsize):
        """ Grow the internal representation of the queue.

        This should not be called externally.

        This one method can be used to grow or shrink the queue, but assumes
        that an appropriate size parameter is given as input. If an input
        parameter that is too small is given, the result is not defined (but
        will probably give a queue in which some items have disappeared).

        Args:
            newsize - the (int) new size to be reserved for the queue; must be
                      larger than the number of items already in the queue.
        """
        oldbody = self.body
        self.body = [None] * int(newsize)
        pos = 0
        for i in range(self.size):
            self.body[pos] = oldbody[(self.head + i)%len(oldbody)]
            pos = pos + 1
        self.head = 0


    def enqueue(self,item):
        """ Add an item to the queue.

        Args:
            item - (any type) to be added to the queue.
        """
        if self.size == 0:
            self.body[0] = item      # assumes an empty queue has head at 0
            self.size = 1
        else:
            self.body[(self.head + self.size)%len(self.body)] = item
            self.size = self.size + 1
            if self.size == len(self.body):  # list is now full
                self.grow(2*self.size)       # so grow it ready for next enqueue

    def dequeue(self):
        """ Return (and remove) the item in the queue for longest. """
        if self.size == 0:     # empty queue
            return None
        item = self.body[self.head]
        self.body[self.head] = None
        if self.size == 1:            # just removed last element, so rebalance
            self.head = 0
            #self.tail = 0
            self.size = 0
        else:            
            self.head = (self.head + 1)%len(self.body)
            self.size = self.size - 1
        # we haven't changed the tail, so nothing to do
        if self.size > 10 and self.size < 0.25*len(self.body):
            self.grow(0.5*len(self.body))
        return item

    def length(self):
        """ Return the number of items in the queue. """
        return self.size

    def first(self):
        """ Return the first item in the queue. """
        return self.body[self.head]      # will return None if queue is empty

class Queue(QueueV3):
    """ A Queue, which is effectively just an instance of the above classes.

    This is a hack so that I can change the Queue implementation without
    changing any of my code that uses a Queue class. To test the behaviour or p
    performance of a specific Queue implementation, just change the inheritance
    above to a different QueueVXX implementation.
    """
    def __init__(self):
        super().__init__()


def test_queue_wrap():
    """ Simple test that wrapping around internally is working. """
    q = Queue()
    q.enqueue(1)
    q.enqueue(2)
    q.dequeue()
    q.enqueue(3)
    q.enqueue(4)
    q.enqueue(5)
    q.dequeue()
    q.enqueue(6)
    q.enqueue(7)
    q.enqueue(8)
    q.enqueue(9)
    q.enqueue(10)
    q.enqueue(11)
    q.enqueue(12)
    q.enqueue(13)
    q.enqueue(14)
    q.enqueue(15)
    q.dequeue()
    print('Should be a sequence from 4 to 15 inclusive, items 12, space 20')
    print('q : %s (items = %d, space = %d)' % (
                                         q,
                                         q.length(),
                                         len(q.body)))
    for i in range(30):
        q.enqueue(i + 16)
    print('Should be a sequence from 4 to 45 inclusive, items 42, space 80')
    print('q : %s (items = %d, space = %d)' % (
                                         q,
                                         q.length(),
                                         len(q.body)))
    for i in range(24):
        q.dequeue()
    print('Should be a sequence from 28 to 45 inclusive, items 18, space 40')
    print('q : %s (items = %d, space = %d)' % (
                                         q,
                                         q.length(),
                                         len(q.body)))

'''
def test_all_queues(n):
    """ Compare performance of the four different queue implementations. """

    print("Creating a queue of each type.")
    q0 = QueueV0()
    q1 = QueueV1()
    q2 = QueueV2()
    q3 = QueueV3()
    qlist = [q0, q1,q2, q3]

    print('Empty lengths:', q0.length(), q1.length(), q2.length(), q3.length())
    print("First basic enqueuing and dequeuing:")
    for i in range(4):
        qlist[i].enqueue(1)
        qlist[i].enqueue(2)
        qlist[i].dequeue()
        qlist[i].enqueue(3)
        qlist[i].enqueue(4)
        qlist[i].enqueue(5)
        qlist[i].dequeue()
        qlist[i].enqueue(6)
        qlist[i].enqueue(7)
        qlist[i].enqueue(8)
        qlist[i].enqueue(9)
        qlist[i].enqueue(10)
        qlist[i].enqueue(11)
        qlist[i].enqueue(12)
        qlist[i].enqueue(13)
        qlist[i].enqueue(14)
        qlist[i].enqueue(15)
        qlist[i].dequeue()
        print('q', i, ':', qlist[i])

    print('enqueuing n items, then dequeuing n in each queue:')
    for i in range(4):
        start_time = time.perf_counter()
        for j in range(n):
            qlist[i].enqueue(1)
        for j in range(n):
            qlist[i].dequeue()
        end_time = time.perf_counter()
        print(i, 'took', end_time - start_time,
              'and has size', qlist[i].get_size(),
              'but length', qlist[i].length())

    print('now starting again, and maintaining a list of size 20 through',
          'n operations')
    qlist[0] = QueueV0()
    qlist[1] = QueueV1()
    qlist[2] = QueueV2()
    qlist[3] = QueueV3()
    for i in range(4):
        start_time = time.perf_counter()
        for j in range(20):
            qlist[i].enqueue(1)
        for j in range(n):
            qlist[i].enqueue(1)
            qlist[i].dequeue()
        end_time = time.perf_counter()
        print(i, 'took', end_time - start_time,
              'and has size', qlist[i].get_size(),
              'but length', qlist[i].length())
'''

def reverse_queue(queue):
    """ Reverse a queue.

    Note that this will destroy the original queue.

    Args:
        queue - a queue

    Returns the reverse of the input queue.
    """
    outqueue = QueueV3()
    stack = Stack()
    while not queue.length() == 0:
        item = queue.dequeue()
        stack.push(item)
        print('dequeued', item)
    while not stack.length() == 0:
        item = stack.pop()
        outqueue.enqueue(item)
        print('enqueued', item)
    return outqueue

def reverse_queue2(queue):
    """ Reverse a queue.

    This will finish with the original queue in its original state.

    Args:
        queue - a queue

    Returns the reverse of the input queue.
    """
    outqueue = QueueV3()
    stack = Stack()
    i = queue.length()
    for pos in range(i):
        item = queue.dequeue()
        stack.push(item)
        print('dequeued', item)
        queue.enqueue(item)
    while not stack.length() == 0:
        item = stack.pop()
        outqueue.enqueue(item)
        print('enqueued', item)
    return outqueue

def test_reverse_queue(flag):
    """ Test the reverse queue methods.

    Args:
        flag - int stating which method to use (1 for first, 2 for second
    """
    queue = Queue()
    queue.enqueue(1)
    queue.enqueue(2)
    queue.enqueue(3)
    queue.enqueue(4)
    queue.enqueue(5)
    print('Input queue:', queue)
    if flag == 1 :
        outqueue = reverse_queue(queue)
    elif flag == 2:
        outqueue = reverse_queue2(queue)
    else:
        print('Input flag must be 1 or 2')
    print('Reversed queue:', outqueue)
    print('original queue:', queue)

if __name__ == '__main__':
    test_reverse_queue(2)

