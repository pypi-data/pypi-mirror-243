import random
import time
from unittest import TestCase

from . import BinaryTree


class MyTestClass:
    def __init__(self, sortable_value: int, message: str):
        assert isinstance(sortable_value, int)
        assert isinstance(message, str)
        self.value = sortable_value
        self.message = message

    def __lt__(self, other):
        if isinstance(other, MyTestClass):
            return self.value < other.value
        elif isinstance(other, int):
            return self.value < other

    def __le__(self, other):
        if isinstance(other, MyTestClass):
            return self.value <= other.value
        elif isinstance(other, int):
            return self.value <= other

    def __eq__(self, other):
        if isinstance(other, MyTestClass):
            return self.value == other.value
        elif isinstance(other, int):
            return self.value == other

    def __ge__(self, other):
        if isinstance(other, MyTestClass):
            return self.value >= other.value
        elif isinstance(other, int):
            return self.value >= other

    def __gt__(self, other):
        if isinstance(other, MyTestClass):
            return self.value > other.value
        elif isinstance(other, int):
            return self.value > other

    def __str__(self):
        return "{}: {}".format(self.value, self.message)


class TestBinaryTree(TestCase):
    def test_sort_string(self):
        test_string = "The quick brown fox jumps over the lazy dog."
        sorted_list = sorted([x for x in test_string])
        tree = BinaryTree(list(test_string))
        self.assertEqual(sorted_list, list(tree))

    def test_sort_integers(self):
        integers = [5, 3, 5, 7, 37, 1, 20]
        sorted_list = sorted(integers)
        tree = BinaryTree(integers)
        self.assertEqual(sorted_list, list(tree))

    def test_sort_random_integers(self):
        random.seed(time.time())
        integers = [random.randint(1, 1000) for x in range(1_000)]
        sorted_list = sorted(integers)
        tree = BinaryTree(integers)
        self.assertEqual(sorted_list, list(tree))

    def test_balance(self):
        random.seed(time.time())
        integers = [random.randint(1, 10_000) for x in range(1_000)]
        sorted_list = sorted(integers)
        tree = BinaryTree(integers)
        self.assertEqual(sorted_list, list(tree))
        tree.balance()
        self.assertEqual(sorted_list, list(tree))

    def test_find(self):
        num_values = 1000
        random.seed(time.time())

        random_values = [random.randint(1, 1_000) for _ in range(num_values)]
        random_strings = [random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(num_values)]
        values = [
            MyTestClass(sortable_value=val, message=mes)
            for val, mes in
            zip(random_values, random_strings)
        ]
        search_val = random.randint(-1000, -1)
        num_searchable_values = 10
        searchable_message_chars = "!@#$%^&*()-_=+"
        for _ in range(num_searchable_values):
            message = random.choice(searchable_message_chars)
            values.append(MyTestClass(sortable_value=search_val, message=message))

        tree = BinaryTree(values)
        values.sort()

        # Assert that searchable items keep their other attributes.
        result = tree.find_equal_to(search_val)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), num_searchable_values)
        self.assertEqual(len(result), sum([x.message in searchable_message_chars for x in result]))

        # Assert that a non-existent value returns an empty list.
        self.assertEqual([], tree.find_equal_to(2319))

        integers = [10, 1, 9, 2, 8, 3, 7, 4, 6, 5]
        tree = BinaryTree(integers, balance_on_init=False)

        self.assertEqual([2], tree.find_equal_to(2))

    def test_len(self):
        tree = BinaryTree()
        tree.add("A")
        self.assertEqual(len(list(tree)), len(tree))
        self.assertEqual(1, len(tree))

        random.seed(time.time())
        for _ in range(100):
            random_length = random.randint(10, 100)
            integers = [random.randint(1, 1000) for _ in range(random_length)]
            tree = BinaryTree(integers)
            self.assertEqual(len(list(tree)), len(tree))
            self.assertEqual(len(integers), len(tree))

        for _ in range(100):
            random_length = random.randint(10, 100)
            integers = [random.randint(1, 1000) for _ in range(random_length)]
            tree = BinaryTree()
            tree.add(integers)
            self.assertEqual(len(list(tree)), len(tree))
            self.assertEqual(len(integers), len(tree))

    def test_reverse_iter(self):
        random.seed(time.time())
        integers = [random.randint(1, 1000) for x in range(1_000)]
        tree = BinaryTree(integers)

        reversed_list = sorted(integers)
        reversed_list.reverse()
        reversed_tree_vals = list(tree.reversed())
        self.assertEqual(reversed_list, reversed_tree_vals)

    def test_find_lesser(self):
        integers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        tree = BinaryTree(integers)

        self.assertEqual([1, 2, 3, 4], tree.find_less_than(5))
        self.assertEqual([1, ], tree.find_less_than(2))
        self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], tree.find_less_than(100))
        self.assertEqual([], tree.find_less_than(0))

        integers = [10, 1, 9, 2, 8, 3, 7, 4, 6, 5]
        tree = BinaryTree(integers, balance_on_init=False)

        self.assertEqual([1, 2, 3, 4], tree.find_less_than(5))
        self.assertEqual([1, ], tree.find_less_than(2))
        self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], tree.find_less_than(100))
        self.assertEqual([], tree.find_less_than(0))

    def test_find_greater(self):
        integers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        tree = BinaryTree(integers)

        self.assertEqual([6, 7, 8, 9, 10], tree.find_greater_than(5))
        self.assertEqual([3, 4, 5, 6, 7, 8, 9, 10], tree.find_greater_than(2))
        self.assertEqual([], tree.find_greater_than(100))
        self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], tree.find_greater_than(0))

        integers = [10, 1, 9, 2, 8, 3, 7, 4, 6, 5]
        tree = BinaryTree(integers, balance_on_init=False)

        self.assertEqual([6, 7, 8, 9, 10], tree.find_greater_than(5))
        self.assertEqual([3, 4, 5, 6, 7, 8, 9, 10], tree.find_greater_than(2))
        self.assertEqual([], tree.find_greater_than(100))
        self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], tree.find_greater_than(0))

    def test_find_between(self):
        integers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        tree = BinaryTree(integers)

        self.assertEqual([2, 3, 4], tree.find_between(2, 4))
        self.assertEqual([2, ], tree.find_between(2, 2))
        self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], tree.find_between(1, 10))
        self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], tree.find_between(-100, 100))
        self.assertEqual([], tree.find_between(100, 200))

        integers = [10, 1, 9, 2, 8, 3, 7, 4, 6, 5]
        tree = BinaryTree(integers, balance_on_init=False)

        self.assertEqual([2, 3, 4], tree.find_between(2, 4))
        self.assertEqual([2, ], tree.find_between(2, 2))
        self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], tree.find_between(1, 10))
        self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], tree.find_between(-100, 100))
        self.assertEqual([], tree.find_between(100, 200))

        integers = [x for x in range(100)]
        integers.sort(key=lambda x: random.randint(1, 100))
        tree = BinaryTree(integers, balance_on_init=False)

        self.assertEqual([2, 3, 4], tree.find_between(2, 4))
        self.assertEqual([2, ], tree.find_between(2, 2))
        self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], tree.find_between(1, 10))
        self.assertEqual([x for x in range(100)], tree.find_between(0, 100))

    def test_in_keyword(self):
        integers = [1, 2, 3, 4, 5]
        tree = BinaryTree(integers)

        for integer in integers:
            self.assertTrue(integer in tree)
        self.assertFalse(6 in integers)
        self.assertFalse(6 in tree)

    def test_context_manager(self):
        integers = [x for x in range(127)]
        with BinaryTree(integers) as tree:
            tree.add(-1)
            self.assertTrue(1 in list(tree))

    def test_remove_value(self):
        integer = 1
        tree = BinaryTree(integer)
        tree.remove_one(integer)

        integers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        tree = BinaryTree(integers)
        tree.remove_one(3)
        self.assertEqual([1, 2, 4, 5, 6, 7, 8, 9, 10], list(tree))

        # Test with random data.
        for _ in range(100):
            integers = [random.randint(1, 10_000) for _ in range(25)]
            tree = BinaryTree(integers)

            while len(integers) > 0:
                removed_int = integers.pop(0)
                tree.remove_one(removed_int)
                self.assertEqual(len(integers), len(tree))
                self.assertEqual(list(sorted(integers)), list(tree))

    def test_remove_list_of_values(self):
        integers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        tree = BinaryTree(integers)
        tree.remove_one([1, 2, 3, 4, 5])
        self.assertEqual([6, 7, 8, 9, 10], list(tree))

        # Test with random data.
        for _ in range(100):
            integers = [random.randint(1, 10_000) for _ in range(25)]
            tree = BinaryTree(integers)

            remove_ints = integers[:len(integers) // 2]
            keep_ints = integers[len(integers) // 2:]
            tree.remove_one(remove_ints)
            self.assertEqual(len(keep_ints), len(tree))
            self.assertEqual(list(sorted(keep_ints)), list(tree))

    def test_remove_all_values(self):
        integers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] + [11 for _ in range(10)]
        tree = BinaryTree(integers)
        tree.remove_all(11)
        self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], list(tree))

    def test_remove_all_values_in_list(self):
        remove_values = [x + 100 for x in range(10)]
        integers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] + remove_values
        tree = BinaryTree(integers)
        tree.remove_all(remove_values)
        self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], list(tree))

    def test_add_value(self):
        tree = BinaryTree()
        self.assertEqual([], list(tree))
        tree.add(5)
        self.assertEqual([5], list(tree))

    def test_add_list_of_values(self):
        tree = BinaryTree()
        self.assertEqual([], list(tree))
        tree.add([1, 2, 3, 4, 5])
        self.assertEqual([1, 2, 3, 4, 5], list(tree))
        tree.add((6, 7, 8, 9, 10))
        self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], list(tree))

    def test_print_empty_tree(self):
        tree = BinaryTree()
        self.assertEqual("", tree.to_display_string())
        self.assertEqual("", tree.to_flipped_display_string())

    def test_print_single_node_tree(self):
        tree = BinaryTree(1)
        self.assertEqual("1", tree.to_display_string())
        self.assertEqual("1", tree.to_flipped_display_string())





