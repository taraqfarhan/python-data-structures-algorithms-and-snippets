class SinglyLinkedList:
    class Node:
        """each Node of a Linked List structure"""
        # Each Node has a data and a pointer to the next Node
        def __init__(self, data, next=None):
            self.data = data # data stored in the current Node

            # each Node points to the next Node of the Linked List
            # if there is no Node after current Node then next points to None
            self.next = next


        def __repr__(self):
            """Represenattion of a Node object"""
            try:
                return f"Node({self.data} -> {self.next.data})"
            except AttributeError:
                return f"Node({self.data} -> {None})"



    # Each Linked List has a head pointer
    # which points to the head (first Node) of the Linked List
    # If there is no Node (the linked list is empty)
    # then head points to None
    def __init__(self, linkedlist=None):
        self.head = None  # the head pointer
        self._n = 0    # total nodes

        # SinglyLinkedList(['A', 'B', 'C', 'D']) to A -> B -> C -> D
        if linkedlist is not None:
            for data in linkedlist: self.append(data)


    def append(self, data):
        """append a new Node at the end of the Linked List"""
        current_node = self.head
        new_node = self.Node(data)

        # case 1: the list is empty
        if current_node is None:
            self.head = new_node

        # case 2: the list has already one or more elements
        else:
            # while current_node is not the last node
            while current_node.next is not None:
                current_node = current_node.next

            # current_node is now the last node
            # link the new node from the last node
            current_node.next = new_node
        self._n += 1


    def appendleft(self, data):
        """append a new Node at the start of the Linked List"""
        new_node = self.Node(data)    # Create the new node
        new_node.next = self.head     # new_node points it to the old head
        self.head = new_node          # Make it the new head
        self._n += 1


    def index(self, data, start=0):
        """return the first index of data starting at `start`"""
        current_node = self.head
        current_index = 0

        while current_node is not None:
            if current_node.data == data and current_index >= start:
                return current_index
            current_index += 1
            current_node = current_node.next


    # Improvements: Python's built-in list.insert()
    # will just append to the end if the index is too large.
    def insert(self, index, data):
        """insert data before index"""
        if index < 0:
            index += self._n    # handle negative indexing
        if index < 0:
            raise IndexError("Index out of range")

        if index == 0:
            self.appendleft(data)
            return
        elif index >= self._n:
            self.append(data)
            return

        current_node = self.head
        current_index = 0
        new_node = self.Node(data)

        while current_node is not None and current_index != (index-1):
            current_node = current_node.next
            current_index += 1

        if current_node is not None:
            # add data to this
            old_node = current_node.next
            current_node.next = new_node
            new_node.next = old_node
        self._n += 1


    def pop(self, index=None, node=False):
        """Pop an item from the list using indexing"""
        if index is None or index >= self._n:   # default is the last item
            index = self._n - 1
        if index < 0:
            index += self._n
        if index < 0:
            raise IndexError("Index out of range")
        if index == 0:
            return self.popleft()

        current_index = 0
        current_node = self.head
        # traverse to the index - 1
        while current_node is not None and current_index != (index - 1):
            current_node = current_node.next
            current_index += 1

        # current_node is in (index - 1)th position
        if node: value = current_node
        else: value = current_node.data
        current_node.next = current_node.next.next
        self._n -= 1
        return value


    def popleft(self, node=False):
        current_node = self.head

        # Case 1: empty
        if current_node is None: value = self.head
        # Case 2: Only one node
        elif current_node.next is None:
            value = self.head.data
            self.head = None
        # Case 3: More than 1 node
        else:
            value = self.head.data
            self.head = current_node.next
        self._n -= 1

        if node: value = current_node
        else: value = current_node.data

        return value


    def remove(self, value):
        """Remove the first occurrence of Node that has Node.data == value"""
        current_node = self.head
        # while current_node is not None and current_node.next.data != value:
        while current_node is not None:
            if current_node.next.data == value:
                current_node.next = current_node.next.next
                break
            current_node = current_node.next
        # if current_node is None or (current_node.next is None and current_node.next.data != value):
        #     raise ValueError("Value not in the list")
        # current_node.next = current_node.next.next



    def get_node(self, index):
        """get Node from the Linked List using 0 indexing"""
        current_node = self.head
        current_index = 0

        while current_node is not None and current_index != index:
            current_node = current_node.next
            current_index += 1

        if current_node is not None:
            return current_node


    def get_data(self, index):
        return self[index]


    def __getitem__(self, key):
        """get data from the Linked List using [ ] indexing"""
        if isinstance(key, int):
            if key < 0:
                key += self._n    # handle negative index
            if key < 0 or key >= self._n:
                raise IndexError("Linked List index out of range")

            node = self.get_node(key)   # get the node at that index
            if node: return node.data   # if node exits, then return the data

        if isinstance(key, slice):
            start, stop, step = key.indices(len(self))
            return [self.get_node(k).data for k in range(start, stop, step)]


    def __iter__(self):
        """Iterator for the SinglyLinkedList object"""
        for i in range(self._n):
            yield self[i]


    def __repr__(self):
        """Representation of a SinglyLinkedList object"""
        # values = ["head"]
        # values.extend(map(str, list(self.tolist())))
        # values.append("None")
        values = map(str, list(self.tolist()))
        return f"SinglyLinkedList({" -> ".join(values)})"


    def tolist(self):
        """traverse the whole Linked List"""
        current_node = self.head

        # the last Node always points to None
        # condtion: while there is a Node
        while current_node is not None:
            yield current_node.data
            current_node = current_node.next


    def reverse(self):
        """
            reverse the actual linked list in place
            like from A -> B -> C -> D to A <- B <- C <- D
        """
        prev_visited = None
        current_node = self.head

        while current_node is not None:
            next_node = current_node.next
            current_node.next = prev_visited
            prev_visited = current_node

            current_node = next_node

        self.head = prev_visited


    def __len__(self):
        """Get the length of the Singly Linked List"""
        return self._n


    def __add__(self, other):
        """
        Zipping two linked lists into a NEW third list.
        Does NOT mutate self or other.

        if first = A -> B -> C -> D - E
        and second = F -> G
        first + second = A -> F -> B -> G -> C -> D - E
        """

        # 1. Create the new list object
        new_list = SinglyLinkedList()

        # 2. Create a 'dummy' node. This is a temporary placeholder
        # that helps us avoid writing complex "if head is None" logic.
        # We will attach our new nodes to this dummy.
        dummy = self.Node(None)
        tail = dummy

        # Pointers for the existing lists
        current1 = self.head
        current2 = other.head

        # 3. Loop while BOTH lists have data
        while current1 is not None and current2 is not None:
            # --- Take from List 1 ---
            # Create a NEW node with the data (copying)
            tail.next = self.Node(current1.data)
            tail = tail.next  # Move tail forward
            current1 = current1.next  # Move ptr1 forward

            # --- Take from List 2 ---
            # Create a NEW node with the data (copying)
            tail.next = self.Node(current2.data)
            tail = tail.next  # Move tail forward
            current2 = current2.next  # Move ptr2 forward

        # 4. Handle leftovers (if one list is longer than the other)
        # We still need to loop and COPY the data, otherwise
        # the end of our new list would point to the old list's nodes.

        while current1 is not None:
            tail.next = self.Node(current1.data)
            tail = tail.next
            current1 = current1.next

        while current2 is not None:
            tail.next = self.Node(current2.data)
            tail = tail.next
            current2 = current2.next

        # 5. Set the head of our new list
        # 'dummy' was just a placeholder. The real list starts at dummy.next
        new_list.head = dummy.next

        new_list._n = self._n + len(other)
        return new_list
