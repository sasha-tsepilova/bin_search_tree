"""
File: linkedstack.py
Author: Ken Lambert
"""

from node import Node
from abstractstack import AbstractStack


class LinkedStack(AbstractStack):
    """A link-based stack implementation."""

    # Constructor
    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._items = None
        AbstractStack.__init__(self, sourceCollection)

    # Accessor methods
    def __iter__(self):
        """Supports iteration over a view of self."""

        def visit_nodes(node):
            """Adds items to temp_list from tail to head."""
            if not node is None:
                visit_nodes(node.next)
                temp_list.append(node.data)

        temp_list = list()
        visit_nodes(self._items)
        return iter(temp_list)

    def peek(self):
        """
        Returns the item at the top of the stack.
        Precondition: the stack is not empty.
        Raises: KeyError if the stack is empty."""
        if self.isEmpty():
            raise KeyError("The stack is empty.")
        return self._items.data

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._size = 0
        self._items = None

    def push(self, item):
        """Adds item to the top of the stack."""
        self._items = Node(item, self._items)
        self._size += 1

    def pop(self):
        """
        Removes and returns the item at the top of the stack.
        Precondition: the stack is not empty.
        Raises: KeyError if the stack is empty.
        Postcondition: the top item is removed from the stack."""
        if self.isEmpty():
            raise KeyError("The stack is empty.")
        data = self._items.data
        self._items = self._items.next
        self._size -= 1
        return data
