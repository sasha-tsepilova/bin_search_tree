"""
File: linkedbst.py
Author: Ken Lambert
"""

from math import log
from time import time
from random import choice, shuffle
from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack


class LinkedBST(AbstractCollection):
    """
    An link-based binary search tree implementation.
    Attributes
    ----------
    _root: BSTNode
        The root of the tree.
    Methods
    -------
    inorder()
        Returns a list of an inorder view of the tree.
    find(item)
        Returns True if item is in the tree and False otherwise.
    clear()
        Clears the tree.
    add(item)
        Adds the item to the tree.
    remove(item)
        Removes the item from the tree.
    replace(item, new_item)
        Replaces the item in the tree with the new_item.
    height()
        Returns the height of the tree.
    num_vert()
        Returns the number of the vertixes in the tree.
    is_balanced()
        Returns True if the tree is balanced? otherwise returns False.
    range_find(low, high)
        Returns the  list of items in tree which are between low and high.
    rebalance()
        Makes the tree balanced.
    successor(item)
        Returns the smallest item that is larger than
        item, or None if there is no such item.
    predecessor(item)
        Returns the largest item that is smaller than
        item, or None if there is no such item.
    """

    def __init__(self, source_collection=None) -> None:
        """
        Sets the initial state of self, which includes the
        contents of source_collection, if it's present.
        Parameters
        ----------
        source_collection: iterable
            The source collection.
        """
        self._root = None
        AbstractCollection.__init__(self, source_collection)

    def __str__(self) -> str:
        """
        Returns a string representation with the tree rotated
        90 degrees counterclockwise.
        """

        def recurse(node: BSTNode, level: int) -> str:
            '''
            Recursion function to get string representation of the tree.
            Parameters
            ----------
            node: BSTNode
                The current node.
            level: int
                The level of current node.
            '''
            strin = ""
            if node:
                strin += recurse(node.right, level + 1)
                strin += "| " * level
                strin += str(node.data) + "\n"
                strin += recurse(node.left, level + 1)
            return strin

        return recurse(self._root, 0)

    def __iter__(self) -> iter:
        """
        Supports a preorder traversal on a view of self.
        """
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right:
                    stack.push(node.right)
                if node.left:
                    stack.push(node.left)

    def inorder(self) -> list:
        """
        Supports an inorder traversal on a view of self.
        """
        lyst = list()

        def recurse(node):
            if node:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return lyst

    def __contains__(self, item: object) -> bool:
        """
        Returns True if target is found or False otherwise.
        Parameters
        ----------
        item: object
            The item, which needs to be checked.
        """
        return bool(self.find(item))

    def find(self, item: object) -> object:
        """
        If item matches an item in self, returns the
        matched item, or None otherwise.
        Parameters
        ----------
        item: object
            The item, which needs to be found.
        """

        def recurse(node: BSTNode) -> BSTNode:
            '''
            Recursion function for finding the needed item.
            Parameters
            ----------
            node: BSTNode
                The current node.
            '''
            if node is None:
                return None
            if item == node.data:
                return node.data
            if item < node.data:
                return recurse(node.left)
            return recurse(node.right)

        return recurse(self._root)

    def clear(self) -> None:
        """
        Makes self become empty.
        """
        self._root = None
        self._size = 0

    def add(self, item: object) -> None:
        """
        Adds item to the tree.
        Parameters
        ----------
        item: object
            The added item.
        """

        def recurse(node: BSTNode) -> None:
            '''
            Helper function to search for item's position.
            Parameters
            ----------
            node: BSTNode
                The current node.
            '''
            if item < node.data:
                if not node.left:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            elif not node.right:
                node.right = BSTNode(item)
            else:
                recurse(node.right)

        if self.isEmpty():
            self._root = BSTNode(item)
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item: object) -> None:
        """
        Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self.
        Parameters
        ----------
        item: object
            The removed item.
        """
        if not item in self:
            raise KeyError("Item not in tree.""")

        def lift_max_in_left_subtree_to_top(top: BSTNode) -> None:
            '''
            Helper function to adjust placement of an item.
            Replace top's datum with the maximum datum in the left subtree
            Pre:  top has a left child
            Post: the maximum node in top's left subtree
                  has been removed
            Post: top.data = maximum value in top's left subtree
            Parameters
            ----------
            top: BSTNode
                The current node.
            '''
            parent = top
            current_node = top.left
            while current_node.right:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        if self.isEmpty():
            return None

        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        current_node = self._root
        while current_node:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = 'L'
                current_node = current_node.left
            else:
                direction = 'R'
                current_node = current_node.right

        if not item_removed:
            return None

        if current_node.left and current_node.right:
            lift_max_in_left_subtree_to_top(current_node)
        else:

            if not current_node.left:
                new_child = current_node.right

            else:
                new_child = current_node.left

            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item: object, new_item: object) -> object:
        """
        If item is in self, replaces it with new_item and
        returns the old item, or returns None otherwise.
        Parameters
        ----------
        item: object
            The replaced item.
        new_item: object
            On what we want to replace.
        """
        probe = self._root
        while probe:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            if probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self) -> int:
        '''
        Return the height of tree
        '''
        def height1(top: BSTNode) -> int:
            '''
            Helper function for founding the tree height.
            Parameters
            ----------
            top: BSTNode
                The current top.
            '''
            if not top:
                return 0
            return max(height1(top.left), height1(top.right)) + 1

        return height1(self._root) - 1

    def num_vert(self) -> int:
        '''
        Returns the number of vertixes in the tree.
        '''
        def num_nasch(top: BSTNode) -> int:
            '''
            Returns the number of all children of the top.
            Parameters
            ----------
            top: BSTNode
                The current top.
            '''
            children = 0
            if top.left:
                children += 1 + num_nasch(top.left)
            if top.right:
                children += 1 + num_nasch(top.right)
            return children
        return num_nasch(self._root) + 1

    def is_balanced(self) -> bool:
        '''
        Return True if tree is balanced.
        '''
        return self.height() < 2 * log(self.num_vert() + 1) - 1

    def range_find(self, low: object, high: object) -> list:
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        Parameters
        ----------
        low: object
            The minimum possible item in the returned list.
        high: object
            The maximum possible item in the returned list.
        '''
        lyst = self.inorder()
        return list(filter(lambda x: low <= x <= high, lyst))

    def rebalance(self) -> None:
        '''
        Rebalances the tree.
        '''
        lyst = self.inorder()
        self.clear()

        def recurs(lyst, tree):
            if lyst:
                elem = lyst[len(lyst) // 2]
                tree.add(elem)
                recurs(lyst[0:len(lyst) // 2], tree)
                recurs(lyst[len(lyst) // 2 + 1:], tree)
        recurs(lyst, self)
        return self

    def successor(self, item: object) -> object:
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        Parameters
        ----------
        item: object
            The successor item.
        """
        top = self._root

        def recurs(top):
            if top:
                if top.data <= item:
                    answ = recurs(top.right)
                    if answ:
                        return answ
                    return None
                answ = recurs(top.left)
                if answ:
                    return answ
                return top.data
            return None
        return recurs(top)

    def predecessor(self, item: object) -> object:
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        Parameters
        ----------
        item: object
            The predecessor item.
        """
        top = self._root

        def recurs(top):
            if top:
                if top.data >= item:
                    answ = recurs(top.left)
                    if answ:
                        return answ
                    return None
                answ = recurs(top.right)
                if answ:
                    return answ
                return top.data
            return None
        return recurs(top)

    def demo_bst(self, input_file: str) -> None:
        '''
        Demonstrates the differences in time between searches
        with binary tree and list methods.
        Parameters
        ----------
        input_file: str
            The analysed file.
        '''
        def search_time(words, tree):
            '''
            Returns the searching time for 10000 random words in given tree.
            Parameters
            ----------
            words: list
                The words list.
            tree: LinkedBST
                The tree.
            '''
            start_time = time()
            for _ in range(10000):
                word = choice(words)
                tree.find(word)
            return time() - start_time

        words = []
        with open(input_file) as fin:
            word = fin.readline()
            while word:
                words.append(word)
                word = fin.readline()
        if len(words) > 1000:
            words = words[:1000]

        self.clear()
        for word in words:
            self.add(word)

        start_time = time()
        for _ in range(10000):
            word = choice(words)
            words.index(word)
        print('Час пошуку 10000 випадкових слів у впорядкованому за абеткою словнику:',
              f'{time() - start_time}.')

        print('Час пошуку 10000 випадкових слів у словнику, який представлений у вигляді ' +
              'бінарного дерева пошуку (побудовона нa основі словника, відсортованого за' +
              f' алфавітом): {search_time(words, self)}.')

        self.clear()
        shuffle(words)
        for word in words:
            self.add(word)

        print('Час пошуку 10000 випадкових слів у словнику, який представлений у вигляді ' +
              'бінарного дерева пошуку (побудовона нa основі словника, не відсортованого за' +
              f' алфавітом): {search_time(words, self)}.')

        self.rebalance()
        print('Час пошуку 10000 випадкових слів у словнику, який представлений у вигляді ' +
              f'збалансованого бінарного дерева пошуку: {search_time(words, self)}.')
