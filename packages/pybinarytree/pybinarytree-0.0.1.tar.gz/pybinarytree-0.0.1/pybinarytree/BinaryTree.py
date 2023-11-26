from collections.abc import Iterable
from typing import Any

from pybinarytree.exceptions import NotComparableException


class BinaryTree:
    def __init__(self, values: tuple or list or Any = None, balance_on_init: bool = True):
        self._node_value = None
        self._less_than = None
        self._equal_to = None
        self._greater_than = None
        self.__length = 0

        if values is None:
            pass  # Do nothing.
        elif isinstance(values, tuple) or isinstance(values, list):
            self._node_value = values[0]
            self.__length = 1
            for value in values[1:]:
                self.add(value)
            if balance_on_init:
                self.balance()
        else:
            self._node_value = values
            self.__length = 1

    def __contains__(self, item):
        return item in self.find_equal_to(value=item)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        del self
        return None

    def __iter__(self):
        if self._node_value is None or self.__length == 0:
            return []

        crawl_stack = [self, ]
        lowest_yieldable_value = None
        while len(crawl_stack) > 0:
            # Navigate to the lowest yield-able value from the working node.
            working_node = crawl_stack[-1]
            smaller_node = working_node._less_than
            while isinstance(smaller_node, BinaryTree) and (
                lowest_yieldable_value is None or (
                    lowest_yieldable_value is not None and
                    lowest_yieldable_value < smaller_node._node_value
                )
            ):
                crawl_stack.append(smaller_node)
                smaller_node = smaller_node._less_than

            # Send back the lowest yield-able value(s).
            working_node = crawl_stack[-1]
            if lowest_yieldable_value is None or (
                lowest_yieldable_value is not None and lowest_yieldable_value < working_node._node_value
            ):
                lowest_yieldable_value = working_node._node_value
                yield lowest_yieldable_value
                equal_to_node = working_node._equal_to
                while isinstance(equal_to_node, BinaryTree):
                    yield equal_to_node._node_value
                    equal_to_node = equal_to_node._equal_to

            # Remove the current node to prevent moving backwards through the tree.
            # Add the greater than node (if it exists) to continue moving forwards.
            crawl_stack.pop(-1)
            if isinstance(working_node._greater_than, BinaryTree):
                crawl_stack.append(working_node._greater_than)

    def __len__(self):
        return self.__length

    def __reversed__(self):
        crawl_stack = [self, ]
        highest_yieldable_value = None
        while len(crawl_stack) > 0:
            # Navigate to the highest yield-able value from the working node.
            working_node = crawl_stack[-1]
            larger_node = working_node._greater_than
            while isinstance(larger_node, BinaryTree) and (
                    highest_yieldable_value is None or (
                        highest_yieldable_value is not None and
                        highest_yieldable_value > larger_node._node_value
                    )
            ):
                crawl_stack.append(larger_node)
                larger_node = larger_node._greater_than

            # Send back the highest yield-able value(s).
            working_node = crawl_stack[-1]
            if highest_yieldable_value is None or (
                    highest_yieldable_value is not None and
                    highest_yieldable_value > working_node._node_value
            ):
                highest_yieldable_value = working_node._node_value
                yield highest_yieldable_value
                equal_to_node = working_node._equal_to
                while isinstance(equal_to_node, BinaryTree):
                    yield equal_to_node._node_value
                    equal_to_node = equal_to_node._equal_to

            # Remove the current node to prevent moving backwards through the tree.
            # Add the less than node (if it exists) to continue moving forwards.
            crawl_stack.pop(-1)
            if isinstance(working_node._less_than, BinaryTree):
                crawl_stack.append(working_node._less_than)

    def __str__(self):
        return str([x for x in self.__iter__()])

    @staticmethod
    def __values_are_comparable(x, y) -> bool:
        # Check that the two values can be compared with each other.
        try:
            _ = x < y
            _ = x <= y
            _ = x == y
            _ = x >= y
            _ = x > y
            return True
        except Exception:
            return False

    def __assert_value_is_comparable(self, value):
        if self._node_value is None and not self.__values_are_comparable(value, value):
            raise NotComparableException()
        elif self._node_value is not None and not self.__values_are_comparable(self._node_value, value):
            raise NotComparableException()

    def __get_value_root_depth(self, value) -> int:
        assert value in self.find_equal_to(value)

        working_node = self
        current_depth = 0
        while working_node._node_value != value:
            current_depth += 1
            if isinstance(working_node._less_than, BinaryTree) and value < working_node._node_value:
                working_node = working_node._less_than
            elif isinstance(working_node._greater_than, BinaryTree) and value >= working_node._node_value:
                working_node = working_node._greater_than
            else:
                return -1
        else:
            return current_depth

    def add(self, new_value: Any) -> None:
        if isinstance(new_value, list) or isinstance(new_value, tuple):
            for val in new_value:
                self.add(val)
            return
        self.__assert_value_is_comparable(new_value)

        if self._node_value is None:
            self._node_value = new_value
            self.__length = 1
            return

        new_node = BinaryTree(new_value, balance_on_init=False)
        working_node = self
        try:
            self.__length += 1
            while True:
                if new_value < working_node._node_value:
                    if isinstance(working_node._less_than, BinaryTree):
                        working_node = working_node._less_than
                    else:
                        working_node._less_than = new_node
                        return
                elif new_value == working_node._node_value:
                    if isinstance(working_node._equal_to, BinaryTree):
                        working_node = working_node._equal_to
                    else:
                        working_node._equal_to = new_node
                        return
                elif new_value > working_node._node_value:
                    if isinstance(working_node._greater_than, BinaryTree):
                        working_node = working_node._greater_than
                    else:
                        working_node._greater_than = new_node
                        return
        except Exception as ex:
            self.__length -= 1
            raise ex

    def balance(self) -> None:
        new_tree_root = BinaryTree(balance_on_init=False)
        all_values = list(self)

        # Add all unique values first so that the tree is equally balanced by value, rather than being skewed
        # by multiple duplicate values.
        unique_values = []
        for value in all_values:
            if len(unique_values) == 0 or unique_values[-1] < value:
                unique_values.append(value)
        chunks = [unique_values, ]
        while len(chunks) > 0:
            working_chunk = chunks.pop(0)
            if len(working_chunk) <= 2:
                for val in working_chunk:
                    new_tree_root.add(val)
                    all_values.pop(all_values.index(val))
            else:
                val = working_chunk[len(working_chunk) // 2]
                new_tree_root.add(val)
                all_values.pop(all_values.index(val))
                chunks.append(working_chunk[:len(working_chunk) // 2])
                chunks.append(working_chunk[len(working_chunk) // 2 + 1:])

        # Add back any remaining duplicates now that the tree structure has been solidified.
        while len(all_values) > 0:
            new_tree_root.add(all_values.pop(0))

        # Update the tree.
        self._node_value = new_tree_root._node_value
        self._less_than = new_tree_root._less_than
        self._equal_to = new_tree_root._equal_to
        self._greater_than = new_tree_root._greater_than

    def find_between(self, low_val: Any, high_val: Any) -> list:
        self.__assert_value_is_comparable(low_val)
        self.__assert_value_is_comparable(high_val)
        self.__values_are_comparable(low_val, high_val)
        assert low_val <= high_val, "Lower value is not less than higher value."

        # Climb down the tree until the "root node" is within range. In a balanced tree, this should eliminate
        # about half of all remaining nodes each step. If a value does not exist within range, return an empty list.
        working_node = self
        while not low_val <= working_node._node_value <= high_val:
            if high_val < working_node._node_value:
                if isinstance(working_node._less_than, BinaryTree):
                    working_node = working_node._less_than
                else:
                    return []
            elif working_node._node_value < low_val:
                if isinstance(working_node._greater_than, BinaryTree):
                    working_node = working_node._greater_than
                else:
                    return []

        # Now that the search results have been narrowed, iterate through to get a correct answer.
        result = []
        for val in working_node.__iter__():
            if low_val <= val <= high_val:
                result.append(val)
            elif val > high_val:
                break
        return result

    def find_equal_to(self, value: Any) -> list:
        self.__assert_value_is_comparable(value)

        working_node = self
        while True:
            if value == working_node._node_value:
                result = [working_node._node_value, ]
                working_node = working_node._equal_to
                while isinstance(working_node, BinaryTree):
                    result.append(working_node._node_value)
                    working_node = working_node._equal_to
                return result
            elif isinstance(working_node._less_than, BinaryTree) and value < working_node._node_value:
                working_node = working_node._less_than
                continue
            elif isinstance(working_node._greater_than, BinaryTree) and value > working_node._node_value:
                working_node = working_node._greater_than
                continue
            return []

    def find_greater_than(self, value: Any) -> list:
        self.__assert_value_is_comparable(value)

        result = []
        for val in self.__reversed__():
            if val > value:
                result.append(val)
            else:
                break
        result.reverse()
        return result

    def find_less_than(self, value: Any) -> list:
        self.__assert_value_is_comparable(value)

        result = []
        for val in self.__iter__():
            if val < value:
                result.append(val)
            else:
                break
        return result

    def remove_one(self, value: Any):
        if isinstance(value, list) or isinstance(value, tuple):
            for val in value:
                self.remove_one(val)
            return

        if value not in self:
            return

        # Find the first node containing this value.
        parent_node = None
        remove_node = self
        while remove_node._node_value != value:
            parent_node = remove_node
            if isinstance(remove_node._less_than, BinaryTree) and value < remove_node._node_value:
                remove_node = remove_node._less_than
            elif isinstance(remove_node._greater_than, BinaryTree) and remove_node._node_value < value:
                remove_node = remove_node._greater_than
            else:
                raise Exception("Could not find node that was expected in tree.")

        # "Delete" the removable node and add back all misplaced children nodes.
        add_nodes = []
        if isinstance(remove_node._equal_to, BinaryTree):
            # If the node has an equal node, just overwrite the node with its equal (ignoring LT or GT).
            equal_node = remove_node._equal_to
            remove_node._node_value = equal_node._node_value
            remove_node._equal_to = equal_node._equal_to
            self.__length -= 1
            return
        elif isinstance(remove_node._less_than, BinaryTree):
            # Move the lesser node to where the removable node is, then add back greater values later.
            add_nodes.append(remove_node._greater_than)
            temp_node = remove_node._less_than
            remove_node._node_value = temp_node._node_value
            remove_node._less_than = temp_node._less_than
            remove_node._equal_to = temp_node._equal_to
            remove_node._greater_than = temp_node._greater_than
            self.__length -= 1
        elif isinstance(remove_node._greater_than, BinaryTree):
            # Move the greater node to where the removable node is, then add back lesser values later.
            add_nodes.append(remove_node._less_than)
            temp_node = remove_node._greater_than
            remove_node._node_value = temp_node._node_value
            remove_node._less_than = temp_node._less_than
            remove_node._equal_to = temp_node._equal_to
            remove_node._greater_than = temp_node._greater_than
            self.__length -= 1
        elif isinstance(parent_node, BinaryTree):
            # The removable node does not have any children to replace it. Just delete it from the parent instead.
            if remove_node._node_value < parent_node._node_value:
                parent_node._less_than = None
                self.__length -= 1
            elif parent_node._node_value < remove_node._node_value:
                parent_node._greater_than = None
                self.__length -= 1
        else:
            # The removable node does not have any children nor parent. Just reset the tree root values.
            self._node_value = None
            self._less_than = None
            self._equal_to = None
            self._greater_than = None
            self.__length = 0
            return

        # Add back missing nodes while keeping track of the actual tree length.
        while len(add_nodes) > 0:
            node = add_nodes.pop(0)
            if node is None:
                continue

            assert isinstance(node, BinaryTree)
            add_nodes.append(node._less_than)
            add_nodes.append(node._equal_to)
            add_nodes.append(node._greater_than)
            self.add(node._node_value)
            self.__length -= 1

    def remove_all(self, value: Any):
        if isinstance(value, list) or isinstance(value, tuple):
            for val in value:
                self.remove_all(val)
            return

        while value in self:
            self.remove_one(value)

    def reversed(self):
        return self.__reversed__()

    def to_display_string(self) -> str:
        if self.__length == 1:
            return str(self._node_value)

        # Get root values for horizontal alignment.
        root_values = []
        for value in self.__iter__():
            if len(root_values) == 0:
                root_values.append(value)
            elif value != root_values[-1]:
                root_values.append(value)

        # If the tree is empty, return an empty string.
        if len(root_values) == 0:
            return ""

        # Get depths of values for vertical alignment.
        root_value_depths = [self.__get_value_root_depth(x) for x in root_values]

        # Generate a string matrix with the height and width of the tree.
        matrix = [[""] * (max(root_value_depths) + 1) for _ in range(len(root_values))]

        # Add values to the string matrix.
        for x in range(len(root_values)):
            y = root_value_depths[x]
            cell_str = str(root_values[x]).replace("\n", " ")
            if len(cell_str) > 64:
                cell_str = cell_str[:61] + "..."
            matrix[x][y] = " " + cell_str + " "
            num_equal = len(self.find_equal_to(root_values[x]))
            if num_equal > 1:
                matrix[x][y] += "(x{}) ".format(num_equal)

        # Make each column's strings equal in length.
        for x in range(len(matrix)):
            col_length = len(matrix[x][root_value_depths[x]])
            for y in range(len(matrix[x])):
                matrix[x][y] = matrix[x][y].ljust(col_length, " ")

        # Draw lines between parent and child nodes.
        unfinished_parents = [self, ]
        while len(unfinished_parents) > 0:
            working_node = unfinished_parents.pop(0)
            working_col_pos = root_values.index(working_node._node_value)
            working_row_pos = self.__get_value_root_depth(working_node._node_value)

            # Add line from left child node to parent.
            if isinstance(working_node._less_than, BinaryTree):
                unfinished_parents.append(working_node._less_than)
                child_col_pos = root_values.index(working_node._less_than._node_value)
                for x in range(child_col_pos, working_col_pos):
                    matrix[x][working_row_pos] = matrix[x][working_row_pos].replace(" ", "─")
                matrix[child_col_pos][working_row_pos] = " ┌" + matrix[child_col_pos][working_row_pos][2:]

            # Add line from right child node to parent.
            if isinstance(working_node._greater_than, BinaryTree):
                unfinished_parents.append(working_node._greater_than)
                child_col_pos = root_values.index(working_node._greater_than._node_value)
                for x in range(child_col_pos, working_col_pos, -1):
                    matrix[x][working_row_pos] = matrix[x][working_row_pos].replace(" ", "─")
                matrix[child_col_pos][working_row_pos] = "─┐".ljust(len(matrix[child_col_pos][working_row_pos]), " ")

        # Convert the matrix of strings into one printable string.
        result = ""
        for y in range(len(matrix[0])):
            line = ""
            for x in range(len(matrix)):
                line += matrix[x][y]
            result += line.rstrip(" ") + "\n"
        result.strip("\n")
        return result

    def to_flipped_display_string(self) -> str:
        result = self.to_display_string()
        result = result.replace("┌", "└")
        result = result.replace("┐", "┘")
        result = "\n".join([x for x in result.split('\n')[::-1]])
        result = result.strip("\n")
        return result

