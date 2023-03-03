class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None
        self.prev = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
    
    def is_empty(self):
        return self.head is None
    
    def put_front(self, data):
        new_node = Node(data)
        self.size += 1
        if self.is_empty():
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
    
    def put_back(self, data):
        new_node = Node(data)
        self.size += 1
        if self.is_empty():
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
    
    def remove_front(self):
        if self.is_empty():
            return None
        data = self.head.data
        self.size -= 1
        if self.head == self.tail:
            self.head = self.tail = None
        else:
            self.head = self.head.next
            self.head.prev = None
        return data
    
    def remove_back(self):
        if self.is_empty():
            return None
        data = self.tail.data
        self.size -= 1
        if self.head == self.tail:
            self.head = self.tail = None
        else:
            self.tail = self.tail.prev
            self.tail.next = None
        return data
    
    def traverse_forward(self):
        current = self.head
        while current:
            yield current.data
            current = current.next
    
    def traverse_backward(self):
        current = self.tail
        while current:
            yield current.data
            current = current.prev